# 🏉 Rugby Statistics Scraper + 🤖 Generic LLM Scraping Framework

**Two projects in one:**
1. **Generic LLM-Assisted Web Scraping Framework** - Reusable for any website/domain
2. **Rugby Statistics Scraper** - Complete implementation for RugbyPass data

---

## 🎯 Dual Purpose Project

### Purpose 1: Generic Framework
Build **any** intelligent web scraper by extending base classes. The framework handles:
- ✅ LLM-powered planning and decision-making
- ✅ Self-healing and retry logic
- ✅ Validation and quality assurance
- ✅ Flexible configuration and extension points

### Purpose 2: Rugby Stats Scraper
A **production-ready** scraper for international rugby match statistics:
- 🏉 Scrapes comprehensive match stats from RugbyPass
- 🤖 Uses AI to adapt to website changes
- 🔧 Self-corrects when errors occur
- 📊 Exports to CSV with full agent decision logs

---

## 🏗️ Project Structure

```
rugby-stats-scraper/
│
├── llm_scraper/                 # 🎯 GENERIC FRAMEWORK
│   ├── core/
│   │   ├── base_scraper.py     # Extend this for your domain
│   │   ├── llm_agent.py        # LLM interaction & reasoning
│   │   ├── phases.py           # 5-phase workflow
│   │   └── config.py           # Configuration management
│   ├── utils/
│   │   ├── browser.py          # Selenium utilities
│   │   ├── extractors.py       # Data extraction helpers
│   │   └── validators.py       # Validation helpers
│   └── models/
│       └── schemas.py          # Data models
│
├── rugby_scraper/               # 🏉 RUGBY IMPLEMENTATION
│   ├── rugby_scraper.py        # Extends BaseLLMScraper
│   ├── extractors.py           # Rugby-specific extraction
│   └── config.yml              # Rugby configuration
│
├── docs/
│   ├── FRAMEWORK.md            # How to build your own scraper
│   └── RUGBY_USAGE.md          # Rugby scraper usage
│
├── run_rugby_scraper.py        # Main entry point
├── matches_to_scrape.json      # Input data
├── requirements.txt
└── environment.yml
```

---

## 🚀 Quick Start (Rugby Scraper)

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/yourusername/rugby-stats-scraper.git
cd rugby-stats-scraper

# Create conda environment
conda env create -f environment.yml
conda activate rugby-scraper
```

### 2. Set API Key

```bash
# Get API key from https://aistudio.google.com/app/apikey

# On Linux/Mac:
export GEMINI_API_KEY='your-key-here'

# On Windows PowerShell:
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-key', 'User')
```

### 3. Run the Scraper

```bash
python run_rugby_scraper.py
```

That's it! The scraper will:
1. Load matches from `matches_to_scrape.json`
2. Use AI to find and validate each match
3. Save results to CSV files

---

## 🧠 The 5-Phase Intelligent Workflow

Every scrape follows this AI-powered workflow:

```
┌─────────────────────────────────────────────────────────────┐
│                  INTELLIGENT AGENT WORKFLOW                  │
└─────────────────────────────────────────────────────────────┘

PHASE 1: PLANNING (LLM)
├─ "How do I find this match?"
├─ Analyzes available information (teams, date, URL)
├─ Decides on URL strategy
└─ Creates scraping plan

PHASE 2: SCRAPING (Selenium)
├─ Executes the plan
├─ Loads match page with browser
├─ Extracts statistics using patterns
└─ Captures page content

PHASE 3: VALIDATING (LLM)
├─ "Is this data correct?"
├─ Checks team names match
├─ Validates statistics logic
├─ Identifies missing/suspicious data
└─ Assigns confidence score (0-100)

PHASE 4: DECIDING (LLM)
├─ Evaluates validation results
├─ Options: ACCEPT, RETRY, or REJECT
├─ Confidence ≥80 → ACCEPT
├─ Confidence 40-79 → RETRY
└─ Confidence <40 → REJECT

PHASE 5: CORRECTING (LLM) [if RETRY]
├─ "What went wrong and how to fix it?"
├─ Suggests alternative URLs
├─ Adjusts team name spellings
└─ Creates new plan → Back to PHASE 1
```

---

## 🎯 Why This Framework?

### Traditional Scrapers
```python
# Brittle, breaks when website changes
scraper.find_element_by_class('match-stats-2023')  # ❌ Class changed!
```

### LLM-Assisted Scraper (This Framework)
```python
# LLM understands context, adapts automatically
agent.validate_data()  # ✅ Detects wrong data, suggests fixes
```

### Key Advantages

| Feature | Traditional | LLM-Assisted |
|---------|------------|--------------|
| **Handles URL variations** | ❌ Fixed patterns | ✅ AI constructs URLs |
| **Adapts to HTML changes** | ❌ Breaks easily | ✅ Understands context |
| **Self-validates data** | ❌ No validation | ✅ Comprehensive checks |
| **Self-corrects errors** | ❌ Manual fixes | ✅ Auto-retry with fixes |
| **Handles name variations** | ❌ Exact matches only | ✅ Understands equivalences |
| **Cost** | Free | ~$0.001-0.005 per target |
| **Speed** | Fast | +5-10s overhead |

---

## 📊 Rugby Scraper Features

### Comprehensive Statistics
- **Scoring**: Tries, conversions, penalties, drop goals
- **Possession**: Possession %, territory %
- **Attack**: Carries, metres made, line breaks, defenders beaten
- **Defense**: Tackles made/missed, turnovers won/conceded
- **Set pieces**: Scrums won, lineouts won
- **Discipline**: Penalties conceded, cards

### Smart URL Discovery
Don't have game IDs? No problem!

```json
{
  "date": "2025-02-01",
  "home": "Scotland",
  "away": "Italy",
  "competition": "Six Nations"
}
```

The agent will:
1. Construct likely URLs
2. Try variations (scotland-vs-italy, scotland-vs-italia)
3. Validate the right match was found
4. Auto-correct if needed

### Output Files

```
matches_intelligent_20250213_143022.csv      # Match information
team_stats_intelligent_20250213_143022.csv   # Team statistics
agent_decisions_20250213_143022.json         # LLM reasoning log
```

**Agent log example:**
```json
{
  "phase": "VALIDATE",
  "validation": {
    "is_valid": true,
    "confidence": 95,
    "assessment": "All statistics present and logical"
  }
},
{
  "phase": "DECIDE",
  "decision": {
    "action": "ACCEPT",
    "reason": "High confidence, no significant issues"
  }
}
```

---

## 🛠️ Building Your Own Scraper

The framework is designed to be extended for **any website or domain**.

### 4 Simple Steps:

#### 1. Extend `BaseLLMScraper`
```python
from llm_scraper.core.base_scraper import BaseLLMScraper

class MyDomainScraper(BaseLLMScraper):
    pass  # Start here
```

#### 2. Implement 4 Abstract Methods
- `get_planning_prompt()` - How to find content
- `get_validation_prompt()` - What makes data valid
- `execute_scraping()` - Extract the data
- `save_results()` - Save the data

#### 3. Create Domain-Specific Extractors
```python
from llm_scraper.utils.extractors import RegexExtractor

extractor = RegexExtractor({
    'price': r'\$(\d+\.\d{2})',
    'rating': r'(\d+\.\d+)\s+stars'
})
```

#### 4. Run Your Scraper
```python
config = ScraperConfig.from_env()
scraper = MyDomainScraper(config)
scraper.scrape_from_file('targets.json')
scraper.save_results()
```

### Full Tutorial
See **[docs/FRAMEWORK.md](docs/FRAMEWORK.md)** for complete guide with examples.

---

## ⚙️ Configuration

### Environment Variables
```bash
export GEMINI_API_KEY='your-key'
export LLM_MODEL='gemini-2.0-flash-exp'
export MAX_RETRIES='3'
export HEADLESS='true'
```

### YAML Configuration
```yaml
# rugby_scraper/config.yml
llm_model: "gemini-2.0-flash-exp"
max_retries: 3
confidence_threshold: 80
headless_browser: false

custom_settings:
  base_url: "https://www.rugbypass.com"
  # Domain-specific settings
```

### Command Line
```bash
python run_rugby_scraper.py --headless --max-retries 5 --output-dir results/
```

---

## 💰 Cost Analysis

### Per Match (Rugby)
- **API calls**: 3-5 per match (Plan, Validate, Decide, maybe Correct)
- **Cost**: ~$0.001-0.005 per match (Gemini Flash)
- **Time**: +5-10 seconds LLM overhead

### For 15 Six Nations Matches
- **Total cost**: ~$0.015-0.075 (less than 10 cents!)
- **Time**: ~5-10 minutes total
- **Value**: Self-healing scraper that works even when website changes

### Worth It When:
✅ Website changes frequently
✅ Don't have all URLs/IDs
✅ Need high data quality
✅ Want to minimize maintenance
✅ Scraping 100s-1000s of targets

---

## 📈 Use Cases

### Rugby Scraper
- Historical match analysis
- Team performance tracking
- Player statistics aggregation
- Tournament analytics

### Framework (Build Your Own)
- **E-commerce**: Product prices, reviews, availability
- **News**: Article scraping with validation
- **Social Media**: Public post aggregation
- **Sports**: Any sports statistics (football, cricket, etc.)
- **Real Estate**: Listings with price/location data
- **Job Boards**: Job postings with details
- **Research**: Academic paper metadata

**Any website where structure might change or data needs validation.**

---

## 🧪 Example: Agent Self-Correction

```
Match: Scotland vs Italy (wrong URL initially)

ATTEMPT 1:
  Plan: Try https://rugbypass.com/.../scotland-vs-italy/...
  Scrape: ✓ Got data
  Validate: ❌ Confidence 45% - "Wrong team names detected"
  Decide: RETRY
  Correct: "Try 'italia' (Italian spelling)"

ATTEMPT 2:
  Plan: Try https://rugbypass.com/.../scotland-vs-italia/...
  Scrape: ✓ Got data
  Validate: ✓ Confidence 90% - "Data complete and correct"
  Decide: ACCEPT

✓ Successfully scraped on attempt 2!
```

---

## 🔧 Development

### Run Tests
```bash
pytest tests/
```

### Add New Extractor
```python
# rugby_scraper/extractors.py
class PlayerStatsExtractor:
    def extract(self, soup, page_text):
        # Implement extraction logic
        pass
```

### Improve Prompts
Edit prompts in `rugby_scraper/rugby_scraper.py`:
- `get_planning_prompt()`
- `get_validation_prompt()`
- `get_correction_prompt()`

---

## 📚 Documentation

- **[FRAMEWORK.md](docs/FRAMEWORK.md)** - Complete framework guide
- **[README.md](README.md)** - This file (getting started)
- **Code comments** - Comprehensive docstrings

---

## 🤝 Contributing

We welcome contributions!

### Add a New Domain Implementation
1. Create `my_domain_scraper/` directory
2. Extend `BaseLLMScraper`
3. Implement required methods
4. Add documentation
5. Submit PR

### Improve the Framework
1. New extractors/validators in `llm_scraper/utils/`
2. New LLM providers in `llm_scraper/core/llm_agent.py`
3. Enhanced error handling
4. Performance optimizations

---

## 🌟 Star Features

- **🧠 AI-Powered**: LLM makes intelligent decisions at every step
- **🔧 Self-Healing**: Auto-corrects errors, tries alternatives
- **🎯 Extensible**: Build your own scraper in <100 lines
- **📊 Observable**: Complete logs of LLM reasoning
- **⚙️ Configurable**: YAML, env vars, CLI options
- **🏗️ Production-Ready**: Error handling, logging, retry logic
- **📦 Batteries Included**: Extractors, validators, browser management

---

## 🎓 Learn More

### Understanding LLM-Assisted Scraping
1. Read [FRAMEWORK.md](docs/FRAMEWORK.md) - Comprehensive guide
2. Study `rugby_scraper/` - Reference implementation
3. Review `agent_decisions_*.json` - See LLM reasoning
4. Build your own - Start with a simple domain

### When to Use This vs Traditional Scraper
**Use LLM-assisted when:**
- Website structure changes frequently
- You need self-validation of data
- URLs/IDs are unknown or variable
- You want to minimize maintenance

**Use traditional when:**
- Website is stable and well-documented
- You need maximum speed (no LLM overhead)
- Working with APIs (not scraping HTML)
- Cost is a primary concern

---

## 📜 License

[Your License Here]

---

## 🙏 Acknowledgments

- Built with **Gemini AI** for intelligent decision-making
- Uses **Selenium** for browser automation
- Inspired by the need for more robust web scraping

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/rugby-stats-scraper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/rugby-stats-scraper/discussions)
- **Documentation**: [docs/](docs/)

---

**Built with ❤️ for intelligent web scraping**

*Create your own scraper in minutes, not days.*
