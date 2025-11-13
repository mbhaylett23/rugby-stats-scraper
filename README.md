# Rugby Statistics Scraper 🏉🤖

An intelligent, AI-powered web scraper for collecting comprehensive international rugby match statistics from RugbyPass.

## Overview

This project uses **Gemini AI** as an intelligent agent to plan, validate, and self-correct during web scraping. Unlike traditional scrapers that blindly follow rules, this scraper uses LLM reasoning to:
- 🧠 Understand what data to find and how to find it
- ✅ Validate that scraped data is correct
- 🔧 Self-heal when errors occur
- 🎯 Adapt to website changes automatically

**Data Source:** [RugbyPass](https://www.rugbypass.com/) - Comprehensive match statistics for Tier 1 international rugby nations

## 🧠 How It Works

This is a **hybrid approach** combining the best of both worlds:
- **Selenium** does the heavy lifting (browser automation, page loading, data extraction)
- **Gemini AI** provides intelligence (planning, validation, correction)

**Key Capabilities:**
- ✅ Plans how to find each match using AI reasoning
- ✅ Validates extracted data for correctness
- ✅ Self-corrects when errors occur
- ✅ Adapts to website changes automatically
- ✅ Learns from failures and tries alternatives

## 🤖 Agent Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                  INTELLIGENT AGENT WORKFLOW                  │
└─────────────────────────────────────────────────────────────┘

PHASE 1: PLANNING (LLM)
├─ Analyze match details
├─ Decide URL strategy
├─ Handle team name variations
└─ Create scraping plan

PHASE 2: SCRAPING (Selenium)
├─ Execute the plan
├─ Load match page
├─ Extract statistics
└─ Capture page content

PHASE 3: VALIDATION (LLM)
├─ Check data correctness
├─ Verify team names
├─ Validate statistics logic
├─ Identify missing data
└─ Assess confidence level

PHASE 4: DECISION (LLM)
├─ Evaluate validation results
├─ Decide: ACCEPT, RETRY, or REJECT
└─ Provide reasoning

PHASE 5: CORRECTION (LLM) [if RETRY]
├─ Analyze what went wrong
├─ Suggest alternative URLs
├─ Adjust team names
└─ Create new plan

→ Loop back to PHASE 1 (max 3 attempts)
```

## 🎯 Key Advantages

### 1. **Handles URL Variations**
**Problem**: Game IDs change, URLs vary
**Solution**: LLM intelligently constructs and tests URLs

### 2. **Adapts to HTML Changes**
**Problem**: RugbyPass updates their website
**Solution**: LLM understands context, not just patterns

### 3. **Self-Validates Data**
**Problem**: Scraped data might be wrong
**Solution**: LLM checks if statistics make sense

### 4. **Self-Corrects Errors**
**Problem**: First attempt fails
**Solution**: LLM suggests fixes and retries automatically

### 5. **Handles Team Name Variations**
**Problem**: "New Zealand" vs "All Blacks" vs "NZ"
**Solution**: LLM understands equivalences

## 🚀 Quick Start

### Prerequisites

```bash
pip install selenium beautifulsoup4 pandas google-generativeai webdriver-manager
```

### Get Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Set as environment variable:

```bash
export GEMINI_API_KEY='your-key-here'
```

Or use OpenAI API key (if you have Gemini access through OpenAI):
```bash
export OPENAI_API_KEY='your-key-here'
```

### Run the Scraper

```bash
python intelligent_agent_scraper.py
```

## 📊 Example Agent Workflow

### Match: France vs Wales (2025-01-31)

```
PHASE 1: PLANNING
  Strategy: direct_url
  URL to try: https://www.rugbypass.com/live/france-vs-wales/stats/?g=944287
  Reasoning: Game ID provided, use direct URL

PHASE 2: SCRAPING
  Loading: https://www.rugbypass.com/live/france-vs-wales/stats/?g=944287
  ✓ Found game_id: 944287
  ✓ Extracted 11 statistics

PHASE 3: VALIDATING
  Valid: true
  Confidence: 95%
  Assessment: Data looks correct, all key stats present

PHASE 4: DECIDING
  Decision: ACCEPT
  Reason: High confidence, no significant issues

✓ Successfully scraped match!
```

### Match with Issues: Scotland vs Italy (wrong URL)

```
PHASE 1: PLANNING
  Strategy: construct_url
  URL to try: https://www.rugbypass.com/live/scotland-vs-italy/stats/?g=944288
  Reasoning: Constructing URL from team names

PHASE 2: SCRAPING
  Loading: https://www.rugbypass.com/live/scotland-vs-italy/stats/?g=944288
  ✓ Found game_id: 944288
  ✓ Extracted 8 statistics

PHASE 3: VALIDATING
  Valid: false
  Confidence: 45%
  Issues: ["Missing key statistics", "Suspicious possession values"]
  Assessment: Data incomplete, likely wrong page

PHASE 4: DECIDING
  Decision: RETRY
  Reason: Low confidence, fixable issues
  Suggested fixes: ["Try alternative URL", "Check team name spelling"]

PHASE 5: CORRECTING
  Corrections: Try "scotland-vs-italia" (Italian spelling)
  Updated URL: https://www.rugbypass.com/live/scotland-vs-italia/stats/?g=944288

--- Attempt 2/3 ---

PHASE 1: PLANNING
  Strategy: direct_url
  URL to try: https://www.rugbypass.com/live/scotland-vs-italia/stats/?g=944288
  Reasoning: Using corrected team name

PHASE 2: SCRAPING
  ✓ Found game_id: 944288
  ✓ Extracted 11 statistics

PHASE 3: VALIDATING
  Valid: true
  Confidence: 90%
  Assessment: Data now complete and correct

PHASE 4: DECIDING
  Decision: ACCEPT
  Reason: High confidence after correction

✓ Successfully scraped match on attempt 2!
```

## 📁 Output Files

### Standard CSV Files
1. **`matches_intelligent_TIMESTAMP.csv`** - Match information
2. **`team_stats_intelligent_TIMESTAMP.csv`** - Team statistics
3. **`player_stats_intelligent_TIMESTAMP.csv`** - Player statistics

### Agent Decision Log
4. **`agent_decisions_TIMESTAMP.json`** - Complete log of all agent decisions

Example agent log:
```json
[
  {
    "phase": "PLAN",
    "attempt": 1,
    "plan": {
      "strategy": "direct_url",
      "url_to_try": "https://...",
      "reasoning": "Game ID provided"
    }
  },
  {
    "phase": "VALIDATE",
    "validation": {
      "is_valid": true,
      "confidence": 95,
      "issues": [],
      "overall_assessment": "Data looks correct"
    }
  },
  {
    "phase": "DECIDE",
    "decision": {
      "action": "ACCEPT",
      "reason": "High confidence"
    }
  }
]
```

## 💡 Use Cases

### 1. **Scraping Without Game IDs**
Just provide team names and date:
```json
{
  "date": "2025-02-01",
  "home": "Scotland",
  "away": "Italy",
  "competition": "Six Nations"
}
```
Agent will figure out the URL!

### 2. **Handling Team Name Variations**
```json
{
  "home": "All Blacks",  // Agent knows this is New Zealand
  "away": "Springboks"   // Agent knows this is South Africa
}
```

### 3. **Recovering from Failures**
If first URL fails, agent automatically:
- Tries alternative team name spellings
- Searches for the match
- Adjusts URL patterns

### 4. **Validating Historical Data**
Agent checks if scraped data makes sense:
- Tries ≤ total score
- Possession adds to ~100%
- Tackles made > tackles missed (usually)

## ⚙️ Configuration

### Adjust Retry Attempts

In `intelligent_agent_scraper.py`:
```python
max_retries = 3  # Change to 5 for more attempts
```

### Adjust Validation Threshold

In `_phase_4_decide()`:
```python
# Current: ACCEPT if confidence ≥ 80
# Change to: ACCEPT if confidence ≥ 70 (more lenient)
```

### Use Different LLM Model

```python
self.model = genai.GenerativeModel('gemini-pro')  # Different model
```

## 💰 Cost Analysis

### Per Match
- **API calls**: 3-5 per match (Plan, Validate, Decide, possibly Correct)
- **Cost**: ~$0.001-0.005 per match (Gemini Flash is very cheap)
- **Time**: +5-10 seconds per match (LLM overhead)

### For 15 Six Nations Matches
- **Total API calls**: ~45-75
- **Total cost**: ~$0.015-0.075 (less than 10 cents!)
- **Total time**: ~5-10 minutes (vs 2-3 minutes for basic scraper)

### For 400 Historical Matches (5 years)
- **Total cost**: ~$0.40-2.00
- **Time saved from debugging**: Hours!

## 🎓 When to Use Intelligent Agent vs Basic Scraper

### Use **Intelligent Agent** When:
✅ You don't have game IDs
✅ Scraping historical matches with unknown URLs
✅ Website structure changes frequently
✅ You need high data quality assurance
✅ You want self-healing capabilities

### Use **Basic Scraper** When:
✅ You have all game IDs and URLs
✅ Scraping recent matches with known structure
✅ You want maximum speed
✅ You want to minimize API costs
✅ You're comfortable debugging manually

## 🔧 Troubleshooting

### API Key Issues
```bash
# Check if key is set
echo $GEMINI_API_KEY

# Set temporarily
export GEMINI_API_KEY='your-key-here'

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
```

### Agent Always Rejects Data
- Check `agent_decisions_TIMESTAMP.json` for reasons
- Lower confidence threshold in code
- Verify match details are correct

### Agent Takes Too Long
- Reduce `max_retries` from 3 to 2
- Use faster LLM model (gemini-flash)
- Increase validation confidence threshold

## 📈 Advanced Features

### Custom Validation Rules

Add your own validation logic:
```python
def _phase_3_validate(self, match_info, scraped_data):
    # ... existing code ...
    
    # Add custom check
    if scraped_data['team_stats'][0]['tries'] > 10:
        validation['issues'].append("Unusually high tries count")
        validation['confidence'] -= 10
    
    return validation
```

### Multi-Source Validation

Validate against multiple sources:
```python
def _phase_3_validate_multi_source(self, match_info, scraped_data):
    # Scrape from ESPN too
    espn_data = self.scrape_espn(match_info)
    
    # Compare with RugbyPass data
    if scraped_data['score'] != espn_data['score']:
        validation['issues'].append("Score mismatch with ESPN")
```

## 🎉 Benefits Summary

| Feature | Basic Scraper | Intelligent Agent |
|---------|--------------|-------------------|
| **Speed** | ⚡⚡⚡ Fast | ⚡⚡ Moderate |
| **Robustness** | ⭐⭐ Fragile | ⭐⭐⭐ Robust |
| **Self-Healing** | ❌ No | ✅ Yes |
| **URL Discovery** | ❌ Manual | ✅ Automatic |
| **Data Validation** | ❌ None | ✅ Comprehensive |
| **Adaptability** | ❌ Fixed rules | ✅ AI-powered |
| **Cost** | 💰 Free | 💰 ~$0.001/match |
| **Setup** | ✅ Simple | ⚙️ Needs API key |

## 🚀 Next Steps

1. **Test with sample matches**
   ```bash
   python intelligent_agent_scraper.py
   ```

2. **Review agent decisions**
   ```bash
   cat agent_decisions_TIMESTAMP.json | jq
   ```

3. **Analyze results**
   ```python
   import pandas as pd
   df = pd.read_csv('matches_intelligent_TIMESTAMP.csv')
   print(df.head())
   ```

4. **Scale to more matches**
   - Add more matches to `matches_to_scrape.json`
   - Let the agent handle URL discovery automatically

## 📝 Example: Scraping Without Game IDs

Create `matches_unknown_ids.json`:
```json
[
  {
    "date": "2025-02-01",
    "home": "Scotland",
    "away": "Italy",
    "competition": "Six Nations"
  },
  {
    "date": "2025-02-01",
    "home": "Ireland",
    "away": "England",
    "competition": "Six Nations"
  }
]
```

Run:
```bash
python intelligent_agent_scraper.py
```

The agent will:
1. **Plan**: Construct likely URLs
2. **Scrape**: Try each URL
3. **Validate**: Check if data matches expected match
4. **Decide**: Accept if correct, retry if wrong
5. **Correct**: Try alternative URLs if needed

**No manual URL finding required!** 🎉

---

## 🤖 The Future of Web Scraping

This intelligent agent approach represents the future of web scraping:

- **Less brittle**: Adapts to changes automatically
- **More intelligent**: Understands context, not just patterns
- **Self-healing**: Fixes issues without human intervention
- **Scalable**: Can handle thousands of matches with minimal supervision

**The small API cost is worth the massive time savings in maintenance and debugging!**

---

**Ready to scrape intelligently! 🏉🤖📊**

*Created November 2025 - The next generation of rugby statistics collection*
