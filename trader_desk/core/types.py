from typing import TypedDict, Annotated, List
import operator


class AgentState(TypedDict):
    """
    State definition for the financial analysis workflow.
    
    Attributes:
        ticker: Stock symbol to analyze
        financial_data: Raw financial data fetched from APIs
        sentiment_analysis: Analysis results from the financial analyst
        critic_feedback: Feedback from the critic node
        report: Final generated report
        messages: Log of workflow messages
        iterations: Number of iterations through the workflow
    """
    ticker: str
    financial_data: str
    sentiment_analysis: str
    critic_feedback: str
    report: str
    messages: Annotated[List[str], operator.add]
    iterations: int


class FinancialData(TypedDict):
    """
    Structured financial data extracted from APIs.
    """
    ticker: str
    current_price: float
    market_cap: int
    pe_ratio: float
    business_summary: str
    analyst_price_target: dict
    change_52_weeks: float
    market_change_52_weeks: float
    relative_performance: float
    risk_score: int
    volatility_score: float
    debt_to_equity: float