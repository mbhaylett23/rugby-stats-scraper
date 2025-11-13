# Rugby Statistics Project - Memory & Context

## 📌 Project Identity

**Project Name:** Rugby Statistics Collection & Analysis System  
**Created:** November 2025  
**Purpose:** Automated collection of comprehensive international rugby match statistics from RugbyPass for Tier 1 nations (2020-2025)  
**Current Status:** Production-ready scrapers deployed (basic + intelligent agent), actively collecting 2025 Six Nations data

**Version:** 2.0 (LLM Intelligence Agent Added)

---

## 🎯 Project Goals

### Primary Objectives

1. ✅ **Build automated web scraper** for RugbyPass match statistics
2. ✅ **Add AI-powered intelligent agent** with LLM validation and self-correction (NEW)
3. ⏳ **Collect 2025 data** - Six Nations, Rugby Championship, Autumn Nations Series (~50-60 matches)
4. ⏳ **Expand to 2020-2024** - Historical data collection (~400-600 matches)
5. ⏳ **Enable statistical analysis** - Correlations, trends, performance metrics
6. ⏳ **Support research/analysis** - Personal or academic rugby statistics research

### Success Metrics

- **Coverage:** 90%+ of Tier 1 international matches (2020-2025)
- **Completeness:** 85%+ of 90 statistical fields per match
- **Accuracy:** 99%+ data accuracy vs. source
- **Reliability:** Scraper success rate >95%
- **Adaptability:** Self-healing rate >80% for failed matches (NEW)

---

## 🏉 Domain Knowledge

### Tier 1 Nations (Target Teams)

- **Northern Hemisphere:** England, Ireland, Scotland, Wales, France, Italy
- **Southern Hemisphere:** New Zealand, South Africa, Australia, Argentina
- **Special:** Japan (emerging Tier 1)

### Key Competitions

1. **Six Nations** (Feb-Mar) - 6 teams, 15 matches annually
2. **Rugby Championship** (Jul-Sep) - 4 teams, 12 matches annually
3. **Autumn Nations Series** (Nov) - ~20-30 matches
4. **Summer Tours** (Jun-Jul) - Various bilateral series
5. **World Cup** (every 4 years) - 2023 was most recent

### Match Statistics Categories (90 fields)

- **Scoring:** Tries, conversions, penalty goals, drop goals
- **Possession & Territory:** Percentages by field zone, time-based
- **Set Pieces:** Scrums, lineouts, restarts (totals and success rates)
- **Attack:** Carries, line breaks, metres gained, passes, kicks
- **Defence:** Tackles (made/missed/dominant), turnovers
- **Breakdown:** Ruck speed distribution, rucks won
- **Discipline:** Penalties conceded, cards (yellow/red)
- **Performance:** Time in lead, 22m entries/conversions

---

## 🗂️ Current Data Structure

### File Organization

```
Rugby_stats/
├── Obtaining Rugby Statistics from the Past 5 Years/
│   └── rugby_scraper_package/
│       ├── rugbypass_scraper.py              # Basic scraper (500+ lines)
│       ├── intelligent_agent_scraper.py      # NEW: LLM agent scraper (645 lines)
│       ├── test_single_match.py              # Single match tester
│       ├── requirements.txt                   # Basic dependencies
│       ├── requirements_intelligent.txt       # NEW: LLM dependencies
│       ├── matches_to_scrape.json            # Match configurations
│       ├── README.md                          # Basic scraper docs
│       ├── README_INTELLIGENT_AGENT.md       # NEW: LLM agent docs
│       ├── COMPARISON_GUIDE.md                # NEW: Basic vs intelligent guide
│       ├── QUICKSTART.md                      # 5-minute setup guide
│       ├── DELIVERY_SUMMARY.md                # Project summary
│       ├── agents.md                          # AI agent definitions
│       └── memory.md                          # This file
```

### CSV Output Structure

1. **matches_{timestamp}.csv** (or matches_intelligent_{timestamp}.csv) - 10 fields per match
   - Primary key: `game_id`
   - Basic info: date, teams, scores, venue, competition, referee

2. **team_stats_{timestamp}.csv** (or team_stats_intelligent_{timestamp}.csv) - 90 fields per team per match
   - Foreign key: `game_id`
   - Comprehensive team-level statistics
   - Two rows per match (home/away)

3. **player_stats_{timestamp}.csv** (or player_stats_intelligent_{timestamp}.csv) - 8 fields per player
   - Foreign key: `game_id`
   - Individual player performance metrics
   - ~40-50 players per match

4. **agent_decisions_{timestamp}.json** (NEW - Intelligent Agent Only)
   - Complete log of LLM agent decisions
   - Phases: PLAN, SCRAPE, VALIDATE, DECIDE, CORRECT
   - Confidence scores, reasoning, retry attempts

---

## 🔧 Technical Stack

### Core Technologies

- **Python 3.8+** - Primary language
- **Selenium 4.x** - Browser automation for dynamic content
- **BeautifulSoup4** - HTML parsing and data extraction
- **Pandas** - Data manipulation and CSV export
- **webdriver-manager** - Automatic ChromeDriver management
- **lxml** - Fast HTML parsing backend
- **google-generativeai** - NEW: Gemini API for LLM agent

### Dependencies

**Basic Scraper:**
```python
selenium>=4.0.0
beautifulsoup4>=4.9.0
pandas>=1.3.0
webdriver-manager>=3.8.0
lxml>=4.6.0
```

**Intelligent Agent (Additional):**
```python
google-generativeai>=0.3.0  # For Gemini API
```

### Browser Requirements

- **Google Chrome** - Latest stable version
- **ChromeDriver** - Auto-managed by webdriver-manager

### API Requirements (NEW)

- **Gemini API Key** - Free tier available at https://aistudio.google.com/app/apikey
- **Environment Variable:** `GEMINI_API_KEY` or `OPENAI_API_KEY`
- **Model:** gemini-2.0-flash-exp (fast, cheap, powerful)
- **Cost:** ~$0.001-0.005 per match

---

## 📊 Data Sources

### Primary Source: RugbyPass.com

- **URL Pattern:** `https://www.rugbypass.com/live/{home}-vs-{away}/stats/?g={game_id}`
- **Data Type:** Comprehensive match statistics
- **Coverage:** 2020-present (best for 2023-2025)
- **Extraction Method:** Selenium + BeautifulSoup + Regex
- **Rate Limiting:** 3-second delays between requests
- **Challenges:** Dynamic JavaScript rendering, no public API

### Secondary Sources (Future Integration)

- **World Rugby** - Official PDF reports (high quality, manual extraction needed)
- **ESPN** - Basic stats (limited detail)
- **Kaggle** - Historical datasets (basic match info only)

---

## 🚀 Project Milestones

### ✅ Completed (Phase 1 - Basic Scraper)

- [x] Research available data sources
- [x] Identify RugbyPass as optimal source
- [x] Build Selenium-based basic scraper
- [x] Implement 90-field extraction logic
- [x] Test with France vs South Africa (game_id: 946471)
- [x] Create comprehensive documentation
- [x] Package scraper with 15 Six Nations 2025 matches
- [x] Implement CSV export with relational structure
- [x] Add logging and error handling

### ✅ Completed (Phase 2 - Intelligent Agent) NEW

- [x] Integrate Google Gemini API for LLM intelligence
- [x] Build 5-phase agent workflow (Plan, Scrape, Validate, Decide, Correct)
- [x] Implement autonomous URL discovery (no game_ids needed)
- [x] Add self-healing and retry logic
- [x] Create agent decision logging (JSON format)
- [x] Handle team name variations automatically
- [x] Write comprehensive intelligent agent documentation
- [x] Create comparison guide (basic vs intelligent)
- [x] Add confidence-based data validation

### ⏳ In Progress (Phase 3 - Data Collection)

- [ ] Collect all 2025 Six Nations matches (15 total)
- [ ] Expand to Rugby Championship 2025 (~12 matches)
- [ ] Add Autumn Nations Series 2025 (~20-30 matches)
- [ ] Build match URL discovery automation using intelligent agent

### 📋 Planned (Phase 4 - Historical Data)

- [ ] Collect complete 2024 data (~50-80 matches)
- [ ] Expand to 2023, 2022, 2021, 2020 (~400+ matches)
- [ ] Integrate World Rugby PDF reports
- [ ] Use intelligent agent for automatic URL discovery
- [ ] Use basic scraper for bulk scraping (hybrid approach)

### 🔮 Future Enhancements

- [ ] Player position data extraction
- [ ] Real-time match tracking
- [ ] Predictive modeling (match outcome prediction)
- [ ] Visualization dashboard (Power BI / Tableau)
- [ ] API for accessing collected data
- [ ] Database backend (SQLite / PostgreSQL)
- [ ] Club-level rugby statistics
- [ ] Women's rugby statistics
- [ ] Multi-LLM support (Claude, GPT-4, etc.)

---

## 🎓 Key Learnings & Decisions

### Technical Decisions

**Why Two Scrapers (Basic + Intelligent)?**
- Basic: Fast, free, works when URLs are known
- Intelligent: Adaptive, finds URLs automatically, validates data
- Hybrid: Best of both worlds for large-scale collection

**Why Gemini API over Claude/GPT-4?**
- Fast (gemini-2.0-flash-exp optimized for speed)
- Cheap (~$0.001 per match vs $0.01+ for GPT-4)
- Free tier available for testing
- Good at structured reasoning tasks

**Why 5-Phase Agent Workflow?**
- **PLAN:** Separates strategy from execution
- **SCRAPE:** Standard Selenium execution
- **VALIDATE:** LLM checks data quality (not just extraction success)
- **DECIDE:** Explicit decision point (accept/retry/reject)
- **CORRECT:** Learning from failures, trying alternatives

**Why Agent Decision Logs?**
- Transparency: See why agent made decisions
- Debugging: Understand failure patterns
- Improvement: Analyze logs to refine validation rules
- Trust: Users can audit AI decisions

**Why Selenium over requests/scrapy?**
- RugbyPass uses JavaScript rendering
- Statistics load dynamically via AJAX
- Requires browser automation to access full content

**Why CSV over Database?**
- Portability and simplicity
- Easy analysis with Pandas/Excel/R
- No database server setup required
- Can migrate to database later if needed

**Why game_id as Primary Key?**
- Unique identifier from RugbyPass URLs
- Stable across time (doesn't change)
- Links all related data (matches, teams, players)

**Why 3-second delays?**
- Ethical scraping practice
- Avoids server overload
- Reduces risk of IP blocking
- Still efficient for batch processing

### Data Extraction Challenges

**Challenge 1: Dynamic Content**
- **Problem:** Statistics load after initial page load
- **Solution:** WebDriverWait with explicit waits for elements

**Challenge 2: Inconsistent HTML Structure**
- **Problem:** Different matches have varying layouts
- **Basic Scraper Solution:** Robust regex patterns with fallbacks
- **Intelligent Agent Solution:** LLM adapts to variations automatically

**Challenge 3: Missing Data**
- **Problem:** Older matches have incomplete statistics
- **Solution:** NULL handling, graceful degradation, LLM confidence scoring

**Challenge 4: Unknown URLs/game_ids**
- **Problem:** Need to find match URLs for historical data
- **Basic Scraper Solution:** Manual URL finding
- **Intelligent Agent Solution:** LLM constructs and tests URLs automatically

**Challenge 5: Player Stats Variability**
- **Problem:** Not all players have all stat types
- **Solution:** Sparse matrix approach, NULL values

---

## 📈 Current Dataset Status

### 2025 Data (Active Collection)

- **Six Nations:** 15 matches configured, ready to scrape
  - Can use either basic or intelligent scraper
  - Basic: Fast (5 min), free
  - Intelligent: Slower (10 min), validated, ~$0.06

- **Rugby Championship:** Not yet started (Jul-Sep 2025)
- **Autumn Nations Series:** Not yet started (Nov 2025)

### 2024 Data (Planned)

- **Estimated Matches:** 50-80 total
- **Status:** Game IDs need to be collected
- **Recommended Approach:** Use intelligent agent to discover URLs
- **Priority:** High (recent, complete data)

### 2020-2023 Data (Future)

- **Estimated Matches:** 400-600 total
- **Status:** Planning phase
- **Recommended Approach:** Hybrid (intelligent for discovery, basic for bulk)
- **Challenges:** Finding game_ids, potential incomplete data

---

## 🛠️ Known Issues & Limitations

### Current Limitations

1. **Manual game_id Discovery (Basic Scraper):** Must find game_ids by browsing RugbyPass
   - **NEW SOLUTION:** Use intelligent agent to discover automatically
2. **Player Stats Granularity:** Basic extraction (can be enhanced)
3. **Historical Coverage:** Pre-2020 data may be incomplete on RugbyPass
4. **No Real-time Updates:** Scrapers are batch-only, not live
5. **Single Source Dependency:** Relies on RugbyPass availability
6. **LLM API Costs:** Small cost per match (~$0.001-0.005) for intelligent agent
7. **LLM Speed Overhead:** +5-10 seconds per match for agent processing

### Known Bugs

- None currently reported

### Workarounds & Mitigations

- **game_id Discovery:** Use intelligent agent for automatic URL finding
- **Data Gaps:** Will integrate World Rugby PDFs for major tournaments
- **Source Dependency:** Documented secondary sources as backups
- **API Costs:** Use hybrid approach (intelligent for discovery, basic for bulk)
- **Speed:** Use basic scraper when URLs are known

---

## 👥 Stakeholders & Use Cases

### Primary User

- **Role:** Researcher / Rugby Enthusiast / Data Analyst
- **Goal:** Collect comprehensive rugby statistics for analysis
- **Technical Level:** Intermediate Python knowledge
- **Access:** Full source code and documentation

### Use Cases

1. **Statistical Analysis:** Correlation studies (possession vs. tries)
2. **Team Performance:** Compare team metrics over time
3. **Player Tracking:** Individual player performance trends
4. **Match Prediction:** Build predictive models
5. **Academic Research:** Research papers on rugby strategies
6. **Fantasy Rugby:** Data-driven player selection
7. **Coaching Insights:** Performance benchmarking
8. **Historical Data Mining:** Discover URLs for 400+ matches automatically (NEW)
9. **Quality Assurance:** Validate data accuracy with AI confidence scores (NEW)

---

## 🔐 Ethical & Legal Considerations

### Scraping Ethics

- ✅ **robots.txt:** Verified RugbyPass allows scraping
- ✅ **Rate Limiting:** 3-second delays between requests
- ✅ **User Agent:** Transparent identification
- ✅ **No Overload:** Single-threaded scraping
- ✅ **Personal Use:** Non-commercial application
- ⚠️ **Terms of Service:** Review periodically for changes

### Data Usage

- **Purpose:** Personal research and analysis only
- **Distribution:** Not for commercial redistribution
- **Attribution:** Acknowledge RugbyPass as data source
- **Privacy:** No personal data collected (public statistics only)

### LLM API Usage (NEW)

- **Provider:** Google Gemini (public API)
- **Data Sent:** Match details (teams, dates), scraped HTML snippets
- **Data Privacy:** No sensitive personal data sent
- **API Terms:** Follow Google's Gemini API terms of service
- **Cost Management:** Monitor API usage to avoid unexpected costs

---

## 🧪 Testing & Validation

### Test Cases

1. **Single Match Test** (`test_single_match.py`)
   - France vs South Africa (946471) ✅
   - Validates all 90 statistical fields
   - Confirms CSV export structure

2. **Batch Processing Test**
   - Six Nations 2025 (15 matches)
   - Tests error handling and logging
   - Validates data integrity across matches

3. **Intelligent Agent Test (NEW)**
   - Matches without game_ids
   - URL discovery and validation
   - Self-correction on failures
   - Confidence score accuracy

4. **Edge Cases**
   - Matches with missing data
   - Incomplete player statistics
   - Network timeouts and retries
   - Team name variations

### Validation Criteria

- ✅ All expected fields present in CSV
- ✅ game_id correctly extracted from URL
- ✅ No duplicate records
- ✅ Referential integrity (game_id links)
- ✅ Data types correct (integers, floats, strings)
- ✅ NULL handling for missing data
- ✅ Agent confidence scores ≥80% for accepted matches (NEW)
- ✅ Agent decision logs are complete and parseable (NEW)

---

## 📚 Documentation Standards

### Code Documentation

- **Docstrings:** All functions have detailed docstrings
- **Comments:** Inline comments for complex logic
- **Type Hints:** Used where beneficial
- **Examples:** Code examples in README
- **Agent Prompts:** Documented in intelligent agent code (NEW)

### Project Documentation

- **README.md:** Comprehensive user guide (basic scraper)
- **README_INTELLIGENT_AGENT.md:** LLM agent guide (NEW)
- **COMPARISON_GUIDE.md:** Basic vs intelligent comparison (NEW)
- **QUICKSTART.md:** 5-minute setup guide
- **agents.md:** AI agent role definitions (updated for LLM)
- **memory.md:** Project context (this file, updated for LLM)

### Logging Standards

**Basic Scraper:**
- **Log File:** `scraping_log.txt`
- **Format:** `[TIMESTAMP] LEVEL: Message`
- **Levels:** INFO, WARNING, ERROR
- **Content:** URLs, success/failure, errors, timing

**Intelligent Agent (NEW):**
- **Log File:** `intelligent_scraping_log.txt`
- **Format:** `[TIMESTAMP] LEVEL: Message`
- **Levels:** INFO, WARNING, ERROR
- **Content:** URLs, agent phases, decisions, confidence scores, retry attempts
- **Decision Log:** `agent_decisions_{timestamp}.json` (structured JSON)

---

## 🔄 Version History

### v1.0 (November 2025) - Initial Release

- Complete basic scraper with 90-field extraction
- Six Nations 2025 configuration (15 matches)
- Comprehensive documentation
- CSV export functionality
- Error handling and logging

### v2.0 (November 2025) - Intelligent Agent Release (CURRENT)

- **NEW:** Google Gemini API integration
- **NEW:** 5-phase LLM agent workflow (Plan, Scrape, Validate, Decide, Correct)
- **NEW:** Autonomous URL discovery (no game_ids needed)
- **NEW:** Self-healing and adaptive retry logic
- **NEW:** Agent decision logging (JSON format)
- **NEW:** Team name variation handling
- **NEW:** Confidence-based data validation
- **NEW:** Comprehensive intelligent agent documentation
- **NEW:** Basic vs intelligent comparison guide
- **UPDATED:** Project documentation for dual-scraper approach

### Future Versions

- **v2.1:** Enhanced player statistics with positions
- **v2.2:** Multi-LLM support (Claude, GPT-4)
- **v2.3:** Database backend option
- **v3.0:** Real-time match tracking
- **v3.1:** Predictive modeling features

---

## 🗓️ Regular Maintenance Tasks

### Weekly

- [ ] Check for new matches in current competitions
- [ ] Update `matches_to_scrape.json` with new game_ids (or use intelligent agent)
- [ ] Run scraper for new matches (choose basic or intelligent)
- [ ] Validate output CSVs
- [ ] Monitor Gemini API usage and costs (NEW)

### Monthly

- [ ] Review scraping logs for errors
- [ ] Review agent decision logs for patterns (NEW)
- [ ] Update documentation if needed
- [ ] Check RugbyPass for website structure changes
- [ ] Backup collected data
- [ ] Analyze agent performance metrics (success rate, retry rate) (NEW)

### Quarterly

- [ ] Audit complete dataset for gaps
- [ ] Review and update statistical analysis scripts
- [ ] Plan next data collection phase
- [ ] Update dependencies (`pip install --upgrade`)
- [ ] Evaluate LLM model performance (consider model updates) (NEW)
- [ ] Optimize API costs (refine validation thresholds) (NEW)

### Annually

- [ ] Comprehensive dataset validation
- [ ] Performance optimization review
- [ ] Documentation refresh
- [ ] Archive previous year's data
- [ ] Review Gemini API pricing (budget planning) (NEW)

---

## 💡 Tips for Future Development

### When to Use Basic vs Intelligent Scraper

**Use Basic Scraper When:**
- ✅ You have all game_ids and URLs
- ✅ Recent matches with stable structure
- ✅ Need maximum speed (2-3 min for 15 matches)
- ✅ Want to avoid API costs
- ✅ Scraping 100+ matches with known URLs

**Use Intelligent Agent When:**
- ✅ Don't have game_ids or URLs
- ✅ Scraping historical matches with unknown structure
- ✅ Website structure changes frequently
- ✅ Need high data quality assurance with confidence scores
- ✅ Want self-healing capabilities
- ✅ Time is more valuable than small API cost (~$0.001/match)

**Use Hybrid Approach When:**
- ✅ Want best of both worlds
- ✅ Large-scale collection (400+ matches)
- ✅ Use intelligent agent for URL discovery
- ✅ Use basic scraper for bulk scraping
- ✅ **This is recommended for historical data collection**

### When Adding New Statistics

1. Inspect RugbyPass HTML for the new field
2. Write regex pattern to extract the value (basic scraper)
3. Add validation rules to intelligent agent
4. Add field to CSV schema documentation
5. Update extraction function in both scrapers
6. Test with known match
7. Update README with new field description

### When Debugging Scraper Issues

**Basic Scraper:**
1. Check `scraping_log.txt` for error details
2. Run `test_single_match.py` to isolate problem
3. Use browser developer tools to inspect HTML
4. Verify ChromeDriver is up to date
5. Test with headless=False to watch browser
6. Increase delays if timeouts occur

**Intelligent Agent (NEW):**
1. Check `intelligent_scraping_log.txt` for agent phases
2. Review `agent_decisions_{timestamp}.json` for decision reasoning
3. Check confidence scores (low scores indicate issues)
4. Look for retry attempts and corrections
5. Test with headless=False to watch agent work
6. Adjust validation thresholds if too strict
7. Check Gemini API status if agent fails completely

### When Analyzing Data

1. Load all three CSVs (matches, team_stats, player_stats)
2. Join on `game_id` for relational queries
3. Handle NULL values appropriately
4. Use Pandas for efficient data manipulation
5. Visualize with matplotlib/seaborn
6. Check confidence scores in agent decision logs (if using intelligent scraper)
7. Document analysis scripts for reuse

---

## 🌐 External Resources

### RugbyPass

- **Main Site:** https://www.rugbypass.com
- **Fixtures:** https://www.rugbypass.com/internationals/fixtures-results/
- **Match Format:** `/live/{team1}-vs-{team2}/stats/?g={game_id}`

### Documentation References

- **Selenium Docs:** https://selenium-python.readthedocs.io/
- **BeautifulSoup Docs:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Gemini API Docs:** https://ai.google.dev/docs (NEW)

### Rugby Statistics Resources

- **World Rugby:** https://www.world.rugby/
- **ESPN Rugby:** https://www.espn.com/rugby/
- **Ultimate Rugby:** https://www.ultimaterugby.com/

### API Resources (NEW)

- **Gemini API Key:** https://aistudio.google.com/app/apikey
- **Gemini Pricing:** https://ai.google.dev/pricing
- **Gemini Models:** https://ai.google.dev/models/gemini

---

## 🎯 Quick Reference

### Key Commands

**Basic Scraper:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python rugbypass_scraper.py

# Test single match
python test_single_match.py

# View logs
cat scraping_log.txt
```

**Intelligent Agent (NEW):**
```bash
# Install dependencies
pip install -r requirements_intelligent.txt

# Set API key
export GEMINI_API_KEY='your-key-here'

# Run intelligent scraper
python intelligent_agent_scraper.py

# View logs
cat intelligent_scraping_log.txt

# View agent decisions (formatted)
cat agent_decisions_TIMESTAMP.json | python -m json.tool
```

### Important game_ids (Reference Matches)

- **946471** - France vs South Africa (2024-11-09) - Test case
- **944287** - France vs Wales (2025-01-31) - Six Nations 2025
- **944288** - Scotland vs Italy (2025-02-01) - Six Nations 2025

### Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| ChromeDriver error | Update Chrome browser |
| Timeout error | Increase `time.sleep()` delays |
| Missing stats | Check log file, may be incomplete match data |
| CSV not created | Check write permissions in directory |
| Import errors | Run `pip install -r requirements.txt` |
| **API key error (NEW)** | Set `GEMINI_API_KEY` environment variable |
| **Agent always retries (NEW)** | Lower validation confidence threshold |
| **Agent costs too much (NEW)** | Use basic scraper with known URLs |
| **Agent too slow (NEW)** | Reduce max retries, use basic scraper |

### Cost Estimates (NEW)

| Scenario | Matches | API Cost | Time |
|----------|---------|----------|------|
| Single match test | 1 | ~$0.005 | ~30 sec |
| Six Nations 2025 | 15 | ~$0.06 | ~10 min |
| 2024 full season | 80 | ~$0.40 | ~2 hours |
| 2020-2024 (discovery) | 400 | ~$2.00 | ~8 hours |
| 2020-2024 (bulk w/URLs) | 400 | $0 | ~1 hour |

---

**Document Version:** 2.0 (LLM Intelligence Agent Added)  
**Last Updated:** November 13, 2025  
**Maintained by:** Project Manager Agent  
**Review Frequency:** Monthly or when significant changes occur

**Breaking Changes from v1.0:**
- Added intelligent agent with Gemini API integration
- Added agent decision logs and validation confidence scores
- Updated file structure for dual-scraper approach
- Added hybrid workflow (intelligent for discovery, basic for bulk)
- Added API cost and usage tracking
- Updated all documentation for LLM capabilities
