from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

from ..core.types import AgentState


class FinancialAnalyst:
    """
    Handles financial analysis using LLM-based reasoning.
    """
    
    def __init__(self, model: str = "gpt-4-turbo", temperature: float = 0):
        """
        Initialize the financial analyst with specified LLM configuration.
        
        Args:
            model: LLM model to use for analysis
            temperature: Temperature setting for response generation
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Senior Financial Analyst. Your task is to analyze raw financial data and provide high-level insights.

    You must follow these reasoning steps (Chain of Thought):
    1. **Data Overview**: Summarize the key data points provided.
    2. **Trend Identification**: Is there an upward, downward, or stable trend? Explain why.
    3. **Risk Assessment**: What are the potential risks or red flags identified in this data?

    Write your analysis in a professional, objective, and structured manner."""),
            ("user", "Here is the data for {ticker}: {financial_data}")
        ])
        
    def analyze(self, state: AgentState) -> Dict[str, Any]:
        """
        Perform financial analysis on the provided data.
        
        Args:
            state: Current agent state with financial data
            
        Returns:
            Dictionary with sentiment analysis results and updated messages
        """
        print(f"--- Analyst is processing data for {state['ticker']} ---")
        current_iter = state.get('iterations', 0) + 1

        chain = self.prompt | self.llm

        response = chain.invoke({
            "ticker": state["ticker"],
            "financial_data": state["financial_data"],
            "iterations": current_iter,
        })

        return {
            "sentiment_analysis": response.content,
            "financial_data": state["financial_data"],
            "messages": [f"Analysis completed for {state['ticker']}."],
            "iterations": current_iter
        }


class ReportCritic:
    """
    Handles quality assurance and feedback for financial analysis reports.
    """
    
    def __init__(self, model: str = "gpt-4-turbo", temperature: float = 0):
        """
        Initialize the report critic with specified LLM configuration.
        
        Args:
            model: LLM model to use for criticism
            temperature: Temperature setting for response generation
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Senior Investment Editor. Your goal is to ensure that the Financial Analyst's report is data-driven, logical, and complete.

### EVALUATION RUBRIC:
1. **Data Integrity**: Does the report mention the specific Current Price, P/E Ratio, and Market Cap?
2. **Performance Context**: Did the analyst mention the 52-Week Change relative to the S&P 500? (Critical for momentum analysis).
3. **Risk/Reward Balance**: Does the report contrast the 'Analyst Price Targets' (Reward) against the 'Risk Score' and 'Debt to Equity' (Risk)?
4. **Professionalism**: Is the summary concise and free of generic fluff?

### OUTPUT INSTRUCTIONS:
- If ALL rubric items are met and the report is professional, respond with ONLY the word: **APPROVE**.
- If any data point is missing or the logic is flawed, respond with: **FEEDBACK: [List specific missing items or logical errors]**.

**Note**: Be firm but fair. If the report is 90% there, APPROVE it. Do not be pedantic about style, only focus on substance and data."""),
            ("user", """
REFERENCE DATA:
{financial_data}

ANALYST'S REPORT TO REVIEW:
{sentiment_analysis}
""")
        ])
        
    def review(self, state: AgentState) -> Dict[str, Any]:
        """
        Review and provide feedback on the financial analysis report.
        
        Args:
            state: Current agent state with analysis to review
            
        Returns:
            Dictionary with critic feedback and updated messages
        """
        print("--- Reviewing Report ---")
        chain = self.prompt | self.llm
        response = chain.invoke({
            "sentiment_analysis": state["sentiment_analysis"], 
            "financial_data": state["financial_data"]
        })

        return {
            "critic_feedback": response.content,
            "messages": ["Reviewing Done"]
        }