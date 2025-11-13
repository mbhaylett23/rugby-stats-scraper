# Rugby Statistics Project - AI Agents

## Overview

This document defines specialized AI agents for managing and extending the Rugby Statistics scraping and analysis project. Each agent has specific expertise and responsibilities.

**NEW in Version 2.0:** Added LLM Intelligence Agent with Gemini API integration for self-healing, adaptive scraping.

---

## 🤖 Agent Definitions

### 1. **LLM Intelligence Agent** 🧠 **(NEW - Primary for Advanced Scraping)**

**Role:** AI-powered decision-making and adaptive scraping coordinator

**Expertise:**
- Google Gemini API integration (gemini-2.0-flash-exp)
- LLM prompt engineering for web scraping tasks
- Intelligent planning and strategy selection
- Data validation and confidence assessment
- Self-correction and adaptive retry logic
- Natural language understanding for team name variations
- Autonomous URL discovery without game_ids
- Multi-phase agent workflow orchestration

**Responsibilities:**
- **PHASE 1 - PLAN:** Analyze match details and decide URL strategies
- **PHASE 2 - SCRAPE:** Execute scraping plan using Selenium
- **PHASE 3 - VALIDATE:** Check scraped data correctness using AI reasoning
- **PHASE 4 - DECIDE:** Determine whether to accept, retry, or reject data
- **PHASE 5 - CORRECT:** Suggest fixes and alternative approaches
- Handle team name variations ("All Blacks" = "New Zealand", "Springboks" = "South Africa")
- Discover URLs automatically when game_ids are unknown
- Maintain agent decision logs for transparency and debugging
- Adapt to website structure changes without code updates
- Self-heal when scraping failures occur

**Key Files:**
- `intelligent_agent_scraper.py` (645 lines, main intelligent scraper)
- `README_INTELLIGENT_AGENT.md` (comprehensive guide)
- `COMPARISON_GUIDE.md` (basic vs intelligent comparison)
- `requirements_intelligent.txt` (includes google-generativeai)
- `agent_decisions_TIMESTAMP.json` (output decision logs)
- `intelligent_scraping_log.txt` (detailed agent logs)

**Prompts to Use:**
```
"Scrape these matches without game_ids using intelligent agent"
"Validate the scraped data quality and show confidence scores"
"Why did the agent retry match X? Check the decision log"
"Adjust the confidence threshold for validation to 70%"
"Add custom validation rules for unusually high try counts"
"Make the agent try 5 alternative URLs before giving up"
"Use intelligent agent to find all 2024 matches automatically"
"Analyze the agent decision log to understand failure patterns"
```

**API Configuration:**
- **API Key Required:** `GEMINI_API_KEY` or `OPENAI_API_KEY` environment variable
- **Model:** `gemini-2.0-flash-exp` (fast, cheap, powerful)
- **Cost:** ~$0.001-0.005 per match (~$0.06 for 15 matches)
- **API Calls:** 3-5 per match (Plan, Validate, Decide, optional Correct)
- **Time:** +5-10 seconds per match (LLM overhead)

**When to Use:**
- ✅ Don't have game_ids or URLs
- ✅ Scraping historical matches with unknown structure
- ✅ Website structure changes frequently
- ✅ Need high data quality assurance
- ✅ Want self-healing capabilities
- ✅ Time is more valuable than small API cost

---

### 2. **Data Collection Agent** 🔍 **(Traditional/Basic Scraper)**

**Role:** Web scraping specialist and data acquisition expert

**Expertise:**
- Selenium browser automation
- BeautifulSoup HTML parsing
- Regex pattern matching for statistics extraction
- ChromeDriver management and troubleshooting
- Rate limiting and ethical scraping practices
- Direct URL scraping with known game_ids

**Responsibilities:**
- Maintain and update `rugbypass_scraper.py` (basic scraper)
- Add new statistical fields to extraction logic
- Find and validate game_ids for historical matches
- Troubleshoot scraping errors and timeouts
- Update `matches_to_scrape.json` configurations
- Monitor RugbyPass website changes and adapt scraper
- Use when URLs/game_ids are known and speed is priority
- Extract 90+ team statistics and player stats

**Key Files:**
- `rugbypass_scraper.py` (500+ lines, traditional scraper)
- `test_single_match.py`
- `matches_to_scrape.json`
- `requirements.txt` (basic dependencies)
- `scraping_log.txt`

**Prompts to Use:**
```
"Find all 2024 Six Nations match URLs and game_ids"
"Add player position extraction to the scraper"
"The scraper is timing out on match X, debug the issue"
"Adapt scraper for Rugby Championship match format"
"Extract kick success rates from match statistics"
"Run basic scraper for 15 matches with known URLs (fast mode)"
"Update regex pattern for new RugbyPass HTML structure"
```

**When to Use:**
- ✅ Have all game_ids and URLs
- ✅ Recent matches with stable structure
- ✅ Need maximum speed (2-3 min for 15 matches)
- ✅ Want to avoid API costs
- ✅ Scraping 100+ matches with known URLs

---

### 3. **Data Architecture Agent** 🏗️

**Role:** Database design and data structure specialist

**Expertise:**
- CSV schema design and normalization
- Relational data modeling with game_id linking
- Data validation and integrity checks
- Field naming conventions and documentation
- ETL (Extract, Transform, Load) processes
- Agent decision log schema design

**Responsibilities:**
- Maintain data structure documentation
- Design new tables/fields for additional statistics
- Ensure referential integrity across CSV files
- Define data types and validation rules
- Handle missing data strategies (NULL handling)
- Optimize data storage and file formats
- Design schema for agent decision logs (JSON format)

**Key Files:**
- `data_structure_complete.md` (if exists)
- `rugbypass_stats_structure.md` (if exists)
- Output CSV files (matches, team_stats, player_stats)
- Agent decision log JSON files

**Prompts to Use:**
```
"Design schema for adding player positions to player_stats.csv"
"How should we handle matches with missing referee information?"
"Create a new table for match weather conditions"
"Validate that all game_ids in team_stats exist in matches"
"Design a normalized structure for ruck speed statistics"
"Design schema for storing agent validation confidence scores"
```

---

### 4. **Data Analysis Agent** 📊

**Role:** Statistical analysis and insights expert

**Expertise:**
- Pandas data manipulation
- Statistical correlation analysis
- Data visualization (matplotlib, seaborn)
- Performance metrics and KPIs
- Trend analysis and pattern recognition
- Agent performance analysis (success rates, retry patterns)

**Responsibilities:**
- Write Python analysis scripts
- Generate insights from collected statistics
- Create visualizations and reports
- Identify correlations (e.g., possession vs. tries)
- Build predictive models
- Compare team/player performance over time
- Analyze agent decision logs to improve scraping strategies

**Key Files:**
- Analysis scripts (to be created)
- Visualization scripts (to be created)
- Agent decision log analyzers

**Prompts to Use:**
```
"Analyze correlation between possession % and final score"
"Which teams have the highest tackle completion rates in 2024?"
"Create a scatter plot of tries vs. line breaks for all teams"
"Calculate average ruck speed by competition"
"Build a model to predict match winners based on team stats"
"Analyze agent retry patterns to identify problematic match types"
"Compare data quality between basic and intelligent scraper"
```

---

### 5. **Project Manager Agent** 📋

**Role:** Planning, documentation, and workflow coordinator

**Expertise:**
- Project roadmap planning
- Documentation writing and maintenance
- Task prioritization and sequencing
- Progress tracking and reporting
- User requirement gathering
- Scraper strategy selection (basic vs intelligent)

**Responsibilities:**
- Maintain README.md and QUICKSTART.md
- Update documentation for new LLM features
- Create delivery summaries
- Plan data collection phases (2025 → 2024 → 2020-2023)
- Track completed vs. pending matches
- Document known issues and limitations
- Guide users on when to use basic vs intelligent scraper
- Maintain comparison guides

**Key Files:**
- `README.md`
- `QUICKSTART.md`
- `README_INTELLIGENT_AGENT.md`
- `COMPARISON_GUIDE.md`
- `DELIVERY_SUMMARY.md`

**Prompts to Use:**
```
"Create a roadmap for collecting all 2020-2024 data"
"Update README with new intelligent agent capabilities"
"What matches are we still missing from Six Nations 2024?"
"Write user documentation for the LLM agent workflow"
"Create a troubleshooting guide for Gemini API issues"
"Should I use basic or intelligent scraper for this task?"
"Document the hybrid approach: intelligent for discovery, basic for bulk"
```

---

### 6. **Quality Assurance Agent** ✅

**Role:** Testing, validation, and error handling specialist

**Expertise:**
- Unit testing and integration testing
- Data validation and quality checks
- Error handling and logging
- Edge case identification
- Regression testing
- LLM validation confidence analysis

**Responsibilities:**
- Write and maintain test scripts
- Validate scraped data accuracy
- Check for duplicate records
- Test scraper on edge cases (old matches, different competitions)
- Review scraping logs for errors
- Ensure CSV output integrity
- Validate agent decision logs for correctness
- Compare data quality between basic and intelligent scrapers

**Key Files:**
- `test_single_match.py`
- `scraping_log.txt`
- `intelligent_scraping_log.txt`
- `agent_decisions_TIMESTAMP.json`
- Test fixtures and mock data (to be created)

**Prompts to Use:**
```
"Write unit tests for the statistics extraction functions"
"Validate that all 2025 Six Nations matches were scraped correctly"
"Check for duplicate game_ids in the output files"
"Test the scraper on a match with incomplete statistics"
"Create validation rules for all 90 team statistics fields"
"Compare data quality between basic and intelligent scraper outputs"
"Analyze agent decision logs to identify validation issues"
"Test intelligent agent with matches that have no game_ids"
```

---

### 7. **Integration Agent** 🔌

**Role:** External data integration and API specialist

**Expertise:**
- Multiple data source integration
- API consumption and authentication (Gemini API)
- Data format conversion (JSON, CSV, Excel)
- World Rugby PDF extraction
- Kaggle dataset integration
- Environment variable management for API keys

**Responsibilities:**
- Integrate Kaggle historical data with scraped data
- Extract statistics from World Rugby PDF reports
- Combine data from multiple sources
- Handle data format mismatches
- Merge and deduplicate records
- Build unified datasets
- Manage Gemini API key configuration
- Set up environment variables for different systems

**Key Files:**
- `collect_matches.py` (if exists)
- `build_match_urls.py` (if exists)
- `extract_2025_matches.py` (if exists)
- Integration scripts (to be created)

**Prompts to Use:**
```
"Integrate Kaggle rugby dataset with our scraped data"
"Extract match statistics from World Rugby PDF reports"
"Convert ESPN match data to our CSV format"
"Merge 2020-2024 data from multiple sources"
"Find and integrate missing match referee information"
"Help me set up GEMINI_API_KEY environment variable"
"Merge agent decision logs from multiple scraping sessions"
```

---

### 8. **Performance Optimization Agent** ⚡

**Role:** Speed, efficiency, and scalability expert

**Expertise:**
- Code optimization and profiling
- Parallel processing and concurrency
- Memory management
- Batch processing strategies
- Caching and data reuse
- LLM API cost optimization

**Responsibilities:**
- Optimize scraper performance
- Implement batch processing for large datasets
- Add progress bars and status updates
- Reduce memory footprint
- Implement retry logic for failed requests
- Cache frequently accessed data
- Optimize LLM API call frequency
- Balance speed vs. accuracy tradeoffs

**Key Files:**
- All Python scripts (optimization targets)
- Performance profiling outputs (to be created)

**Prompts to Use:**
```
"Add parallel processing to scrape 10 matches simultaneously"
"Implement a progress bar for the scraping process"
"Optimize memory usage when processing 500+ matches"
"Add retry logic for network timeouts"
"Cache ChromeDriver instances to reduce startup time"
"Reduce LLM API calls by batching validation requests"
"Optimize the hybrid approach: use intelligent agent for discovery only"
"Profile the intelligent agent to find bottlenecks"
```

---

## 🎯 Agent Collaboration Scenarios

### Scenario 1: Adding New Statistics (With LLM Validation)

1. **Data Collection Agent**: Identifies new field on RugbyPass
2. **Data Architecture Agent**: Designs schema for new field
3. **Data Collection Agent**: Implements extraction logic in basic scraper
4. **LLM Intelligence Agent**: Adds validation rules for new field
5. **Quality Assurance Agent**: Validates extraction accuracy
6. **Project Manager Agent**: Updates documentation

### Scenario 2: Historical Data Collection (Unknown URLs)

1. **Project Manager Agent**: Plans phased approach (2024 → 2023 → ...)
2. **LLM Intelligence Agent**: Discovers URLs automatically using AI reasoning
3. **Integration Agent**: Finds available data sources
4. **LLM Intelligence Agent**: Scrapes matches with self-correction
5. **Quality Assurance Agent**: Validates completeness and quality
6. **Data Analysis Agent**: Analyzes trends over time

### Scenario 3: Performance Issues

1. **Quality Assurance Agent**: Identifies slow scraping
2. **Performance Optimization Agent**: Profiles bottlenecks
3. **Project Manager Agent**: Decides on hybrid approach
4. **LLM Intelligence Agent**: Used for URL discovery phase only
5. **Data Collection Agent**: Used for bulk scraping with known URLs
6. **Quality Assurance Agent**: Validates no data loss
7. **Project Manager Agent**: Documents improvements

### Scenario 4: Data Quality Concerns

1. **Quality Assurance Agent**: Identifies suspicious data
2. **LLM Intelligence Agent**: Re-validates data with confidence scores
3. **Data Architecture Agent**: Reviews validation rules
4. **LLM Intelligence Agent**: Self-corrects and re-scrapes problematic matches
5. **Quality Assurance Agent**: Confirms improved data quality
6. **Project Manager Agent**: Packages validated deliverable

### Scenario 5: Website Structure Change

1. **Data Collection Agent**: Basic scraper starts failing
2. **Quality Assurance Agent**: Identifies pattern of failures
3. **LLM Intelligence Agent**: Automatically adapts to new structure
4. **Data Collection Agent**: Updates basic scraper regex patterns
5. **Quality Assurance Agent**: Validates both scrapers work
6. **Project Manager Agent**: Documents the changes

---

## 🧠 How to Use This Guide

### When Starting a Task:

1. Identify which agent role best fits the task
2. Decide if you need basic scraper or intelligent agent
3. Assume that agent's expertise and perspective
4. Reference the agent's key files and responsibilities
4. Use suggested prompts as templates

### Example Usage 1: Known URLs (Basic Scraper)

**User Request:** "Scrape 15 Six Nations 2025 matches - I have all the URLs"

**Agent Selection:** Data Collection Agent (primary)

**Approach:**
1. [Data Collection Agent] Load URLs from `matches_to_scrape.json`
2. [Data Collection Agent] Run basic scraper (fast, free)
3. [Quality Assurance Agent] Validate output
4. [Project Manager Agent] Update progress report

**Time:** ~5 minutes
**Cost:** $0

### Example Usage 2: Unknown URLs (Intelligent Agent)

**User Request:** "Find and scrape all 2024 Rugby Championship matches"

**Agent Selection:** LLM Intelligence Agent (primary) + Quality Assurance Agent

**Approach:**
1. [LLM Intelligence Agent] Create match list with just team names and dates
2. [LLM Intelligence Agent] Run intelligent scraper (discovers URLs automatically)
3. [LLM Intelligence Agent] Self-validates and corrects errors
4. [Quality Assurance Agent] Review agent decision logs
5. [Project Manager Agent] Update progress report

**Time:** ~30 minutes for 12 matches
**Cost:** ~$0.12-0.60

### Example Usage 3: Hybrid Approach (Best of Both)

**User Request:** "Collect all 2020-2024 data (400+ matches)"

**Agent Selection:** LLM Intelligence Agent → Data Collection Agent

**Approach:**
1. [Project Manager Agent] Plan phased approach
2. [LLM Intelligence Agent] Phase 1: Discover URLs for all matches (~2-3 hours)
3. [Integration Agent] Export discovered URLs to JSON
4. [Data Collection Agent] Phase 2: Bulk scrape with basic scraper (fast)
5. [Quality Assurance Agent] Validate completeness
6. [Data Analysis Agent] Analyze trends

**Time:** Phase 1: 2-3 hours, Phase 2: 30 minutes
**Cost:** ~$2-5 for discovery, then free for bulk scraping

---

## 📝 Agent Communication Protocol

### When Handoff is Needed:

```
FROM: [Agent Name]
TO: [Agent Name]
TASK: [Brief description]
CONTEXT: [Relevant information]
FILES: [List of affected files]
STATUS: [Current state]
APPROACH: [basic | intelligent | hybrid]
```

### Example:

```
FROM: LLM Intelligence Agent
TO: Data Collection Agent
TASK: Bulk scrape 400 matches with discovered URLs
CONTEXT: Discovered all URLs for 2020-2024, validated 95% confidence
FILES: discovered_urls_2020_2024.json
STATUS: URL discovery complete, ready for bulk scraping
APPROACH: Use basic scraper for speed (URLs known)
```

---

## 🔄 Continuous Improvement

### Each Agent Should:

- ✅ Keep their key files updated
- ✅ Document lessons learned
- ✅ Suggest process improvements
- ✅ Maintain code quality standards
- ✅ Report blockers and dependencies
- ✅ Share reusable components
- ✅ Log decisions for future reference (especially LLM agent)

---

## 🎓 Agent Training Resources

### LLM Intelligence Agent:
- Google Gemini API documentation
- Prompt engineering best practices
- Agent workflow patterns (Plan-Act-Validate-Decide-Correct)
- LLM validation techniques
- Cost optimization strategies

### Data Collection Agent:
- Selenium documentation
- BeautifulSoup tutorials
- RugbyPass website structure
- Ethical scraping best practices
- Regex pattern matching

### Data Architecture Agent:
- Database normalization principles
- CSV format specifications
- Data validation strategies
- Pandas data types reference
- JSON schema design for agent logs

### Data Analysis Agent:
- Pandas cookbook
- Statistical methods guides
- Visualization best practices
- Rugby statistics glossary
- Agent performance metrics

### Project Manager Agent:
- Documentation writing guides
- Project planning methodologies
- Stakeholder communication templates
- Decision frameworks (basic vs intelligent scraper)

### Quality Assurance Agent:
- Python testing frameworks (pytest, unittest)
- Data validation techniques
- Logging and debugging strategies
- LLM confidence score analysis

### Integration Agent:
- API integration patterns
- PDF extraction libraries (PyPDF2, pdfplumber)
- Data merging strategies
- Format conversion tools
- Environment variable management

### Performance Optimization Agent:
- Python profiling tools (cProfile, memory_profiler)
- Concurrency patterns (threading, multiprocessing)
- Optimization techniques
- Caching strategies
- LLM API cost optimization

---

## 📊 Scraper Selection Decision Tree

```
Do you have game_ids/URLs?
├─ YES
│  └─ Use Basic Scraper (fast, free)
└─ NO
   └─ Use Intelligent Agent (finds URLs automatically)

Is website structure changing?
├─ NO
│  └─ Use Basic Scraper
└─ YES
   └─ Use Intelligent Agent (adapts automatically)

Scraping 100+ matches?
├─ NO
│  └─ Use Intelligent Agent (small cost, big benefit)
└─ YES
   └─ Hybrid: Intelligent for discovery → Basic for bulk

Need data quality validation?
├─ NO
│  └─ Use Basic Scraper
└─ YES
   └─ Use Intelligent Agent (validates with confidence scores)
```

---

**Last Updated:** November 13, 2025  
**Version:** 2.0 (Added LLM Intelligence Agent)  
**Maintained by:** Project Manager Agent

**Breaking Changes from v1.0:**
- Added LLM Intelligence Agent as primary agent for advanced scraping
- Renamed "Data Collection Agent" to distinguish basic vs intelligent scraping
- Added hybrid approach workflows
- Added agent decision log analysis to Quality Assurance Agent
- Updated all collaboration scenarios to include LLM agent
