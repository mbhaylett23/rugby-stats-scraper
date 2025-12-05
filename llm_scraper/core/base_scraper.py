"""
Base scraper class for building domain-specific LLM-assisted scrapers.

All domain-specific scrapers should inherit from BaseLLMScraper and implement
the required abstract methods.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

from llm_scraper.core.llm_agent import LLMAgent
from llm_scraper.core.phases import PhaseExecutor
from llm_scraper.core.config import ScraperConfig
from llm_scraper.models.schemas import ScrapingPlan, ScrapedData

logger = logging.getLogger(__name__)


class BaseLLMScraper(ABC):
    """
    Abstract base class for LLM-assisted web scrapers.

    To create a domain-specific scraper:
    1. Inherit from this class
    2. Implement all abstract methods
    3. Override optional methods as needed

    Example:
        class MyDomainScraper(BaseLLMScraper):
            def get_planning_prompt(self) -> str:
                return "Instructions for planning in my domain..."

            def execute_scraping(self, plan: ScrapingPlan) -> ScrapedData:
                # Implement scraping logic
                ...
    """

    def __init__(self, config: ScraperConfig):
        """
        Initialize the base scraper.

        Args:
            config: Configuration for the scraper
        """
        # Validate configuration
        config.validate()
        self.config = config

        # Setup logging
        self._setup_logging()

        # Initialize LLM agent
        self.llm_agent = LLMAgent(
            api_key=config.llm_api_key,
            model_name=config.llm_model
        )

        # Initialize browser (to be done by subclass)
        self.driver = None

        # Data storage
        self.scraped_data = []
        self.agent_logs = []

        logger.info(f"✓ {self.__class__.__name__} initialized")

    def _setup_logging(self):
        """Setup logging based on config."""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{self.__class__.__name__.lower()}_log.txt'),
                logging.StreamHandler()
            ]
        )

    # =========================================================================
    # ABSTRACT METHODS - Must be implemented by subclasses
    # =========================================================================

    @abstractmethod
    def get_planning_prompt(self) -> str:
        """
        Return domain-specific instructions for the planning phase.

        The prompt should explain:
        - What you're trying to scrape
        - URL patterns or strategies
        - Any domain-specific considerations

        Returns:
            Planning instructions for the LLM
        """
        pass

    @abstractmethod
    def get_validation_prompt(self) -> str:
        """
        Return domain-specific instructions for validation.

        The prompt should explain:
        - What data should be present
        - What constitutes valid data
        - Domain-specific validation rules

        Returns:
            Validation instructions for the LLM
        """
        pass

    @abstractmethod
    def execute_scraping(self, plan: ScrapingPlan) -> ScrapedData:
        """
        Execute the scraping plan to extract data.

        This method should:
        1. Navigate to the URL in the plan
        2. Extract data using appropriate methods
        3. Return ScrapedData with results

        Args:
            plan: The scraping plan to execute

        Returns:
            ScrapedData with success status and extracted data
        """
        pass

    @abstractmethod
    def save_results(self, output_dir: Optional[str] = None) -> None:
        """
        Save scraped data to files.

        Args:
            output_dir: Directory to save results (uses config default if None)
        """
        pass

    # =========================================================================
    # OPTIONAL METHODS - Can be overridden by subclasses
    # =========================================================================

    def get_decision_prompt(self) -> Optional[str]:
        """
        Return optional domain-specific decision criteria.

        Returns:
            Decision criteria or None
        """
        return None

    def get_correction_prompt(self) -> str:
        """
        Return domain-specific instructions for corrections.

        Returns:
            Correction instructions for the LLM
        """
        return """
TASK: Suggest corrections to fix the scraping issues.

INSTRUCTIONS:
1. Suggest alternative URLs to try
2. Suggest adjustments to target information
3. Suggest different strategies
"""

    def initialize_browser(self) -> None:
        """
        Initialize the browser/selenium driver.

        Override this to customize browser setup.
        """
        from llm_scraper.utils.browser import BrowserManager

        browser_manager = BrowserManager(
            headless=self.config.headless_browser,
            timeout=self.config.browser_timeout
        )
        self.driver = browser_manager.get_driver()
        logger.info("✓ Browser initialized")

    def close_browser(self) -> None:
        """Close the browser."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✓ Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def scrape_target(self, target_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape a single target using the 5-phase workflow.

        Args:
            target_info: Information about what to scrape

        Returns:
            Dictionary with success status and results
        """
        # Initialize browser if not already done
        if self.driver is None:
            self.initialize_browser()

        # Create phase executor
        executor = PhaseExecutor(
            llm_agent=self.llm_agent,
            scraper_instance=self,
            config=self.config
        )

        # Execute workflow
        success, result = executor.execute_workflow(target_info)

        # Store results
        if success:
            self.scraped_data.append(result['data'])
            self.agent_logs.append(result['agent_log'])

        return result

    def scrape_multiple(
        self,
        targets: List[Dict[str, Any]],
        delay_between: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Scrape multiple targets.

        Args:
            targets: List of target information dictionaries
            delay_between: Optional delay between scrapes (seconds)

        Returns:
            List of results
        """
        import time

        results = []
        total = len(targets)

        logger.info(f"\n{'='*80}")
        logger.info(f"SCRAPING {total} TARGETS")
        logger.info(f"{'='*80}\n")

        for i, target in enumerate(targets, 1):
            logger.info(f"\n{'#'*80}")
            logger.info(f"TARGET {i}/{total}")
            logger.info(f"{'#'*80}")

            result = self.scrape_target(target)
            results.append(result)

            # Delay between scrapes
            if delay_between and i < total:
                time.sleep(delay_between)

        return results

    def scrape_from_file(
        self,
        file_path: str,
        delay_between: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Scrape targets from a JSON file.

        Args:
            file_path: Path to JSON file with target information
            delay_between: Optional delay between scrapes (seconds)

        Returns:
            List of results
        """
        import json

        logger.info(f"Loading targets from: {file_path}")

        with open(file_path, 'r') as f:
            targets = json.load(f)

        logger.info(f"Found {len(targets)} targets")

        return self.scrape_multiple(targets, delay_between)

    # =========================================================================
    # CONTEXT MANAGER SUPPORT
    # =========================================================================

    def __enter__(self):
        """Context manager entry."""
        self.initialize_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_browser()
        return False
