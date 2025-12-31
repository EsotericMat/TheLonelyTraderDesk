"""
The Lonely Trader Desk - Financial Analysis Application

A production-grade financial analysis tool using AI agents to analyze stock data,
provide insights, and generate comprehensive reports with built-in quality assurance.
"""

import sys
from dotenv import load_dotenv

from .core.workflow import TradingWorkflow
from .core.config import AppConfig


def main(ticker: str = "AAPL"):
    """
    Main application entry point.
    
    Args:
        ticker: Stock symbol to analyze
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize configuration from environment
        config = AppConfig.from_environment()
        
        # Initialize the workflow with configuration
        workflow = TradingWorkflow(config)
        
        # Run analysis
        final_state = workflow.run(
            ticker, 
            verbose=config.workflow.enable_verbose_logging
        )
        
        # Optionally save results if enabled
        if config.workflow.enable_result_saving:
            save_results(final_state)
            
        return final_state
        
    except Exception as e:
        print(f"Error running financial analysis: {e}")
        raise


def save_results(final_state):
    """
    Save analysis results to file or database.
    
    Args:
        final_state: Final workflow state with results
    """
    # Implementation for saving results
    # Could save to JSON file, database, etc.
    import json
    import datetime
    
    filename = f"analysis_{final_state['ticker']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    results = {
        "ticker": final_state["ticker"],
        "analysis": final_state["sentiment_analysis"],
        "critic_feedback": final_state["critic_feedback"],
        "timestamp": datetime.datetime.now().isoformat(),
        "iterations": final_state["iterations"]
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {filename}")


def cli_main():
    """CLI entry point that handles command line arguments."""
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    main(ticker)


if __name__ == "__main__":
    cli_main()