"""
Rugby Statistics Scraper implementation using the LLM scraping framework.

This demonstrates how to build a domain-specific scraper by extending
the base framework classes.
"""

import re
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup

from llm_scraper.core.base_scraper import BaseLLMScraper
from llm_scraper.core.config import ScraperConfig
from llm_scraper.models.schemas import ScrapingPlan, ScrapedData
from llm_scraper.utils.browser import PageNavigator
from rugby_scraper.extractors import RugbyStatsExtractor

logger = logging.getLogger(__name__)


class RugbyStatsScraper(BaseLLMScraper):
    """
    Scraper for rugby match statistics from RugbyPass.

    Extends BaseLLMScraper to provide rugby-specific scraping logic.
    """

    def __init__(self, config: ScraperConfig):
        """
        Initialize rugby scraper.

        Args:
            config: Scraper configuration
        """
        super().__init__(config)

        # Rugby-specific data storage
        self.matches_data = []
        self.team_stats_data = []
        self.player_stats_data = []

        # Initialize extractor
        self.extractor = RugbyStatsExtractor()

        logger.info("✓ Rugby Stats Scraper initialized")

    # =========================================================================
    # IMPLEMENT ABSTRACT METHODS
    # =========================================================================

    def get_planning_prompt(self) -> str:
        """Return rugby-specific planning instructions."""
        return """
TASK: Create a plan to find and scrape this rugby match from RugbyPass.com

INSTRUCTIONS:
1. If game_id or URL is known, use it directly
2. If not, construct the URL from team names and date
3. Consider team name variations:
   - "New Zealand" = "All Blacks" = "NZ"
   - "South Africa" = "Springboks" = "SA"
   - "Ireland" = "Irish"
   - etc.
4. RugbyPass URL pattern: /live/{{home-team}}-vs-{{away-team}}/stats/?g={{game_id}}
5. Team names in URL are lowercase with hyphens
6. Example: https://www.rugbypass.com/live/france-vs-wales/stats/?g=944287

STRATEGY OPTIONS:
- "direct_url": Use known URL or game_id
- "construct_url": Build URL from team names
- "search_required": Need to search for the match first
"""

    def get_validation_prompt(self) -> str:
        """Return rugby-specific validation instructions."""
        return """
TASK: Validate if the scraped rugby statistics are correct and complete.

VALIDATION CHECKS:
1. Team names: Do they match the expected match?
2. Statistics logic:
   - Tries should be reasonable (0-10 per team typically)
   - Possession percentages should add up to ~100%
   - Tackles made > tackles missed (usually)
   - Points = (tries × 5) + (conversions × 2) + (penalties × 3) + (drop goals × 3)
3. Required statistics:
   - tries, conversions, penalty_goals
   - possession_pct
   - tackles_made, tackles_missed
   - carries, line_breaks
4. Data completeness: Are key stats present?
5. Page content: Does it mention the right teams and competition?

COMMON ISSUES:
- Wrong match loaded (check team names in page content)
- Missing statistics (incomplete page load)
- Suspicious values (e.g., 99% possession, 0 tackles)
"""

    def get_correction_prompt(self) -> str:
        """Return rugby-specific correction instructions."""
        return """
TASK: Suggest corrections to fix rugby scraping issues.

COMMON FIXES:
1. Alternative team name spellings:
   - "Scotland" vs "scotland"
   - "Italy" vs "Italia" (Italian spelling)
   - "New Zealand" vs "all-blacks" vs "new-zealand"
2. Alternative URL formats:
   - Try with/without competition name
   - Try different date formats
   - Try different game_id values
3. Search strategies:
   - Search RugbyPass for the match
   - Use competition + date to find match
   - Look for fixture lists

INSTRUCTIONS:
Analyze the validation issues and suggest specific corrections to try.
"""

    def execute_scraping(self, plan: ScrapingPlan) -> ScrapedData:
        """
        Execute rugby scraping plan.

        Args:
            plan: Scraping plan from LLM

        Returns:
            ScrapedData with rugby statistics
        """
        logger.info(f"  Loading: {plan.url_to_try}")

        try:
            # Navigate to page
            navigator = PageNavigator(self.driver)
            if not navigator.load_page(plan.url_to_try, wait_time=4):
                return ScrapedData(
                    success=False,
                    error="Failed to load page"
                )

            # Get page content
            page_source = navigator.get_page_source()
            current_url = navigator.get_current_url()
            soup = BeautifulSoup(page_source, 'html.parser')
            page_text = soup.get_text()

            # Extract game_id
            game_id_match = re.search(r'\?g=(\d+)', current_url)
            game_id = game_id_match.group(1) if game_id_match else None

            if not game_id:
                return ScrapedData(
                    success=False,
                    error="Could not find game_id in URL"
                )

            logger.info(f"  ✓ Found game_id: {game_id}")

            # Extract statistics
            match_info, team_stats = self.extractor.extract_rugby_stats(
                soup, page_text, game_id, current_url
            )

            logger.info(f"  ✓ Extracted statistics for game {game_id}")

            return ScrapedData(
                success=True,
                url=current_url,
                data={
                    'match_info': match_info,
                    'team_stats': team_stats,
                    'player_stats': []  # TODO: Add player stats extraction
                },
                page_content_sample=page_text[:2000],
                metadata={'game_id': game_id}
            )

        except Exception as e:
            logger.error(f"  ✗ Scraping error: {e}")
            return ScrapedData(
                success=False,
                error=str(e)
            )

    def save_results(self, output_dir: Optional[str] = None) -> None:
        """
        Save rugby statistics to CSV files.

        Args:
            output_dir: Directory to save results
        """
        output_path = Path(output_dir or self.config.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        logger.info(f"\n{'='*80}")
        logger.info("SAVING RUGBY STATISTICS")
        logger.info(f"{'='*80}\n")

        # Collect all data from scraped results
        for result in self.scraped_data:
            if 'match_info' in result:
                self.matches_data.append(result['match_info'])
            if 'team_stats' in result:
                self.team_stats_data.extend(result['team_stats'])
            if 'player_stats' in result:
                self.player_stats_data.extend(result['player_stats'])

        # Save matches
        if self.matches_data:
            df = pd.DataFrame(self.matches_data)
            filename = output_path / f'matches_intelligent_{timestamp}.csv'
            df.to_csv(filename, index=False)
            logger.info(f"✓ Saved {len(df)} matches to: {filename}")

        # Save team stats
        if self.team_stats_data:
            df = pd.DataFrame(self.team_stats_data)
            filename = output_path / f'team_stats_intelligent_{timestamp}.csv'
            df.to_csv(filename, index=False)
            logger.info(f"✓ Saved {len(df)} team stat records to: {filename}")

        # Save player stats
        if self.player_stats_data:
            df = pd.DataFrame(self.player_stats_data)
            filename = output_path / f'player_stats_intelligent_{timestamp}.csv'
            df.to_csv(filename, index=False)
            logger.info(f"✓ Saved {len(df)} player stat records to: {filename}")

        # Save agent logs
        if self.agent_logs:
            import json
            log_filename = output_path / f'agent_decisions_{timestamp}.json'
            with open(log_filename, 'w') as f:
                json.dump(self.agent_logs, f, indent=2)
            logger.info(f"✓ Saved agent decision log to: {log_filename}")
