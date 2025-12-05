"""
Rugby-specific data extractors.

Implements extraction logic for rugby statistics from RugbyPass pages.
"""

import re
import logging
from typing import Dict, Tuple, List
from bs4 import BeautifulSoup

from llm_scraper.utils.extractors import PairwiseStatExtractor

logger = logging.getLogger(__name__)


class RugbyStatsExtractor:
    """
    Extractor for rugby match statistics from RugbyPass.

    Uses regex patterns to extract pairwise statistics (home vs away).
    """

    def __init__(self):
        """Initialize rugby stats extractor."""
        # Define stat patterns for RugbyPass format
        self.stat_patterns = {
            'tries': r'(\d+)\s+Tries\s+(\d+)',
            'conversions': r'(\d+)\s+Conversions?\s+(\d+)',
            'penalty_goals': r'(\d+)\s+Penalty Goals?\s+(\d+)',
            'drop_goals': r'(\d+)\s+Drop Goals?\s+(\d+)',
            'possession_pct': r'(\d+)%?\s+Possession\s+(\d+)%?',
            'territory_pct': r'(\d+)%?\s+Territory\s+(\d+)%?',
            'carries': r'(\d+)\s+Carries\s+(\d+)',
            'metres_made': r'(\d+)\s+Metres?\s+Made\s+(\d+)',
            'clean_breaks': r'(\d+)\s+Clean Breaks?\s+(\d+)',
            'defenders_beaten': r'(\d+)\s+Defenders?\s+Beaten\s+(\d+)',
            'line_breaks': r'(\d+)\s+Line Breaks?\s+(\d+)',
            'offloads': r'(\d+)\s+Offloads?\s+(\d+)',
            'passes': r'(\d+)\s+Passes\s+(\d+)',
            'tackles_made': r'(\d+)\s+Tackles Made\s+(\d+)',
            'tackles_missed': r'(\d+)\s+Tackles Missed\s+(\d+)',
            'turnovers_won': r'(\d+)\s+Turnovers?\s+Won\s+(\d+)',
            'turnovers_conceded': r'(\d+)\s+Turnovers?\s+Conceded\s+(\d+)',
            'scrums_won': r'(\d+)\s+Scrums?\s+Won\s+(\d+)',
            'lineouts_won': r'(\d+)\s+Lineouts?\s+Won\s+(\d+)',
            'penalties_conceded': r'(\d+)\s+Penalties\s+Conceded\s+(\d+)',
            'yellow_cards': r'(\d+)\s+Yellow Cards?\s+(\d+)',
            'red_cards': r'(\d+)\s+Red Cards?\s+(\d+)',
        }

        self.pairwise_extractor = PairwiseStatExtractor(self.stat_patterns)

    def extract_rugby_stats(
        self,
        soup: BeautifulSoup,
        page_text: str,
        game_id: str,
        url: str
    ) -> Tuple[Dict, List[Dict]]:
        """
        Extract rugby statistics from a RugbyPass page.

        Args:
            soup: BeautifulSoup object of the page
            page_text: Plain text of the page
            game_id: Game ID
            url: URL of the page

        Returns:
            Tuple of (match_info, team_stats_list)
        """
        # Extract match info
        match_info = {
            'game_id': game_id,
            'url': url
        }

        # Extract team names from page if possible
        team_names = self._extract_team_names(soup, page_text)
        if team_names:
            match_info['home_team'] = team_names[0]
            match_info['away_team'] = team_names[1]

        # Extract match score
        score = self._extract_score(page_text)
        if score:
            match_info['home_score'] = score[0]
            match_info['away_score'] = score[1]

        # Extract pairwise statistics
        home_stats, away_stats = self.pairwise_extractor.extract(soup, page_text)

        # Add metadata
        home_stats['game_id'] = game_id
        home_stats['team'] = 'home'
        away_stats['game_id'] = game_id
        away_stats['team'] = 'away'

        # Calculate derived stats
        home_stats = self._add_derived_stats(home_stats)
        away_stats = self._add_derived_stats(away_stats)

        logger.info(f"  ✓ Extracted {len([k for k, v in home_stats.items() if v is not None])} stats for home team")
        logger.info(f"  ✓ Extracted {len([k for k, v in away_stats.items() if v is not None])} stats for away team")

        return match_info, [home_stats, away_stats]

    def _extract_team_names(
        self,
        soup: BeautifulSoup,
        page_text: str
    ) -> Tuple[str, str] | None:
        """
        Try to extract team names from the page.

        Args:
            soup: BeautifulSoup object
            page_text: Plain text

        Returns:
            Tuple of (home_team, away_team) or None
        """
        # Try to find team names in the title or headings
        title = soup.find('title')
        if title:
            title_text = title.get_text()
            # Pattern: "Team A vs Team B"
            match = re.search(r'([A-Za-z\s]+)\s+vs\s+([A-Za-z\s]+)', title_text)
            if match:
                return match.group(1).strip(), match.group(2).strip()

        return None

    def _extract_score(self, page_text: str) -> Tuple[int, int] | None:
        """
        Extract final score from page.

        Args:
            page_text: Plain text of page

        Returns:
            Tuple of (home_score, away_score) or None
        """
        # Pattern: "Score: 25 - 18" or "25-18"
        patterns = [
            r'Score:?\s*(\d+)\s*-\s*(\d+)',
            r'Final:?\s*(\d+)\s*-\s*(\d+)',
            r'(\d+)\s*-\s*(\d+)\s+Final'
        ]

        for pattern in patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                return int(match.group(1)), int(match.group(2))

        return None

    def _add_derived_stats(self, stats: Dict) -> Dict:
        """
        Calculate derived statistics.

        Args:
            stats: Dictionary of stats

        Returns:
            Stats with derived values added
        """
        # Tackle success rate
        if stats.get('tackles_made') and stats.get('tackles_missed'):
            total_tackles = stats['tackles_made'] + stats['tackles_missed']
            if total_tackles > 0:
                stats['tackle_success_rate'] = round(
                    (stats['tackles_made'] / total_tackles) * 100, 1
                )

        # Points from tries/conversions/penalties
        tries = stats.get('tries', 0) or 0
        conversions = stats.get('conversions', 0) or 0
        penalties = stats.get('penalty_goals', 0) or 0
        drop_goals = stats.get('drop_goals', 0) or 0

        stats['calculated_points'] = (tries * 5) + (conversions * 2) + (penalties * 3) + (drop_goals * 3)

        return stats
