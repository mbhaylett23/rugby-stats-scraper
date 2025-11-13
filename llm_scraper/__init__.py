"""
LLM-Assisted Web Scraping Framework
====================================

A generic framework for building intelligent web scrapers powered by Large Language Models.

Key Features:
- 5-phase workflow: Plan → Scrape → Validate → Decide → Correct
- LLM-powered decision making and self-correction
- Extensible base classes for domain-specific implementations
- Built-in retry and error handling logic

Author: Created for intelligent web scraping
Version: 1.0.0
Date: November 2025
"""

__version__ = '1.0.0'
__author__ = 'LLM Scraper Framework'

from llm_scraper.core.base_scraper import BaseLLMScraper
from llm_scraper.core.llm_agent import LLMAgent
from llm_scraper.core.config import ScraperConfig

__all__ = ['BaseLLMScraper', 'LLMAgent', 'ScraperConfig']
