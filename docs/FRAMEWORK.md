# LLM-Assisted Web Scraping Framework

## Overview

This is a **generic, reusable framework** for building intelligent web scrapers powered by Large Language Models (LLMs). The framework implements a 5-phase workflow that uses AI to make scraping more robust, adaptive, and self-healing.

## Architecture

### Core Components

```
llm_scraper/                    # Generic Framework
├── core/
│   ├── base_scraper.py        # Abstract base class for all scrapers
│   ├── llm_agent.py           # LLM interaction & decision-making
│   ├── phases.py              # 5-phase workflow execution
│   └── config.py              # Configuration management
├── utils/
│   ├── browser.py             # Selenium/browser utilities
│   ├── extractors.py          # Data extraction helpers
│   └── validators.py          # Data validation helpers
└── models/
    └── schemas.py             # Data models (Plan, ScrapedData, etc.)
```

### The 5-Phase Workflow

Every scraper built with this framework follows this workflow:

```
┌─────────────────────────────────────────────────────────────┐
│                     INTELLIGENT WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

PHASE 1: PLAN (LLM)
├─ Analyze target information
├─ Decide URL strategy
├─ Handle name variations
└─ Create scraping plan

PHASE 2: SCRAPE (Selenium)
├─ Execute the plan
├─ Load target page
├─ Extract data
└─ Capture page content

PHASE 3: VALIDATE (LLM)
├─ Check data correctness
├─ Verify completeness
├─ Validate logic
├─ Identify issues
└─ Assess confidence level

PHASE 4: DECIDE (LLM)
├─ Evaluate validation results
├─ Decide: ACCEPT, RETRY, or REJECT
└─ Provide reasoning

PHASE 5: CORRECT (LLM) [if RETRY]
├─ Analyze what went wrong
├─ Suggest alternative URLs
├─ Adjust parameters
└─ Create new plan

→ Loop back to PHASE 1 (max retries)
```

## Creating a New Scraper

### Step 1: Extend `BaseLLMScraper`

```python
from llm_scraper.core.base_scraper import BaseLLMScraper
from llm_scraper.core.config import ScraperConfig
from llm_scraper.models.schemas import ScrapingPlan, ScrapedData

class MyDomainScraper(BaseLLMScraper):
    """Scraper for my specific domain."""

    def __init__(self, config: ScraperConfig):
        super().__init__(config)
        # Initialize domain-specific components
```

### Step 2: Implement Required Abstract Methods

#### A. `get_planning_prompt()` - How to find content

```python
def get_planning_prompt(self) -> str:
    """Instructions for the LLM on how to find your target content."""
    return """
TASK: Create a plan to scrape [YOUR CONTENT TYPE] from [WEBSITE]

INSTRUCTIONS:
1. If URL is known, use it directly
2. If not, construct URL from available information
3. Consider variations in [relevant parameters]
4. URL pattern: [describe pattern]

STRATEGY OPTIONS:
- "direct_url": Known URL available
- "construct_url": Build URL from components
- "search_required": Need to search first
"""
```

#### B. `get_validation_prompt()` - What makes data valid

```python
def get_validation_prompt(self) -> str:
    """Instructions for the LLM on validating extracted data."""
    return """
TASK: Validate if the scraped [CONTENT TYPE] is correct and complete.

VALIDATION CHECKS:
1. [Domain-specific check 1]
2. [Domain-specific check 2]
3. Required fields: [list required data]
4. Logic checks: [e.g., values in expected ranges]
5. Content verification: [e.g., right page loaded]

COMMON ISSUES:
- [Issue 1 and how to detect it]
- [Issue 2 and how to detect it]
"""
```

#### C. `execute_scraping()` - Extract the data

```python
def execute_scraping(self, plan: ScrapingPlan) -> ScrapedData:
    """Execute the scraping plan to extract data."""
    from llm_scraper.utils.browser import PageNavigator

    try:
        # Navigate to page
        navigator = PageNavigator(self.driver)
        navigator.load_page(plan.url_to_try)

        # Get page content
        soup = BeautifulSoup(navigator.get_page_source(), 'html.parser')
        page_text = soup.get_text()

        # Extract your data using your custom extractors
        extracted_data = self.extract_my_data(soup, page_text)

        return ScrapedData(
            success=True,
            url=navigator.get_current_url(),
            data=extracted_data,
            page_content_sample=page_text[:2000]
        )

    except Exception as e:
        return ScrapedData(success=False, error=str(e))
```

#### D. `save_results()` - Save extracted data

```python
def save_results(self, output_dir: Optional[str] = None) -> None:
    """Save scraped data to files."""
    import pandas as pd
    from pathlib import Path
    from datetime import datetime

    output_path = Path(output_dir or self.config.output_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save your data to CSV/JSON/etc
    df = pd.DataFrame(self.scraped_data)
    df.to_csv(output_path / f'results_{timestamp}.csv', index=False)
```

### Step 3: Create Domain-Specific Extractors

```python
# my_scraper/extractors.py

from llm_scraper.utils.extractors import BaseExtractor

class MyDataExtractor(BaseExtractor):
    """Extract specific data patterns from my domain."""

    def extract(self, soup, page_text, **kwargs):
        # Implement domain-specific extraction logic
        data = {}
        # ... extract data ...
        return data
```

### Step 4: Create Configuration

```yaml
# my_scraper/config.yml

llm_provider: "gemini"
llm_model: "gemini-2.0-flash-exp"
max_retries: 3
confidence_threshold: 80

custom_settings:
  base_url: "https://mywebsite.com"
  # Domain-specific settings
```

### Step 5: Create Main Script

```python
# run_my_scraper.py

from llm_scraper.core.config import ScraperConfig
from my_scraper import MyDomainScraper

def main():
    # Load config
    config = ScraperConfig.from_env()

    # Create scraper
    scraper = MyDomainScraper(config)

    # Scrape targets
    scraper.scrape_from_file('targets.json')

    # Save results
    scraper.save_results()

    # Cleanup
    scraper.close_browser()

if __name__ == '__main__':
    main()
```

## Usage Examples

### Basic Usage

```python
from llm_scraper.core.config import ScraperConfig
from my_scraper import MyDomainScraper

# Initialize
config = ScraperConfig.from_env()
scraper = MyDomainScraper(config)

# Scrape single target
result = scraper.scrape_target({
    'url': 'https://example.com/page',
    'type': 'product'
})

# Scrape multiple targets
results = scraper.scrape_from_file('targets.json')

# Save results
scraper.save_results()
scraper.close_browser()
```

### With Context Manager

```python
with MyDomainScraper(config) as scraper:
    results = scraper.scrape_from_file('targets.json')
    scraper.save_results()
# Browser automatically closed
```

### Advanced: Custom Decision Criteria

Override `get_decision_prompt()` for domain-specific decision logic:

```python
def get_decision_prompt(self) -> Optional[str]:
    return """
ADDITIONAL DECISION CRITERIA:
- For my domain, accept if confidence >= 70 (not 80)
- RETRY if specific field X is missing
- REJECT if page returns error code
"""
```

## Key Design Principles

### 1. **Separation of Concerns**
- **Framework** handles LLM interaction, workflow, retry logic
- **Domain implementation** handles data extraction, validation

### 2. **Extensibility**
- Abstract base classes for easy extension
- Override only what you need
- Add custom extractors, validators

### 3. **Configuration over Code**
- YAML-based configuration
- Environment variable support
- Command-line overrides

### 4. **Testability**
- Framework components can be tested independently
- Mock LLM responses for testing
- Validate extractors without browser

### 5. **Observability**
- Comprehensive logging
- Agent decision logs (JSON)
- Track LLM reasoning for each phase

## Utility Classes

### BrowserManager

```python
from llm_scraper.utils.browser import BrowserManager

manager = BrowserManager(headless=True, timeout=30)
driver = manager.get_driver()
```

### Extractors

```python
from llm_scraper.utils.extractors import (
    RegexExtractor,
    PairwiseStatExtractor,
    TableExtractor
)

# Regex extraction
extractor = RegexExtractor({
    'price': r'\$(\d+\.\d{2})',
    'name': r'Product:\s+(.+)'
})
data = extractor.extract(soup, page_text)

# Pairwise stats (Team A vs Team B)
extractor = PairwiseStatExtractor({
    'score': r'(\d+)\s+Score\s+(\d+)'
})
team_a, team_b = extractor.extract(soup, page_text)
```

### Validators

```python
from llm_scraper.utils.validators import (
    FieldPresenceValidator,
    NumericRangeValidator,
    CompositeValidator
)

# Check required fields
validator = FieldPresenceValidator(
    required_fields=['name', 'price', 'stock'],
    optional_fields=['description']
)

# Check numeric ranges
validator = NumericRangeValidator({
    'price': (0, 10000),
    'stock': (0, None)  # No maximum
})

# Combine validators
composite = CompositeValidator([validator1, validator2])
result = composite.validate(data)
```

## Real-World Example: Rugby Scraper

See `rugby_scraper/` for a complete implementation:

- `rugby_scraper/rugby_scraper.py` - Main scraper class
- `rugby_scraper/extractors.py` - Rugby-specific extractors
- `rugby_scraper/config.yml` - Configuration
- `run_rugby_scraper.py` - Entry point

This serves as a reference implementation showing all framework features.

## Best Practices

### 1. Design Clear Prompts
- Be specific about what you want the LLM to do
- Provide examples of good/bad outputs
- Include domain knowledge in prompts

### 2. Implement Robust Extractors
- Handle missing data gracefully
- Use multiple extraction strategies
- Validate extracted values

### 3. Configure Appropriately
- Set `confidence_threshold` based on your accuracy needs
- Adjust `max_retries` for difficult sites
- Use `headless=True` in production

### 4. Monitor Agent Decisions
- Review `agent_decisions_*.json` files
- Understand why the LLM made each decision
- Improve prompts based on patterns

### 5. Handle Errors
- Log all errors comprehensively
- Implement graceful degradation
- Don't trust scraped data blindly

## Performance Considerations

### LLM API Costs
- ~3-5 API calls per successful scrape
- ~$0.001-0.005 per target (Gemini Flash)
- Use faster/cheaper models for simple tasks

### Speed vs Reliability Tradeoff
- **Fast but fragile**: Traditional scrapers
- **Slower but robust**: LLM-assisted (this framework)
- Adds ~5-10 seconds overhead per target
- Worth it for difficult/changing websites

### Optimization Tips
- Use `headless=True` for faster browser operations
- Reduce `max_retries` if targets are reliable
- Increase `confidence_threshold` to reduce retries
- Batch targets to reuse browser sessions

## Extending the Framework

### Add New LLM Providers

```python
# In llm_agent.py
if provider == "openai":
    # Initialize OpenAI client
elif provider == "anthropic":
    # Initialize Claude client
```

### Add New Extraction Patterns

```python
# Create new extractor in utils/extractors.py
class JSONExtractor(BaseExtractor):
    """Extract JSON data from pages."""
    # Implement...
```

### Add New Validation Rules

```python
# Create new validator in utils/validators.py
class DateRangeValidator(BaseValidator):
    """Validate dates are in expected range."""
    # Implement...
```

## Troubleshooting

### LLM Returns Invalid JSON
- Check prompt clarity
- Add more examples in prompt
- Try different model (e.g., Opus for complex tasks)

### Low Validation Confidence
- Improve validation prompts
- Add more domain knowledge
- Check if data extraction is working

### Infinite Retry Loops
- Review agent decision logs
- Check correction prompts
- Ensure LLM has enough info to fix issues

### Browser Timeout Issues
- Increase `browser_timeout` in config
- Check network connection
- Use headless mode for stability

## Contributing

To add features to the framework:

1. Keep generic logic in `llm_scraper/`
2. Keep domain logic in domain-specific folders
3. Add tests for new components
4. Update this documentation

## License

[Your License Here]

---

**Built with ❤️ for intelligent web scraping**
