"""
Browser and Selenium utilities for web scraping.

Provides a clean interface for browser management with sensible defaults.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional

logger = logging.getLogger(__name__)


class BrowserManager:
    """
    Manages browser/Selenium WebDriver instances.

    Handles initialization, configuration, and cleanup of browser sessions.
    """

    def __init__(
        self,
        headless: bool = False,
        timeout: int = 30,
        user_agent: Optional[str] = None
    ):
        """
        Initialize browser manager.

        Args:
            headless: Run browser in headless mode
            timeout: Page load timeout in seconds
            user_agent: Custom user agent string
        """
        self.headless = headless
        self.timeout = timeout
        self.user_agent = user_agent or (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36'
        )
        self._driver = None

    def get_driver(self) -> webdriver.Chrome:
        """
        Get or create a Chrome WebDriver instance.

        Returns:
            Configured Chrome WebDriver
        """
        if self._driver is None:
            self._driver = self._create_driver()
        return self._driver

    def _create_driver(self) -> webdriver.Chrome:
        """Create and configure a new Chrome WebDriver."""
        chrome_options = Options()

        # Headless mode
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

        # Performance and stability options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        # User agent
        chrome_options.add_argument(f'user-agent={self.user_agent}')

        # Additional options for stability
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')

        # Create service
        service = Service(ChromeDriverManager().install())

        # Create driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(self.timeout)

        logger.info("✓ Chrome WebDriver created")
        return driver

    def close(self):
        """Close the browser and cleanup."""
        if self._driver:
            try:
                self._driver.quit()
                self._driver = None
                logger.info("✓ Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.close()


class PageNavigator:
    """
    Helper class for common page navigation operations.
    """

    def __init__(self, driver: webdriver.Chrome):
        """
        Initialize page navigator.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver

    def load_page(self, url: str, wait_time: int = 4) -> bool:
        """
        Load a page and wait for it to load.

        Args:
            url: URL to load
            wait_time: Time to wait after loading (seconds)

        Returns:
            True if successful, False otherwise
        """
        import time

        try:
            self.driver.get(url)
            time.sleep(wait_time)
            return True
        except Exception as e:
            logger.error(f"Error loading page {url}: {e}")
            return False

    def get_page_source(self) -> str:
        """Get the current page source."""
        return self.driver.page_source

    def get_current_url(self) -> str:
        """Get the current URL."""
        return self.driver.current_url

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def wait_for_element(self, by, value, timeout=10):
        """
        Wait for an element to be present.

        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time in seconds

        Returns:
            WebElement if found, None otherwise
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logger.warning(f"Element not found: {by}={value}")
            return None
