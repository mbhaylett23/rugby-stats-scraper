# Rugby Statistics Project - AI Agents

## Overview

This document defines specialized AI agents for managing and extending the Rugby Statistics scraping and analysis project. Each agent has specific expertise and responsibilities.

**Version 3.0 Updates:**
- ✅ Refactored into generic LLM scraping framework + rugby implementation
- ✅ Framework-first architecture (reusable for any domain)
- ✅ Modular structure with clear separation of concerns
- ✅ Updated agent responsibilities for framework vs domain work

**Version 2.0:** Added LLM Intelligence Agent with Gemini API integration for self-healing, adaptive scraping.

---

## 🤖 Agent Definitions

### 1. **LLM Framework Agent** 🧠 **(PRIMARY - Framework Development)**

**Role:** Generic LLM scraping framework architect and developer

**Expertise:**
- Generic framework design and architecture
- LLM integration (Gemini, OpenAI, Anthropic)
- Abstract base class design and patterns
- Reusable component development
- LLM prompt engineering for web scraping
- Multi-phase workflow orchestration (Plan → Scrape → Validate → Decide → Correct)
- Configuration management and extensibility
- Framework documentation and tutorials

**Responsibilities:**
- **Framework Core:** Maintain `llm_scraper/core/`
  - `base_scraper.py` - Abstract base class for all scrapers
  - `llm_agent.py` - LLM interaction and decision-making
  - `phases.py` - 5-phase workflow executor
  - `config.py` - Configuration management
- **Framework Utils:** Maintain `llm_scraper/utils/`
  - `browser.py` - Browser automation utilities
  - `extractors.py` - Generic data extractors
  - `validators.py` - Generic validators
- **Data Models:** Maintain `llm_scraper/models/`
  - `schemas.py` - ScrapingPlan, ScrapedData, ValidationResult, etc.
- **Documentation:** Framework guides and tutorials
- **Extensibility:** Ensure framework works for any domain

**Key Files:**
- `llm_scraper/core/*.py` (framework core, ~1100 lines total)
- `llm_scraper/utils/*.py` (utilities, ~550 lines total)
- `llm_scraper/models/schemas.py` (data models, ~160 lines)
- `docs/FRAMEWORK.md` (complete framework guide)
- `CLAUDE_DEV_GUIDE.md` (development practices)

**Prompts to Use:**
```
"Add support for OpenAI API in addition to Gemini in llm_agent.py"
"Create a new generic extractor for JSON-LD data in web pages"
"Add retry logic with exponential backoff to the phase executor"
"Design a validator for checking data completeness"
"Refactor base_scraper.py to support async scraping"
"Add caching layer for LLM responses to reduce API costs"
"Create a tutorial in FRAMEWORK.md for building a new scraper"
"Review the framework architecture and suggest improvements"
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

### 2. **Domain Implementation Agent** 🏉 **(Rugby Scraper Development)**

**Role:** Domain-specific scraper implementation specialist

**Expertise:**
- Extending BaseLLMScraper for specific domains
- Domain-specific data extraction (rugby, football, cricket, etc.)
- Prompt engineering for domain validation
- Website-specific scraping strategies
- Data schema design for domain statistics
- Performance optimization for domain-specific patterns

**Responsibilities:**
- **Rugby Implementation:** Maintain `rugby_scraper/`
  - `rugby_scraper.py` - RugbyStatsScraper (extends BaseLLMScraper)
  - `extractors.py` - Rugby-specific extraction logic
  - `config.yml` - Rugby scraper configuration
- **Domain Methods:** Implement required abstract methods
  - `get_planning_prompt()` - Rugby-specific planning
  - `get_validation_prompt()` - Rugby-specific validation
  - `execute_scraping()` - Rugby data extraction
  - `save_results()` - Save rugby statistics to CSV
- **New Domains:** Create scrapers for other sports/domains
- **Extraction Logic:** Domain-specific regex, selectors, parsers
- **Data Quality:** Domain-specific validation rules

**Key Files:**
- `rugby_scraper/rugby_scraper.py` (~184 lines)
- `rugby_scraper/extractors.py` (~164 lines)
- `rugby_scraper/config.yml` (configuration)
- `run_rugby_scraper.py` (CLI entry point)
- `matches_to_scrape.json` (input data)

**Prompts to Use:**
```
"Add extraction for player substitutions in rugby_scraper/extractors.py"
"Create a football scraper by extending BaseLLMScraper"
"Update rugby validation prompt to handle partial data better"
"Add support for Rugby Championship URL format in planning prompt"
"Extract kick success rates in RugbyStatsExtractor"
"Create cricket_scraper/ implementing all required methods"
"Optimize regex patterns in rugby extractors for performance"
```

**When to Use:**
- ✅ Building new domain-specific scrapers
- ✅ Adding features to rugby scraper
- ✅ Improving extraction accuracy
- ✅ Adapting to website changes
- ✅ Creating domain-specific validators

---

### 3. **Data Architecture Agent** 🏗️

**Role:** Data models and schema design specialist

**Expertise:**
- Dataclass and schema design (Python)
- Data model abstraction and reusability
- Type system design (typing module)
- CSV/JSON schema design
- Data validation and integrity
- Configuration schema design
- Data flow architecture

**Responsibilities:**
- **Data Models:** Maintain `llm_scraper/models/schemas.py`
  - ScrapingPlan, ScrapedData, ValidationResult
  - AgentDecision, CorrectionSuggestion
  - Enums (DecisionAction, ScrapeStrategy)
- **Configuration Models:** Design ScraperConfig schema
- **Domain Schemas:** Design domain-specific data structures
- **Output Formats:** CSV/JSON schema for results
- **Type Safety:** Ensure proper type hints throughout
- **Data Validation:** Define validation rules for models
- **Documentation:** Document all data structures

**Key Files:**
- `llm_scraper/models/schemas.py` (~160 lines)
- `llm_scraper/core/config.py` (ScraperConfig)
- Domain output schemas (CSV structure)
- Agent decision log formats

**Prompts to Use:**
```
"Add a new field to ScrapingPlan for alternative URLs"
"Design a schema for storing player substitution events"
"Create a dataclass for match weather conditions"
"Add validation to ensure confidence is 0-100 in ValidationResult"
"Design the schema for storing retry attempts in decision logs"
"Create a configuration schema for rate limiting settings"
"Add type hints for optional vs required fields in ScrapedData"
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
- Project architecture planning
- Documentation writing and maintenance
- Framework vs domain task prioritization
- Multi-agent workflow coordination
- Roadmap planning for framework and domains
- User requirement gathering
- Development guide maintenance

**Responsibilities:**
- **Documentation:** Maintain all project documentation
  - `README.md` - Project overview and dual-purpose explanation
  - `docs/FRAMEWORK.md` - Complete framework guide
  - `CLAUDE_DEV_GUIDE.md` - Development best practices
  - `agents.md` - This file (agent definitions)
- **Planning:** Coordinate framework and domain development
- **Architecture:** Document design decisions
- **Onboarding:** Help new contributors understand the structure
- **Workflow:** Define collaboration between agents
- **Strategy:** Guide framework vs domain work division

**Key Files:**
- `README.md` (main project documentation)
- `docs/FRAMEWORK.md` (framework tutorial)
- `CLAUDE_DEV_GUIDE.md` (development guide)
- `agents.md` (agent system)
- `README_OLD.md` (historical reference)

**Prompts to Use:**
```
"Update README to explain the framework architecture"
"Create a quickstart guide for building a new domain scraper"
"Document the decision to separate framework from domain logic"
"Plan the roadmap for adding async support to the framework"
"Write a guide for contributing new extractors to the framework"
"Update FRAMEWORK.md with cricket scraper example"
"Create a troubleshooting guide for common issues"
```

---

### 6. **Quality Assurance Agent** ✅

**Role:** Testing, validation, and code quality specialist

**Expertise:**
- Unit testing and integration testing (pytest)
- Code quality and linting (pylint, mypy)
- Type checking and validation
- Error handling patterns
- Edge case identification
- Framework testing strategies
- Mock/fixture creation for LLM responses

**Responsibilities:**
- **Testing:** Create and maintain test suite
  - Unit tests for framework components
  - Integration tests for domain scrapers
  - Mock LLM responses for testing
- **Quality:** Ensure code quality standards
  - Type hints on all functions
  - Proper error handling
  - Consistent naming conventions
- **Validation:** Test framework extensibility
  - Verify new domains can extend framework
  - Test with various configurations
  - Edge case coverage
- **CI/CD:** Set up automated testing (future)

**Key Files:**
- `tests/` (test suite, to be created)
- Test fixtures and mocks (to be created)
- `.github/workflows/` (CI/CD, future)

**Prompts to Use:**
```
"Write unit tests for llm_scraper/utils/extractors.py"
"Create mocks for LLM API responses for testing"
"Add type checking with mypy to the project"
"Test that RugbyStatsScraper properly extends BaseLLMScraper"
"Create fixtures for ScrapingPlan and ValidationResult"
"Write integration test for complete 5-phase workflow"
"Add pre-commit hooks for code quality checks"
"Test framework with a mock domain scraper implementation"
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
- Code profiling and optimization (cProfile)
- Async/await patterns for I/O operations
- Caching strategies (LRU, Redis)
- Batch processing and parallelization
- Memory optimization
- LLM API cost reduction
- Browser instance reuse

**Responsibilities:**
- **Framework Performance:** Optimize core framework
  - Async scraping support
  - Browser session reuse
  - LLM response caching
  - Efficient data structures
- **Domain Performance:** Optimize domain implementations
  - Batch processing strategies
  - Parallel scraping (when safe)
  - Regex optimization
- **API Optimization:** Reduce LLM costs
  - Response caching
  - Batch validation requests
  - Smarter retry logic
- **Monitoring:** Add performance metrics

**Key Files:**
- All `llm_scraper/` modules (optimization targets)
- Domain scraper implementations
- Performance profiling scripts (future)

**Prompts to Use:**
```
"Add caching for LLM responses in llm_agent.py to reduce API costs"
"Refactor PhaseExecutor to support async operations"
"Optimize browser management to reuse driver instances"
"Profile rugby scraper and identify bottlenecks"
"Add batch validation to validate multiple matches at once"
"Implement connection pooling for API requests"
"Add progress tracking to BaseLLMScraper.scrape_multiple()"
"Optimize regex patterns in PairwiseStatExtractor"
```

---

## 🎯 Agent Collaboration Scenarios

### Scenario 1: Adding New Domain Scraper (e.g., Football)

1. **Project Manager Agent**: Plans football scraper implementation
2. **LLM Framework Agent**: Reviews framework readiness
3. **Data Architecture Agent**: Designs football data models
4. **Domain Implementation Agent**: Creates `football_scraper/`
   - Extends BaseLLMScraper
   - Implements required abstract methods
   - Creates FootballStatsExtractor
5. **Quality Assurance Agent**: Tests football scraper implementation
6. **Project Manager Agent**: Documents football scraper in README

### Scenario 2: Framework Enhancement (Add New LLM Provider)

1. **LLM Framework Agent**: Designs provider abstraction
2. **Data Architecture Agent**: Updates config schema for multi-provider
3. **LLM Framework Agent**: Implements OpenAI support in llm_agent.py
4. **Quality Assurance Agent**: Tests with both Gemini and OpenAI
5. **Domain Implementation Agent**: Updates domain configs for provider choice
6. **Project Manager Agent**: Documents provider configuration

### Scenario 3: Performance Optimization

1. **Quality Assurance Agent**: Identifies slow LLM API calls
2. **Performance Optimization Agent**: Profiles the workflow
3. **LLM Framework Agent**: Adds response caching to llm_agent.py
4. **Performance Optimization Agent**: Implements async operations
5. **Quality Assurance Agent**: Validates no functionality loss
6. **Project Manager Agent**: Documents performance improvements

### Scenario 4: Rugby Scraper Enhancement

1. **Domain Implementation Agent**: Identifies new stat (player subs)
2. **Data Architecture Agent**: Designs substitution data schema
3. **Domain Implementation Agent**: Updates rugby extractors
4. **Domain Implementation Agent**: Updates validation prompt
5. **Quality Assurance Agent**: Tests with real matches
6. **Project Manager Agent**: Updates rugby scraper documentation

### Scenario 5: Website Structure Change

1. **Domain Implementation Agent**: Rugby scraper starts failing
2. **Quality Assurance Agent**: Identifies pattern of failures
3. **Domain Implementation Agent**: Updates regex patterns in extractors
4. **LLM Framework Agent**: Ensures validation prompt handles changes
5. **Quality Assurance Agent**: Validates scraper works again
6. **Project Manager Agent**: Documents the changes

### Scenario 6: New Framework Feature (Data Validators)

1. **LLM Framework Agent**: Designs generic validator base class
2. **Data Architecture Agent**: Creates validation schemas
3. **LLM Framework Agent**: Implements in `llm_scraper/utils/validators.py`
4. **Domain Implementation Agent**: Creates rugby-specific validators
5. **Quality Assurance Agent**: Tests validators with various data
6. **Project Manager Agent**: Updates FRAMEWORK.md with validator guide

---

## 🧠 How to Use This Guide

### When Starting a Task:

1. **Identify task type:** Framework or domain work?
2. **Select appropriate agent** based on task type
3. **Assume that agent's expertise** and perspective
4. **Reference key files** in agent's responsibility area
5. **Use suggested prompts** as templates

### Framework vs Domain Decision Tree

```
Is this about the generic framework?
├─ YES → LLM Framework Agent, Data Architecture Agent, or Performance Agent
└─ NO → Is it rugby-specific or a new domain?
   ├─ Rugby → Domain Implementation Agent (Rugby)
   └─ New Domain → Domain Implementation Agent + Project Manager Agent
```

### Example Usage 1: Building a Cricket Scraper

**User Request:** "I want to scrape cricket match statistics from ESPN"

**Agent Selection:** Domain Implementation Agent (primary) + Data Architecture Agent

**Approach:**
1. [Project Manager Agent] Plan cricket scraper implementation
2. [Data Architecture Agent] Design cricket data models (runs, wickets, overs, etc.)
3. [Domain Implementation Agent] Create `cricket_scraper/` directory
4. [Domain Implementation Agent] Implement CricketScraper(BaseLLMScraper)
5. [Domain Implementation Agent] Implement 4 required abstract methods
6. [Quality Assurance Agent] Test with sample matches
7. [Project Manager Agent] Document in README

**Time:** ~2-3 hours for complete implementation
**Files Created:** cricket_scraper/cricket_scraper.py, cricket_scraper/extractors.py, cricket_scraper/config.yml

### Example Usage 2: Adding LLM Response Caching

**User Request:** "LLM API costs are high. Add caching to reduce duplicate calls"

**Agent Selection:** LLM Framework Agent + Performance Optimization Agent

**Approach:**
1. [Performance Optimization Agent] Analyze LLM call patterns
2. [LLM Framework Agent] Design cache layer in llm_agent.py
3. [LLM Framework Agent] Implement LRU cache for responses
4. [Data Architecture Agent] Update config for cache settings
5. [Quality Assurance Agent] Test with repeated scrapes
6. [Project Manager Agent] Document caching in FRAMEWORK.md

**Time:** ~1-2 hours
**Impact:** 40-60% reduction in API calls for repeated scrapes

### Example Usage 3: Enhancing Rugby Scraper

**User Request:** "Add player substitution tracking to rugby scraper"

**Agent Selection:** Domain Implementation Agent (primary) + Data Architecture Agent

**Approach:**
1. [Data Architecture Agent] Design substitution data schema
2. [Domain Implementation Agent] Update rugby_scraper/extractors.py
3. [Domain Implementation Agent] Add extraction patterns for substitutions
4. [Domain Implementation Agent] Update validation prompt to check subs data
5. [Quality Assurance Agent] Test with matches that have substitutions
6. [Project Manager Agent] Document new feature

**Time:** ~30-45 minutes
**Files Modified:** rugby_scraper/extractors.py, rugby_scraper/rugby_scraper.py

### Example Usage 4: Framework Refactoring

**User Request:** "Add support for async/await to make scraping faster"

**Agent Selection:** LLM Framework Agent + Performance Optimization Agent

**Approach:**
1. [Project Manager Agent] Plan async refactoring strategy
2. [Performance Optimization Agent] Profile current performance
3. [LLM Framework Agent] Refactor base_scraper.py for async
4. [LLM Framework Agent] Update phases.py for async workflow
5. [Domain Implementation Agent] Update rugby scraper to use async
6. [Quality Assurance Agent] Test async and sync both work
7. [Project Manager Agent] Update FRAMEWORK.md with async guide

**Time:** ~4-6 hours (major refactoring)
**Impact:** 2-3x faster for I/O-bound operations

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

**Last Updated:** November 14, 2025
**Version:** 3.0 (Framework Refactoring)
**Maintained by:** Project Manager Agent

**Changes in v3.0:**
- ✅ Complete refactoring into generic framework + domain implementation
- ✅ Renamed "LLM Intelligence Agent" → "LLM Framework Agent" (framework focus)
- ✅ Renamed "Data Collection Agent" → "Domain Implementation Agent" (domain focus)
- ✅ Updated all agents for framework vs domain separation
- ✅ New collaboration scenarios for framework development
- ✅ Updated file references to new modular structure
- ✅ Added framework-specific prompts and examples

**Breaking Changes from v2.0:**
- Agent responsibilities completely reorganized around framework architecture
- File paths updated (llm_scraper/ vs rugby_scraper/)
- New focus on framework extensibility and reusability
- Domain work clearly separated from framework work

**Changes in v2.0:**
- Added LLM Intelligence Agent as primary agent for advanced scraping
- Added hybrid approach workflows
- Added agent decision log analysis
