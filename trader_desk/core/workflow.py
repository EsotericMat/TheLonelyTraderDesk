from langgraph.graph import StateGraph, END
from typing import Dict, Any, Optional

from .types import AgentState
from .config import AppConfig
from ..utils.data_fetcher import FinancialDataFetcher
from ..nodes.analysis import FinancialAnalyst, ReportCritic


class TradingWorkflow:
    """
    Manages the complete financial analysis workflow using LangGraph.
    """
    
    def __init__(self, config: Optional[AppConfig] = None):
        """
        Initialize the trading workflow.
        
        Args:
            config: Application configuration, defaults to environment-based config
        """
        self.config = config or AppConfig.from_environment()
        self.max_iterations = self.config.workflow.max_iterations
        self.data_fetcher = FinancialDataFetcher()
        self.analyst = FinancialAnalyst(
            model=self.config.llm.model,
            temperature=self.config.llm.temperature
        )
        self.critic = ReportCritic(
            model=self.config.llm.model,
            temperature=self.config.llm.temperature
        )
        self.app = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        Build and compile the workflow graph.
        
        Returns:
            Compiled workflow application
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node('Fetcher', self._fetch_node)
        workflow.add_node('Analyst', self._analyst_node)
        workflow.add_node('Critic', self._critic_node)
        
        # Set entry point
        workflow.set_entry_point('Fetcher')
        
        # Add fixed edges
        workflow.add_edge('Fetcher', 'Analyst')
        workflow.add_edge('Analyst', 'Critic')
        
        # Add conditional edge for refinement loop
        workflow.add_conditional_edges(
            'Critic',
            self._should_continue,
            {
                "end": END,
                "refine": "Analyst"
            }
        )
        
        return workflow.compile()
    
    def _fetch_node(self, state: AgentState) -> Dict[str, Any]:
        """Wrapper for data fetching node."""
        return self.data_fetcher.fetch_financial_data(state)
    
    def _analyst_node(self, state: AgentState) -> Dict[str, Any]:
        """Wrapper for analyst node."""
        return self.analyst.analyze(state)
    
    def _critic_node(self, state: AgentState) -> Dict[str, Any]:
        """Wrapper for critic node."""
        return self.critic.review(state)
    
    def _should_continue(self, state: AgentState) -> str:
        """
        Determine whether to continue refinement or end the workflow.
        
        Args:
            state: Current agent state
            
        Returns:
            Next step: 'end' or 'refine'
        """
        if state.get('iterations', 0) >= self.max_iterations:
            return "end"

        if "APPROVE" in state["critic_feedback"].upper():
            return "end"
        else:
            return "refine"
    
    def run(self, ticker: str, verbose: bool = True) -> AgentState:
        """
        Execute the complete workflow for a given ticker.
        
        Args:
            ticker: Stock symbol to analyze
            verbose: Whether to print step-by-step progress
            
        Returns:
            Final state containing all analysis results
        """
        initial_input = {
            "ticker": ticker,
            "messages": [],
            "financial_data": "",
            "sentiment_analysis": "",
            "critic_feedback": "",
            "report": "",
            "iterations": 0
        }
        
        if verbose:
            print(f"--- Starting Financial Analysis for {ticker} ---")
            print("--- Streaming Agent Steps ---")
            
            for event in self.app.stream(initial_input):
                for node_name, output in event.items():
                    print(f"\n[Node Completed: {node_name}]")
        
        # Execute the workflow
        final_state = self.app.invoke(initial_input)
        
        if verbose:
            self._print_results(final_state)
        
        return final_state
    
    def _print_results(self, final_state: AgentState) -> None:
        """
        Print formatted final results.
        
        Args:
            final_state: Completed workflow state
        """
        print("\n" + "=" * 50)
        print(f"FINAL REPORT FOR: {final_state['ticker']}")
        print("=" * 50)
        print(f"Analysis:\n{final_state['sentiment_analysis']}")
        print("-" * 30)
        print(f"Critic's Final Verdict: {final_state['critic_feedback']}")
        print("=" * 50)