import os
from typing import TypedDict, Annotated, List
import operator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
import yfinance as yf

load_dotenv()

# State definition
class AgentState(TypedDict):
    ticker: str
    financial_data: str
    sentiment_analysis: str
    critic_feedback: str  # שדה חדש למשוב
    report: str
    messages: Annotated[List[str], operator.add]
    iterations: int


def fetch_financial_data(state: AgentState):
    ticker = state['ticker']
    print(f"--- Fetching real-time data for {ticker} ---")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        analyst_price_target = stock.analyst_price_targets

        current_price = info.get('currentPrice')
        market_cap = info.get('marketCap')
        pe_ratio = info.get('forwardPE')
        summary = info.get('longBusinessSummary', 'No summary available.')
        change52weeks = info.get('52WeekChange', 'No data for a change over 52 weeks') * 100
        market_change = info.get('SandP52WeekChange', 'No data for a  market change over 52 weeks') * 100
        overall_risk_score = info.get('overallRisk', 'No Risk data')
        volatility_score = info.get('beta', 'No beta score')
        debt_to_equity = info.get('debtToEquity', 'No data about debt to equity')


        real_data = f"""
           Stock: {ticker}
           Current Price: ${current_price}
           Market Cap: ${market_cap:,}
           Forward P/E Ratio: {pe_ratio}
           Business Summary: {summary[:500]}
           Analysts price target: {analyst_price_target}
           52 Weeks change: {change52weeks:.2f}
           52 weeks Market change: {market_change:.2f}
           Relative performance: {change52weeks - market_change:.2f}
           Risk data:
                Risk score: {overall_risk_score}/10
                Volatility score: {volatility_score}
                Debt to Equity: {debt_to_equity}
        """

        return {
            "financial_data": real_data,
            "messages": [f"Fetched live data for {ticker}"]
        }
    except Exception as e:
        return {
            "financial_data": f"Error fetching data: {str(e)}",
            "messages": ["Failed to fetch data"]
        }

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
analyst_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior Financial Analyst. Your task is to analyze raw financial data and provide high-level insights.

    You must follow these reasoning steps (Chain of Thought):
    1. **Data Overview**: Summarize the key data points provided.
    2. **Trend Identification**: Is there an upward, downward, or stable trend? Explain why.
    3. **Risk Assessment**: What are the potential risks or red flags identified in this data?

    Write your analysis in a professional, objective, and structured manner."""),
    ("user", "Here is the data for {ticker}: {financial_data}")
])

def financial_analyst_node(state: AgentState):
    """
    Node 2: The analyst performing the reasoning based on fetched data.
    """
    print(f"--- Analyst is processing data for {state['ticker']} ---")
    current_iter = state.get('iterations', 0) + 1

    chain = analyst_prompt | llm

    response = chain.invoke({
        "ticker": state["ticker"],
        "financial_data": state["financial_data"],
        "iterations": current_iter,
    })

    return {
        "sentiment_analysis": response.content,
        "financial_data": state["financial_data"],
        "messages": [f"Analysis completed for {state['ticker']}."]
    }

critic_prompt = ChatPromptTemplate.from_messages([
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

def critic_node(state: AgentState):
    print("--- Reviewing Report ---")
    chain = critic_prompt | llm
    response = chain.invoke({"sentiment_analysis": state["sentiment_analysis"], "financial_data": state["financial_data"]})

    return {
        "critic_feedback": response.content,
        "messages": ["Reviewing Done"]
    }


# Rout
def should_continue(state: AgentState) -> str:
    """
    Route the critic decision
    """
    if state.get('iterations', 0) >= 3:
        return "end"

    if "APPROVE" in state["critic_feedback"].upper():
        return "end"
    else:
        return "refine"

# Workflow instance
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node('Fetcher', fetch_financial_data)
workflow.add_node('Analyst', financial_analyst_node)
workflow.add_node('Critic', critic_node)

# Add fixed relations
workflow.set_entry_point('Fetcher')
workflow.add_edge('Fetcher', 'Analyst')
workflow.add_edge('Analyst', 'Critic')

# Add conditional edge
workflow.add_conditional_edges(
    'Critic',
    should_continue,
    {
        "end": END,
        "refine": "Analyst"
    }
)

app = workflow.compile()

if __name__ == "__main__":
    initial_input = {
        "ticker": "AAPL",
        "messages": [],
        "financial_data": "",
        "sentiment_analysis": "",
        "critic_feedback": "",
        "iterations": 0  # CRITICAL: Starts the counter at zero
    }

    print("--- Starting the Financial Agent Workflow ---")

    # 2. הרצת הגרף (Invoke)
    # הפונקציה מחזירה את ה-State הסופי אחרי שכל ה-Nodes סיימו
    print("--- Streaming Agent Steps ---")
    for event in app.stream(initial_input):
        # בכל צעד, הגרף פולט מילון שבו המפתח הוא שם ה-Node שסיים
        for node_name, output in event.items():
            print(f"\n[Node Completed: {node_name}]")

    final_state = app.invoke(initial_input)

    # 3. הדפסת התוצאות מה-State הסופי
    print("\n" + "=" * 50)
    print(f"FINAL REPORT FOR: {final_state['ticker']}")
    print("=" * 50)
    print(f"Analysis:\n{final_state['sentiment_analysis']}")
    print("-" * 30)
    print(f"Critic's Final Verdict: {final_state['critic_feedback']}")
    print("=" * 50)
