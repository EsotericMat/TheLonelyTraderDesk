"""
Configuration management for The Lonely Trader Desk.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """Configuration for Language Model settings."""
    model: str = "gpt-4-turbo"
    temperature: float = 0.0
    max_tokens: Optional[int] = None


@dataclass
class WorkflowConfig:
    """Configuration for workflow behavior."""
    max_iterations: int = 3
    enable_verbose_logging: bool = True
    enable_result_saving: bool = False


@dataclass
class AppConfig:
    """Main application configuration."""
    llm: LLMConfig
    workflow: WorkflowConfig
    openai_api_key: str
    
    @classmethod
    def from_environment(cls) -> "AppConfig":
        """
        Create configuration from environment variables.
        
        Returns:
            AppConfig instance with values from environment
            
        Raises:
            ValueError: If required environment variables are missing
        """
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return cls(
            llm=LLMConfig(
                model=os.getenv("LLM_MODEL", "gpt-4-turbo"),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.0")),
                max_tokens=int(os.getenv("LLM_MAX_TOKENS")) if os.getenv("LLM_MAX_TOKENS") else None
            ),
            workflow=WorkflowConfig(
                max_iterations=int(os.getenv("MAX_ITERATIONS", "3")),
                enable_verbose_logging=os.getenv("VERBOSE_LOGGING", "true").lower() == "true",
                enable_result_saving=os.getenv("SAVE_RESULTS", "false").lower() == "true"
            ),
            openai_api_key=openai_api_key
        )