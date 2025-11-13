"""
Data extraction utilities for web scraping.

Provides base classes and common extraction patterns.
"""

import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """
    Abstract base class for data extractors.

    Extractors parse HTML/page content and extract structured data.
    """

    @abstractmethod
    def extract(
        self,
        soup: BeautifulSoup,
        page_text: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract data from page content.

        Args:
            soup: BeautifulSoup object of the page
            page_text: Plain text content of the page
            **kwargs: Additional extraction parameters

        Returns:
            Dictionary of extracted data
        """
        pass


class RegexExtractor(BaseExtractor):
    """
    Extractor that uses regex patterns to extract data.

    Useful for extracting statistics and structured data from text.
    """

    def __init__(self, patterns: Dict[str, str]):
        """
        Initialize regex extractor.

        Args:
            patterns: Dictionary mapping field names to regex patterns
        """
        self.patterns = patterns

    def extract(
        self,
        soup: BeautifulSoup,
        page_text: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract data using regex patterns.

        Args:
            soup: BeautifulSoup object (not used in this extractor)
            page_text: Plain text to search
            **kwargs: Additional parameters

        Returns:
            Dictionary of extracted data
        """
        extracted = {}

        for field_name, pattern in self.patterns.items():
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                extracted[field_name] = match.groups() if match.groups() else match.group(0)
            else:
                extracted[field_name] = None

        return extracted


class PairwiseStatExtractor(BaseExtractor):
    """
    Extractor for pairwise statistics (Team A vs Team B).

    Common in sports statistics where each stat shows two values.
    Example: "5 Tries 3" -> {team_a: 5, team_b: 3}
    """

    def __init__(self, stat_patterns: Dict[str, str]):
        """
        Initialize pairwise extractor.

        Args:
            stat_patterns: Dictionary mapping stat names to regex patterns
                          Patterns should capture two groups for the two values
        """
        self.stat_patterns = stat_patterns

    def extract(
        self,
        soup: BeautifulSoup,
        page_text: str,
        **kwargs
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Extract pairwise statistics.

        Args:
            soup: BeautifulSoup object (not used)
            page_text: Text to search
            **kwargs: Additional parameters

        Returns:
            Tuple of (team_a_stats, team_b_stats)
        """
        team_a_stats = {}
        team_b_stats = {}

        for stat_name, pattern in self.stat_patterns.items():
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                try:
                    team_a_stats[stat_name] = int(match.group(1))
                    team_b_stats[stat_name] = int(match.group(2))
                except (ValueError, IndexError):
                    team_a_stats[stat_name] = None
                    team_b_stats[stat_name] = None
            else:
                team_a_stats[stat_name] = None
                team_b_stats[stat_name] = None

        return team_a_stats, team_b_stats


class TableExtractor(BaseExtractor):
    """
    Extractor for HTML tables.

    Useful for extracting player statistics and tabular data.
    """

    def extract(
        self,
        soup: BeautifulSoup,
        page_text: str,
        table_selector: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Extract data from HTML tables.

        Args:
            soup: BeautifulSoup object
            page_text: Not used
            table_selector: CSS selector for the table (optional)
            **kwargs: Additional parameters

        Returns:
            List of dictionaries, one per row
        """
        extracted_data = []

        # Find tables
        if table_selector:
            tables = soup.select(table_selector)
        else:
            tables = soup.find_all('table')

        for table in tables:
            # Get headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]

            # Get rows
            tbody = table.find('tbody') or table
            rows = tbody.find_all('tr')

            for row in rows:
                cells = row.find_all(['td', 'th'])
                if cells and len(cells) == len(headers):
                    row_data = {
                        headers[i]: cell.get_text(strip=True)
                        for i, cell in enumerate(cells)
                    }
                    extracted_data.append(row_data)

        return extracted_data


class URLExtractor:
    """
    Utility for extracting information from URLs.
    """

    @staticmethod
    def extract_parameter(url: str, param_name: str) -> Optional[str]:
        """
        Extract a query parameter from a URL.

        Args:
            url: URL to parse
            param_name: Parameter name to extract

        Returns:
            Parameter value or None
        """
        pattern = f'{param_name}=([^&]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else None

    @staticmethod
    def extract_path_segment(url: str, position: int) -> Optional[str]:
        """
        Extract a path segment from URL.

        Args:
            url: URL to parse
            position: Position of segment (0-indexed)

        Returns:
            Path segment or None
        """
        from urllib.parse import urlparse

        parsed = urlparse(url)
        segments = [s for s in parsed.path.split('/') if s]

        if 0 <= position < len(segments):
            return segments[position]
        return None
