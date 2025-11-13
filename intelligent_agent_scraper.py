#!/usr/bin/env python3
"""
Intelligent Rugby Statistics Scraper with LLM Agent Workflow
============================================================

An advanced scraper that uses Gemini AI as an intelligent agent to:
1. Plan how to find and scrape matches
2. Validate extracted data
3. Self-correct when errors occur
4. Adapt to website changes

This creates a robust, self-healing scraper that can handle variations
in URLs, HTML structure, and data formats.

Author: Created for rugby statistics analysis
Version: 2.0 (Intelligent Agent)
Date: November 2025

Requirements:
    pip install selenium beautifulsoup4 pandas google-generativeai

Usage:
    python intelligent_agent_scraper.py
"""

import time
import re
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('intelligent_scraping_log.txt'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RugbyScraperAgent:
    """
    Intelligent agent that uses LLM to plan, scrape, validate, and self-correct.
    
    Workflow:
    1. PLAN: LLM decides how to find the match
    2. SCRAPE: Execute the plan using Selenium
    3. VALIDATE: LLM checks if data is correct
    4. DECIDE: LLM decides to accept, retry, or try alternative
    5. CORRECT: LLM suggests fixes and retries
    """
    
    def __init__(self, gemini_api_key: str, headless: bool = False):
        """
        Initialize the intelligent scraper agent.
        
        Args:
            gemini_api_key: Google Gemini API key
            headless: Run browser in headless mode
        """
        logger.info("Initializing Intelligent Rugby Scraper Agent...")
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        logger.info("✓ Gemini AI configured")
        
        # Setup Selenium
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("✓ Selenium WebDriver initialized")
        
        self.matches_data = []
        self.team_stats_data = []
        self.player_stats_data = []
        
        # Track agent decisions
        self.agent_log = []
    
    def scrape_match_intelligently(
        self,
        home_team: str,
        away_team: str,
        match_date: str,
        competition: str,
        game_id: Optional[str] = None,
        url: Optional[str] = None
    ) -> Dict:
        """
        Main agent workflow: Plan → Scrape → Validate → Decide → Correct
        
        Args:
            home_team: Home team name
            away_team: Away team name
            match_date: Match date (YYYY-MM-DD)
            competition: Competition name
            game_id: Optional game ID if known
            url: Optional URL if known
            
        Returns:
            Dictionary with match data and agent decisions
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"AGENT WORKFLOW: {home_team} vs {away_team} ({match_date})")
        logger.info(f"{'='*80}\n")
        
        match_info = {
            'home': home_team,
            'away': away_team,
            'date': match_date,
            'competition': competition,
            'game_id': game_id,
            'url': url
        }
        
        max_retries = 3
        attempt = 0
        
        while attempt < max_retries:
            attempt += 1
            logger.info(f"\n--- Attempt {attempt}/{max_retries} ---")
            
            # PHASE 1: PLAN
            plan = self._phase_1_plan(match_info, attempt)
            
            # PHASE 2: SCRAPE
            scraped_data = self._phase_2_scrape(plan)
            
            if not scraped_data['success']:
                logger.warning(f"Scraping failed: {scraped_data.get('error')}")
                continue
            
            # PHASE 3: VALIDATE
            validation = self._phase_3_validate(match_info, scraped_data)
            
            # PHASE 4: DECIDE
            decision = self._phase_4_decide(validation)
            
            if decision['action'] == 'ACCEPT':
                logger.info("✓ Agent decision: ACCEPT - Data is valid!")
                return {
                    'success': True,
                    'match_info': scraped_data['match_info'],
                    'team_stats': scraped_data['team_stats'],
                    'player_stats': scraped_data['player_stats'],
                    'agent_log': self.agent_log
                }
            
            elif decision['action'] == 'RETRY':
                logger.info(f"⟳ Agent decision: RETRY - {decision['reason']}")
                # PHASE 5: CORRECT
                match_info = self._phase_5_correct(match_info, decision, validation)
                time.sleep(2)
                continue
            
            elif decision['action'] == 'REJECT':
                logger.error(f"✗ Agent decision: REJECT - {decision['reason']}")
                break
        
        # Failed after all retries
        return {
            'success': False,
            'error': 'Failed after maximum retries',
            'agent_log': self.agent_log
        }
    
    def _phase_1_plan(self, match_info: Dict, attempt: int) -> Dict:
        """
        PHASE 1: LLM creates a plan for finding and scraping the match.
        """
        logger.info("PHASE 1: PLANNING")
        
        prompt = f"""
You are an intelligent web scraping agent for rugby statistics.

TASK: Create a plan to find and scrape this match from RugbyPass.com

MATCH DETAILS:
- Home: {match_info['home']}
- Away: {match_info['away']}
- Date: {match_info['date']}
- Competition: {match_info['competition']}
- Known game_id: {match_info.get('game_id', 'Unknown')}
- Known URL: {match_info.get('url', 'Unknown')}

ATTEMPT: {attempt} of 3

INSTRUCTIONS:
1. If game_id or URL is known, use it directly
2. If not, suggest how to construct the URL
3. Consider team name variations (e.g., "New Zealand" = "All Blacks")
4. RugbyPass URL pattern: /live/{{home-team}}-vs-{{away-team}}/stats/?g={{game_id}}
5. Teams in URL are lowercase with hyphens

OUTPUT FORMAT (JSON):
{{
  "strategy": "direct_url" or "construct_url" or "search_required",
  "url_to_try": "full URL to attempt",
  "reasoning": "why this approach",
  "team_name_adjustments": {{"home": "adjusted name", "away": "adjusted name"}}
}}

Return ONLY valid JSON, no other text.
"""
        
        response = self.model.generate_content(prompt)
        plan = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        logger.info(f"  Strategy: {plan['strategy']}")
        logger.info(f"  URL to try: {plan['url_to_try']}")
        logger.info(f"  Reasoning: {plan['reasoning']}")
        
        self.agent_log.append({
            'phase': 'PLAN',
            'attempt': attempt,
            'plan': plan
        })
        
        return plan
    
    def _phase_2_scrape(self, plan: Dict) -> Dict:
        """
        PHASE 2: Execute the scraping plan using Selenium.
        """
        logger.info("PHASE 2: SCRAPING")
        
        try:
            url = plan['url_to_try']
            logger.info(f"  Loading: {url}")
            
            self.driver.get(url)
            time.sleep(4)
            
            # Get page content
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            page_text = soup.get_text()
            
            # Extract game_id from current URL
            current_url = self.driver.current_url
            game_id_match = re.search(r'\?g=(\d+)', current_url)
            game_id = game_id_match.group(1) if game_id_match else None
            
            if not game_id:
                return {
                    'success': False,
                    'error': 'Could not find game_id in URL'
                }
            
            logger.info(f"  ✓ Found game_id: {game_id}")
            
            # Extract statistics using regex (fast method)
            match_info, team_stats = self._extract_stats_regex(
                soup, page_text, game_id
            )
            
            # Extract player stats (basic)
            player_stats = []
            
            return {
                'success': True,
                'match_info': match_info,
                'team_stats': team_stats,
                'player_stats': player_stats,
                'page_text_sample': page_text[:2000],
                'url': current_url
            }
            
        except Exception as e:
            logger.error(f"  ✗ Scraping error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_stats_regex(self, soup, page_text: str, game_id: str) -> Tuple[Dict, List[Dict]]:
        """Extract statistics using regex patterns (fast method)."""
        
        # Extract basic match info
        match_info = {
            'game_id': game_id,
            'url': self.driver.current_url
        }
        
        # Extract team stats
        stat_patterns = {
            'tries': r'(\d+)\s+Tries\s+(\d+)',
            'conversions': r'(\d+)\s+Conversions?\s+(\d+)',
            'penalty_goals': r'(\d+)\s+Penalty Goals?\s+(\d+)',
            'drop_goals': r'(\d+)\s+Drop Goals?\s+(\d+)',
            'possession_pct': r'(\d+)%?\s+Possession\s+(\d+)%?',
            'carries': r'(\d+)\s+Carries\s+(\d+)',
            'line_breaks': r'(\d+)\s+Line Breaks?\s+(\d+)',
            'tackles_made': r'(\d+)\s+Tackles Made\s+(\d+)',
            'tackles_missed': r'(\d+)\s+Tackles Missed\s+(\d+)',
            'turnovers_won': r'(\d+)\s+Turnovers? Won\s+(\d+)',
            'turnovers_lost': r'(\d+)\s+Turnovers? Lost\s+(\d+)',
        }
        
        home_stats = {'game_id': game_id, 'team': 'home'}
        away_stats = {'game_id': game_id, 'team': 'away'}
        
        for stat_name, pattern in stat_patterns.items():
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                home_stats[stat_name] = int(match.group(1))
                away_stats[stat_name] = int(match.group(2))
            else:
                home_stats[stat_name] = None
                away_stats[stat_name] = None
        
        return match_info, [home_stats, away_stats]
    
    def _phase_3_validate(self, match_info: Dict, scraped_data: Dict) -> Dict:
        """
        PHASE 3: LLM validates the scraped data for correctness.
        """
        logger.info("PHASE 3: VALIDATING")
        
        prompt = f"""
You are a data validation agent for rugby statistics.

TASK: Validate if the scraped data is correct and complete.

EXPECTED MATCH:
- Home: {match_info['home']}
- Away: {match_info['away']}
- Date: {match_info['date']}
- Competition: {match_info['competition']}

SCRAPED DATA:
{json.dumps(scraped_data['team_stats'], indent=2)}

PAGE SAMPLE:
{scraped_data.get('page_text_sample', '')[:1000]}

VALIDATION CHECKS:
1. Are the team names correct?
2. Do the statistics make sense? (e.g., tries ≤ total score)
3. Are key statistics present? (tries, possession, tackles)
4. Are there any obvious errors or missing data?
5. Does the page content match the expected match?

OUTPUT FORMAT (JSON):
{{
  "is_valid": true/false,
  "confidence": 0-100,
  "issues": ["list of issues found"],
  "missing_stats": ["list of missing important stats"],
  "suspicious_values": ["list of suspicious values"],
  "overall_assessment": "brief assessment"
}}

Return ONLY valid JSON, no other text.
"""
        
        response = self.model.generate_content(prompt)
        validation = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        logger.info(f"  Valid: {validation['is_valid']}")
        logger.info(f"  Confidence: {validation['confidence']}%")
        logger.info(f"  Assessment: {validation['overall_assessment']}")
        
        if validation['issues']:
            logger.warning(f"  Issues: {', '.join(validation['issues'])}")
        
        self.agent_log.append({
            'phase': 'VALIDATE',
            'validation': validation
        })
        
        return validation
    
    def _phase_4_decide(self, validation: Dict) -> Dict:
        """
        PHASE 4: LLM decides whether to accept, retry, or reject the data.
        """
        logger.info("PHASE 4: DECIDING")
        
        prompt = f"""
You are a decision-making agent for web scraping.

TASK: Decide what to do based on the validation results.

VALIDATION RESULTS:
{json.dumps(validation, indent=2)}

DECISION OPTIONS:
1. ACCEPT - Data is good enough, save it
2. RETRY - Try again with corrections
3. REJECT - Data is unusable, give up

DECISION CRITERIA:
- ACCEPT if: is_valid=true OR confidence≥80 with minor issues
- RETRY if: confidence 40-79 OR fixable issues identified
- REJECT if: confidence<40 OR unfixable issues

OUTPUT FORMAT (JSON):
{{
  "action": "ACCEPT" or "RETRY" or "REJECT",
  "reason": "explanation for decision",
  "suggested_fixes": ["list of fixes to try if RETRY"]
}}

Return ONLY valid JSON, no other text.
"""
        
        response = self.model.generate_content(prompt)
        decision = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        logger.info(f"  Decision: {decision['action']}")
        logger.info(f"  Reason: {decision['reason']}")
        
        self.agent_log.append({
            'phase': 'DECIDE',
            'decision': decision
        })
        
        return decision
    
    def _phase_5_correct(self, match_info: Dict, decision: Dict, validation: Dict) -> Dict:
        """
        PHASE 5: LLM suggests corrections and updates the match info for retry.
        """
        logger.info("PHASE 5: CORRECTING")
        
        prompt = f"""
You are a problem-solving agent for web scraping.

TASK: Suggest corrections to fix the scraping issues.

CURRENT MATCH INFO:
{json.dumps(match_info, indent=2)}

VALIDATION ISSUES:
{json.dumps(validation.get('issues', []), indent=2)}

SUGGESTED FIXES:
{json.dumps(decision.get('suggested_fixes', []), indent=2)}

INSTRUCTIONS:
1. Suggest alternative URLs to try
2. Suggest team name variations
3. Suggest different search strategies

OUTPUT FORMAT (JSON):
{{
  "updated_match_info": {{
    "home": "corrected home team",
    "away": "corrected away team",
    "url": "alternative URL to try",
    "game_id": "alternative game_id if known"
  }},
  "reasoning": "why these corrections"
}}

Return ONLY valid JSON, no other text.
"""
        
        response = self.model.generate_content(prompt)
        correction = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        logger.info(f"  Corrections: {correction['reasoning']}")
        
        # Update match info with corrections
        updated_info = match_info.copy()
        updated_info.update(correction['updated_match_info'])
        
        self.agent_log.append({
            'phase': 'CORRECT',
            'correction': correction
        })
        
        return updated_info
    
    def scrape_matches_from_file(self, json_file: str):
        """
        Scrape all matches from a JSON file using intelligent agent workflow.
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"INTELLIGENT AGENT SCRAPING SESSION")
        logger.info(f"{'='*80}\n")
        logger.info(f"Loading matches from: {json_file}")
        
        with open(json_file, 'r') as f:
            matches = json.load(f)
        
        logger.info(f"Found {len(matches)} matches to scrape\n")
        
        for i, match in enumerate(matches, 1):
            logger.info(f"\n{'#'*80}")
            logger.info(f"MATCH {i}/{len(matches)}")
            logger.info(f"{'#'*80}")
            
            # Extract game_id from URL if present
            game_id = None
            if 'url' in match:
                game_id_match = re.search(r'\?g=(\d+)', match['url'])
                if game_id_match:
                    game_id = game_id_match.group(1)
            elif 'game_id' in match:
                game_id = match['game_id']
            
            # Run intelligent scraping
            result = self.scrape_match_intelligently(
                home_team=match['home'],
                away_team=match['away'],
                match_date=match['date'],
                competition=match.get('competition', 'Unknown'),
                game_id=game_id,
                url=match.get('url')
            )
            
            if result['success']:
                self.matches_data.append(result['match_info'])
                self.team_stats_data.extend(result['team_stats'])
                self.player_stats_data.extend(result['player_stats'])
                logger.info(f"\n✓ Successfully scraped match {i}")
            else:
                logger.error(f"\n✗ Failed to scrape match {i}: {result.get('error')}")
            
            # Be polite to the server
            time.sleep(3)
    
    def save_to_csv(self, output_dir: str = '.'):
        """Save all collected data to CSV files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        logger.info(f"\n{'='*80}")
        logger.info("SAVING RESULTS")
        logger.info(f"{'='*80}\n")
        
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
        
        # Save agent log
        log_filename = output_path / f'agent_decisions_{timestamp}.json'
        with open(log_filename, 'w') as f:
            json.dump(self.agent_log, f, indent=2)
        logger.info(f"✓ Saved agent decision log to: {log_filename}")
    
    def close(self):
        """Close the browser."""
        try:
            self.driver.quit()
            logger.info("\n✓ Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("INTELLIGENT RUGBY STATISTICS SCRAPER WITH LLM AGENT")
    print("="*80)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get Gemini API key
    import os
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("ERROR: No API key found!")
        print("Please set GEMINI_API_KEY or OPENAI_API_KEY environment variable")
        print("\nExample:")
        print("  export GEMINI_API_KEY='your-key-here'")
        print("  python intelligent_agent_scraper.py")
        return
    
    # Initialize agent
    agent = RugbyScraperAgent(gemini_api_key=api_key, headless=False)
    
    try:
        # Check for matches file
        matches_file = 'matches_to_scrape.json'
        
        if Path(matches_file).exists():
            agent.scrape_matches_from_file(matches_file)
        else:
            logger.error(f"Matches file not found: {matches_file}")
            logger.info("Please create a JSON file with match details")
            return
        
        # Save results
        agent.save_to_csv()
        
        print("\n" + "="*80)
        print("✓ INTELLIGENT SCRAPING COMPLETED")
        print("="*80)
        print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nCheck the output CSV files and agent_decisions.json for details")
        
    except KeyboardInterrupt:
        logger.info("\n\n✗ Scraping interrupted by user")
    except Exception as e:
        logger.error(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        agent.close()


if __name__ == '__main__':
    main()
