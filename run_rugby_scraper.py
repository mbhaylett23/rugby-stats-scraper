#!/usr/bin/env python3
"""
Main entry point for the Rugby Statistics Scraper.

Usage:
    python run_rugby_scraper.py
    python run_rugby_scraper.py --config rugby_scraper/config.yml
    python run_rugby_scraper.py --headless --max-retries 5
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from llm_scraper.core.config import ScraperConfig
from rugby_scraper import RugbyStatsScraper


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Intelligent Rugby Statistics Scraper powered by LLM'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to YAML configuration file'
    )
    parser.add_argument(
        '--matches-file',
        type=str,
        default='matches_to_scrape.json',
        help='Path to JSON file with matches to scrape (default: matches_to_scrape.json)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        help='Maximum retry attempts per match'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory for output files'
    )

    args = parser.parse_args()

    # Print header
    print("\n" + "="*80)
    print("INTELLIGENT RUGBY STATISTICS SCRAPER WITH LLM AGENT")
    print("="*80)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load configuration
    try:
        if args.config:
            print(f"Loading configuration from: {args.config}")
            config = ScraperConfig.from_yaml(args.config)
        else:
            print("Using environment-based configuration")
            config = ScraperConfig.from_env()

        # Override with command-line arguments
        if args.headless:
            config.headless_browser = True
        if args.max_retries:
            config.max_retries = args.max_retries
        if args.output_dir:
            config.output_dir = args.output_dir

        # Validate config
        config.validate()

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease set GEMINI_API_KEY or OPENAI_API_KEY environment variable")
        print("Or provide a configuration file with --config\n")
        print("Example:")
        print("  export GEMINI_API_KEY='your-key-here'")
        print("  python run_rugby_scraper.py\n")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\n❌ Configuration file not found: {args.config}\n")
        sys.exit(1)

    # Check matches file exists
    if not Path(args.matches_file).exists():
        print(f"\n❌ Matches file not found: {args.matches_file}")
        print("\nPlease create a JSON file with match details.")
        print("See matches_to_scrape.json for example format.\n")
        sys.exit(1)

    # Initialize scraper
    print(f"Initializing scraper...")
    scraper = RugbyStatsScraper(config)

    try:
        # Scrape matches
        print(f"\nLoading matches from: {args.matches_file}\n")
        scraper.scrape_from_file(
            file_path=args.matches_file,
            delay_between=3  # Be polite to the server
        )

        # Save results
        scraper.save_results()

        # Print summary
        print("\n" + "="*80)
        print("✓ INTELLIGENT SCRAPING COMPLETED")
        print("="*80)
        print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nResults saved to: {config.output_dir}")
        print("  - matches_intelligent_*.csv")
        print("  - team_stats_intelligent_*.csv")
        print("  - agent_decisions_*.json")
        print("\nCheck the agent_decisions file to see LLM reasoning for each match.\n")

    except KeyboardInterrupt:
        print("\n\n✗ Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        scraper.close_browser()


if __name__ == '__main__':
    main()
