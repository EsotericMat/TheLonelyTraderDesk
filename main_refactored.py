"""
Production-grade entry point for The Lonely Trader Desk.

This replaces the original main.py with a clean, modular architecture.
"""

from trader_desk.main import main, cli_main

if __name__ == "__main__":
    cli_main()