from http.client import HTTPException
from dotenv import load_dotenv
import yfinance as yf
from typing import Dict, Any
from ..core.types import AgentState
from tavily import TavilyClient

load_dotenv()

class FinancialDataFetcher:
    """
    Handles fetching of real-time financial data using Yahoo Finance.
    """
    CLIENT = TavilyClient()

    def get_financial_news(self, ticker: str, results: int = 3):
        """
        Grab some new about given symbol
        :param ticker:
        :param results: How many headlines to fetch
        :return:
        """
        try:
            search_result = self.CLIENT.search(
                query=f"latest market news and financial sentiment for {ticker} today",
                max_results=results
            )
            formatted_news = ""
            for res in search_result['results']:
                formatted_news += f"Title: {res['title']}\n"
                formatted_news += f"Snippet: {res['content']}\n\n"

            return formatted_news

        except HTTPException as e:
            return ''

    

    def fetch_financial_data(self, state: AgentState) -> Dict[str, Any]:
        """
        Fetch comprehensive financial data for a given ticker.
        
        Args:
            state: Current agent state containing the ticker symbol
            
        Returns:
            Dictionary with updated financial_data and messages
        """
        ticker = state['ticker']
        print(f"--- Fetching real-time data for {ticker} ---")

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            analyst_price_target = stock.analyst_price_targets
            news = self.get_financial_news(ticker)

            current_price = info.get('currentPrice')
            market_cap = info.get('marketCap')
            pe_ratio = info.get('forwardPE')
            summary = info.get('longBusinessSummary', 'No summary available.')
            change52weeks = info.get('52WeekChange', 'No data for a change over 52 weeks')
            market_change = info.get('SandP52WeekChange', 'No data for a market change over 52 weeks')
            overall_risk_score = info.get('overallRisk', 'No Risk data')
            volatility_score = info.get('beta', 'No beta score')
            debt_to_equity = info.get('debtToEquity', 'No data about debt to equity')

            # Handle percentage calculations safely
            if isinstance(change52weeks, (int, float)):
                change52weeks_pct = change52weeks * 100
            else:
                change52weeks_pct = 'No data'
                
            if isinstance(market_change, (int, float)):
                market_change_pct = market_change * 100
            else:
                market_change_pct = 'No data'
                
            # Calculate relative performance
            if (isinstance(change52weeks, (int, float)) and 
                isinstance(market_change, (int, float))):
                relative_performance = (change52weeks - market_change) * 100
            else:
                relative_performance = 'No data'

            real_data = f"""
               Stock: {ticker}
               Current Price: ${current_price}
               Market Cap: ${market_cap:,}
               Forward P/E Ratio: {pe_ratio}
               Business Summary: {summary[:500]}
               Analysts price target: {analyst_price_target}
               52 Weeks change: {change52weeks_pct}
               52 weeks Market change: {market_change_pct}
               Relative performance: {relative_performance}
               Risk data:
                    Risk score: {overall_risk_score}/10
                    Volatility score: {volatility_score}
                    Debt to Equity: {debt_to_equity}
               Latest news:
                    {news}
                """

            return {
                "financial_data": real_data,
                "messages": [f"Fetched live data for {ticker}"]
            }
            
        except Exception as e:
            return {
                "financial_data": f"Error fetching data: {str(e)}",
                "messages": [f"Failed to fetch data for {ticker}: {str(e)}"]
            }