"""
Configuration management for the LLM scraping framework.

Handles loading and managing configuration from various sources
(YAML files, environment variables, code).
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ScraperConfig:
    """
    Configuration for the LLM scraper.

    Attributes:
        llm_provider: LLM provider ("gemini", "openai", etc.)
        llm_model: Model name (e.g., "gemini-2.0-flash-exp")
        llm_api_key: API key for LLM service
        max_retries: Maximum retry attempts per scraping target
        retry_delay: Delay between retries in seconds
        headless_browser: Run browser in headless mode
        browser_timeout: Browser page load timeout in seconds
        confidence_threshold: Minimum confidence to accept data
        log_level: Logging level
        output_dir: Directory for output files
        custom_settings: Domain-specific custom settings
    """
    # LLM Settings
    llm_provider: str = "gemini"
    llm_model: str = "gemini-2.0-flash-exp"
    llm_api_key: Optional[str] = None

    # Scraping Settings
    max_retries: int = 3
    retry_delay: int = 2
    headless_browser: bool = False
    browser_timeout: int = 30

    # Validation Settings
    confidence_threshold: int = 80

    # Logging & Output
    log_level: str = "INFO"
    output_dir: str = "."

    # Custom Settings (domain-specific)
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'ScraperConfig':
        """
        Load configuration from a YAML file.

        Args:
            yaml_path: Path to YAML configuration file

        Returns:
            ScraperConfig instance
        """
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        return cls(
            llm_provider=data.get('llm_provider', 'gemini'),
            llm_model=data.get('llm_model', 'gemini-2.0-flash-exp'),
            llm_api_key=data.get('llm_api_key'),
            max_retries=data.get('max_retries', 3),
            retry_delay=data.get('retry_delay', 2),
            headless_browser=data.get('headless_browser', False),
            browser_timeout=data.get('browser_timeout', 30),
            confidence_threshold=data.get('confidence_threshold', 80),
            log_level=data.get('log_level', 'INFO'),
            output_dir=data.get('output_dir', '.'),
            custom_settings=data.get('custom_settings', {})
        )

    @classmethod
    def from_env(cls) -> 'ScraperConfig':
        """
        Load configuration from environment variables.

        Environment variables:
            GEMINI_API_KEY or OPENAI_API_KEY: API key
            LLM_MODEL: Model name
            MAX_RETRIES: Maximum retries
            HEADLESS: Run headless browser

        Returns:
            ScraperConfig instance
        """
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('OPENAI_API_KEY')

        return cls(
            llm_api_key=api_key,
            llm_model=os.getenv('LLM_MODEL', 'gemini-2.0-flash-exp'),
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            headless_browser=os.getenv('HEADLESS', 'false').lower() == 'true'
        )

    def merge_with_yaml(self, yaml_path: str) -> 'ScraperConfig':
        """
        Merge current config with settings from a YAML file.

        YAML settings override current settings.

        Args:
            yaml_path: Path to YAML file

        Returns:
            Updated ScraperConfig instance
        """
        yaml_config = self.from_yaml(yaml_path)

        # YAML overrides everything except API key if not specified
        if yaml_config.llm_api_key is None:
            yaml_config.llm_api_key = self.llm_api_key

        return yaml_config

    def validate(self) -> None:
        """
        Validate configuration settings.

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.llm_api_key:
            raise ValueError(
                "No API key found. Set GEMINI_API_KEY or OPENAI_API_KEY "
                "environment variable, or provide it in config file."
            )

        if self.max_retries < 1:
            raise ValueError("max_retries must be at least 1")

        if self.confidence_threshold < 0 or self.confidence_threshold > 100:
            raise ValueError("confidence_threshold must be between 0 and 100")
