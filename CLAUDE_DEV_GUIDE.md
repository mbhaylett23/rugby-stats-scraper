# Claude Development Guide
## Rugby Stats Scraper & LLM Framework Project

This document contains best practices and guidelines for working with Claude AI on this project.

---

## Table of Contents

1. [Good Development Practices](#good-development-practices)
2. [Modular Code Organization](#modular-code-organization)
3. [File Size Management](#file-size-management)
4. [Module Extraction](#module-extraction)
5. [Documentation Standards](#documentation-standards)
6. [Working with Context Windows](#working-with-context-windows)
7. [Project-Specific Guidelines](#project-specific-guidelines)
8. [Agent Usage Guide](#agent-usage-guide)

---

## Good Development Practices

### Modular Code Organization

Keep Python modules small and focused to avoid overwhelming AI context windows.

#### Why Modular Development Matters

AI assistants like Claude have context window limitations (typically 200k tokens). When files grow too large:

- ❌ Claude cannot read the entire file in one go
- ❌ Understanding the full codebase becomes difficult
- ❌ Refactoring and debugging are slower
- ❌ Risk of missing important details increases

**Best Practice:** Aim for **< 400 lines or < 15,000 tokens per Python file.**

#### Example: Our Refactoring Success ✅

**Before (Monolithic):**
```
rugby-stats-scraper/
  intelligent_agent_scraper.py  (645 lines, ~25,000 tokens) ❌
```

**After (Modular Framework):**
```
rugby-stats-scraper/
  llm_scraper/                   # Generic Framework
    core/
      base_scraper.py            (265 lines) ✅
      llm_agent.py               (232 lines) ✅
      phases.py                  (288 lines) ✅
      config.py                  (133 lines) ✅
    utils/
      browser.py                 (162 lines) ✅
      extractors.py              (182 lines) ✅
      validators.py              (207 lines) ✅
    models/
      schemas.py                 (160 lines) ✅

  rugby_scraper/                 # Domain Implementation
    rugby_scraper.py             (184 lines) ✅
    extractors.py                (164 lines) ✅

  run_rugby_scraper.py           (118 lines) ✅
```

**Benefits:**
- ✅ Each file is easily readable by AI
- ✅ Changes are isolated and safer
- ✅ Easier to test individual modules
- ✅ Better code organization
- ✅ Framework is reusable for other domains
- ✅ Faster development iterations

---

## File Size Management

### When to Split a Python Module

Consider extracting code when:

- ✅ **File exceeds 300 lines** - Getting hard to navigate
- ✅ **Multiple responsibilities** - Module handles more than one concern
- ✅ **Claude hits token limits** - Cannot read full file
- ✅ **Complex class** - Class has >10 methods
- ✅ **New features planned** - Will make file even larger

### How to Split Effectively

#### 1. Identify logical boundaries

```python
# Look for:
- Multiple classes in one file
- Distinct functional areas (extractors, validators, config)
- Utility functions that could be separated
- Different abstraction levels
```

#### 2. Extract into separate modules

```python
# BEFORE: One large file
# scraper.py (800 lines)
class Scraper:
    def __init__(self): ...
    def scrape(self): ...
    def extract_data(self): ...
    def validate(self): ...
    def save(self): ...

# Helper functions
def parse_html(): ...
def format_date(): ...
# ... 700 more lines

# AFTER: Modular structure
# scraper.py (150 lines)
from extractors import DataExtractor
from validators import DataValidator
from utils import parse_html, format_date

class Scraper:
    def __init__(self):
        self.extractor = DataExtractor()
        self.validator = DataValidator()
    # Clean, focused implementation

# extractors.py (200 lines)
class DataExtractor:
    # All extraction logic

# validators.py (180 lines)
class DataValidator:
    # All validation logic

# utils.py (120 lines)
def parse_html(): ...
def format_date(): ...
```

#### 3. Update imports

```python
# Use explicit imports
from llm_scraper.core.base_scraper import BaseLLMScraper
from llm_scraper.models.schemas import ScrapingPlan, ScrapedData

# Avoid wildcard imports
from llm_scraper.core import *  # ❌ BAD

# Group imports logically
# Standard library
import os
import json
from typing import Dict, List

# Third-party
import pandas as pd
from bs4 import BeautifulSoup

# Local application
from llm_scraper.core.base_scraper import BaseLLMScraper
from rugby_scraper.extractors import RugbyStatsExtractor
```

#### 4. Test thoroughly

```bash
# Verify imports work
python -m py_compile module_name.py

# Run tests
pytest tests/

# Check for circular dependencies
python -c "import module_name"
```

---

## Module Extraction

### Step-by-Step Process

#### 1. Analyze the large file

```bash
# Check file size
wc -l scraper.py

# Estimate tokens (rough: lines × 35 for Python)
# 500 lines ≈ 17,500 tokens
```

#### 2. Identify modules to extract

```python
# Look for:
- Class definitions that are self-contained
- Groups of related functions
- Configuration/constants sections
- Utility functions
```

#### 3. Create new directory structure

```bash
mkdir -p module_name
mkdir -p module_name/utils
touch module_name/__init__.py
```

#### 4. Extract modules one by one

```python
# 1. Copy class/functions to new file
# 2. Add necessary imports
# 3. Add __all__ export in __init__.py
# 4. Update original file to import
```

#### 5. Verify and commit

```bash
# Syntax check
python -m py_compile new_module.py

# Import test
python -c "from module_name import MyClass"

# Commit
git add .
git commit -m "refactor: Extract MyClass into separate module"
```

---

## Documentation Standards

### Document As You Go

Always document:

- ✅ **Complex business logic**
- ✅ **Non-obvious design decisions**
- ✅ **API integrations** (Gemini, RugbyPass)
- ✅ **LLM prompt engineering** patterns
- ✅ **Data extraction strategies**

### Good vs Bad Documentation

```python
# ❌ BAD: No context
def calc(a, b):
    return a * 5 + b * 2 + 3

# ✅ GOOD: Clear purpose
def calculate_rugby_points(tries: int, conversions: int, penalties: int = 0) -> int:
    """
    Calculate total points for a rugby team.

    Formula: (tries × 5) + (conversions × 2) + (penalties × 3)

    Args:
        tries: Number of tries scored (worth 5 points each)
        conversions: Number of conversions made (worth 2 points each)
        penalties: Number of penalty goals (worth 3 points each)

    Returns:
        Total points scored by the team

    Example:
        >>> calculate_rugby_points(tries=3, conversions=2, penalties=1)
        22  # (3×5) + (2×2) + (1×3) = 22
    """
    return (tries * 5) + (conversions * 2) + (penalties * 3)
```

### Module-Level Documentation

```python
"""
Rugby-specific data extractors.

This module implements extraction logic for rugby statistics from RugbyPass pages.
Uses regex patterns to extract pairwise statistics (home vs away).

Classes:
    RugbyStatsExtractor: Main extractor for rugby match statistics

Usage:
    extractor = RugbyStatsExtractor()
    match_info, team_stats = extractor.extract_rugby_stats(soup, text, game_id, url)
"""
```

### Class Documentation

```python
class RugbyStatsScraper(BaseLLMScraper):
    """
    Scraper for rugby match statistics from RugbyPass.

    Extends BaseLLMScraper to provide rugby-specific scraping logic.
    Implements the 5-phase intelligent workflow for robust data collection.

    Attributes:
        matches_data: List of scraped match information
        team_stats_data: List of team statistics records
        player_stats_data: List of player statistics records
        extractor: RugbyStatsExtractor instance

    Example:
        config = ScraperConfig.from_env()
        scraper = RugbyStatsScraper(config)
        scraper.scrape_from_file('matches.json')
        scraper.save_results()
    """
```

---

## Working with Context Windows

### Understanding Token Limits

- **Total context:** ~200,000 tokens
- **Safe file size:** < 15,000 tokens (~400 Python lines)
- **Ideal file size:** < 7,000 tokens (~200 Python lines)

### Strategies for This Codebase

#### 1. Use the Task Agent for Exploration

**✅ GOOD:**
```
"Use the Task tool with subagent_type=Explore to find
how the LLM validation works in the framework"
```

**❌ BAD:**
```
"Read all files and tell me how validation works"
```

#### 2. Read Specific Files

**✅ GOOD:**
```
"Read llm_scraper/core/llm_agent.py and explain
the validate_data method"
```

**❌ BAD:**
```
"Read all files in llm_scraper/"
```

#### 3. Grep Before Reading

**✅ GOOD:**
```
"Search for 'ScrapingPlan' then read the relevant files
to understand the data model"
```

#### 4. Provide Clear Context

**✅ GOOD:**
```
"I'm implementing a football scraper. The base framework
is in llm_scraper/. Read llm_scraper/core/base_scraper.py
and rugby_scraper/rugby_scraper.py as a reference, then
help me implement FootballScraper."
```

---

## Project-Specific Guidelines

### Directory Structure

```
rugby-stats-scraper/
├── llm_scraper/           # Generic Framework (reusable)
│   ├── core/             # Core framework logic
│   ├── utils/            # Utilities (browser, extractors, validators)
│   └── models/           # Data models
├── rugby_scraper/         # Rugby Implementation
│   ├── rugby_scraper.py  # Extends BaseLLMScraper
│   └── extractors.py     # Rugby-specific extraction
├── docs/                  # Documentation
├── examples/              # Example implementations (future)
└── tests/                 # Unit tests (future)
```

### Naming Conventions

- **Modules:** `snake_case.py` (base_scraper.py)
- **Classes:** `PascalCase` (BaseLLMScraper)
- **Functions:** `snake_case()` (extract_stats)
- **Constants:** `UPPER_SNAKE_CASE` (MAX_RETRIES)
- **Private:** `_leading_underscore` (_parse_json_response)

### Code Organization

#### Framework vs Domain Logic

```python
# ✅ GOOD: Generic logic in framework
# llm_scraper/core/base_scraper.py
class BaseLLMScraper(ABC):
    """Generic base class for all scrapers"""
    @abstractmethod
    def get_planning_prompt(self) -> str:
        """Domain-specific planning instructions"""
        pass

# ✅ GOOD: Domain logic in implementation
# rugby_scraper/rugby_scraper.py
class RugbyStatsScraper(BaseLLMScraper):
    def get_planning_prompt(self) -> str:
        return "Rugby-specific planning instructions..."
```

```python
# ❌ BAD: Rugby-specific logic in generic framework
# llm_scraper/core/base_scraper.py
class BaseLLMScraper(ABC):
    def extract_tries(self):  # ❌ Rugby-specific!
        pass
```

### Type Hints

```python
# ✅ GOOD: Explicit type hints
def scrape_match(
    self,
    home_team: str,
    away_team: str,
    match_date: str
) -> Dict[str, Any]:
    """Scrape a single match."""
    pass

# ❌ BAD: No type hints
def scrape_match(self, home_team, away_team, match_date):
    pass

# ✅ GOOD: Use typing module
from typing import Dict, List, Optional, Tuple, Any

def extract_stats(
    soup: BeautifulSoup,
    page_text: str
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    pass
```

### Configuration Management

```python
# ✅ GOOD: Use config objects
config = ScraperConfig.from_yaml('config.yml')
scraper = RugbyStatsScraper(config)

# ❌ BAD: Hardcoded values
scraper = RugbyStatsScraper(
    api_key="hardcoded",  # ❌
    max_retries=3,        # ❌
    headless=False        # ❌
)
```

### Error Handling

```python
# ✅ GOOD: Specific exceptions with context
try:
    data = self.extract_stats(soup, text)
except ValueError as e:
    logger.error(f"Failed to extract stats for match {match_id}: {e}")
    return ScrapedData(success=False, error=str(e))

# ❌ BAD: Broad exception catching
try:
    data = self.extract_stats(soup, text)
except:  # ❌ Too broad
    pass  # ❌ Silent failure
```

---

## Agent Usage Guide

### Understanding the Agent System

This project uses specialized AI agents (defined in `agents.md`) for different tasks:

1. **LLM Intelligence Agent** 🧠 - Framework development, LLM integration
2. **Data Collection Agent** 🔍 - Web scraping implementation
3. **Data Architecture Agent** 🏗️ - Data models, schemas
4. **Data Analysis Agent** 📊 - Analytics and insights
5. **Project Manager Agent** 📋 - Planning and documentation
6. **Quality Assurance Agent** ✅ - Testing and validation
7. **Integration Agent** 🔌 - External integrations
8. **Performance Optimization Agent** ⚡ - Speed and efficiency

### When to Use Which Agent

#### Framework Development
**Agent:** LLM Intelligence Agent 🧠
```
"I need to add support for OpenAI API in addition to Gemini.
Update llm_scraper/core/llm_agent.py to support both providers."
```

#### Domain Implementation
**Agent:** Data Collection Agent 🔍
```
"Create a football scraper by extending BaseLLMScraper.
Use rugby_scraper/ as a reference."
```

#### Data Modeling
**Agent:** Data Architecture Agent 🏗️
```
"Design the schema for storing player positions and
substitute events in the match data."
```

#### Code Quality
**Agent:** Quality Assurance Agent ✅
```
"Review the extraction logic in rugby_scraper/extractors.py
and add validation rules."
```

### Agent Handoff Protocol

When switching between agents:

```
FROM: [Agent Name]
TO: [Agent Name]
TASK: [Brief description]
CONTEXT: [Relevant information]
FILES: [List of affected files]
STATUS: [Current state]
```

**Example:**
```
FROM: LLM Intelligence Agent
TO: Data Collection Agent
TASK: Implement cricket scraper using the framework
CONTEXT: Framework is ready, need domain-specific implementation
FILES: cricket_scraper/cricket_scraper.py (to be created)
STATUS: Framework complete, ready for new domain
```

---

## Commit Message Conventions

Follow **conventional commits**:

```bash
# Feature addition
feat: Add support for OpenAI API in LLM agent

# Bug fix
fix: Resolve circular import in schemas.py

# Refactoring
refactor: Extract browser utilities into separate module

# Documentation
docs: Add framework development guide

# Tests
test: Add unit tests for PairwiseStatExtractor

# Chore (dependencies, config)
chore: Update dependencies to latest versions

# Performance improvement
perf: Cache LLM responses to reduce API calls
```

### Commit Message Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**
```
feat(framework): Add support for multiple LLM providers

- Add provider abstraction in llm_agent.py
- Support Gemini, OpenAI, and Anthropic
- Update config to specify provider
- Add provider-specific error handling

Closes #42
```

---

## Before Committing Checklist

### Every Commit Should:

- ✅ **Syntax check:** `python -m py_compile *.py`
- ✅ **Import test:** Verify all imports work
- ✅ **Manual test:** Test the changed functionality
- ✅ **Check logs:** No new errors in console
- ✅ **Review diff:** `git diff` - understand every change
- ✅ **Clear message:** Descriptive commit message
- ✅ **Update docs:** If API/behavior changed

### Pre-Commit Commands

```bash
# Check syntax for all modified Python files
git diff --name-only | grep '\.py$' | xargs -I {} python -m py_compile {}

# Check for common issues
git diff --check

# Review changes
git diff

# Stage files
git add <files>

# Commit with message
git commit -m "feat: Add new feature"
```

---

## Tips for Effective Claude Collaboration

### Do's ✅

- ✅ **Be specific** about what you want
- ✅ **Provide context** about the current task
- ✅ **Reference files** by path (llm_scraper/core/base_scraper.py)
- ✅ **Ask for explanations** when needed
- ✅ **Request modular solutions** for complex features
- ✅ **Break down large tasks** into smaller steps
- ✅ **Review generated code** before committing
- ✅ **Specify which agent** to use for the task

### Don'ts ❌

- ❌ Don't ask vague questions like "fix everything"
- ❌ Don't skip testing AI-generated code
- ❌ Don't commit without reviewing changes
- ❌ Don't create huge files (>400 lines) without planning
- ❌ Don't ignore import errors or warnings
- ❌ Don't forget to document complex changes
- ❌ Don't mix framework and domain logic

### Example Prompts

#### ✅ GOOD Prompts

```
"I need to add a cricket scraper. The framework is in llm_scraper/.
Please:
1. Create cricket_scraper/ directory
2. Implement CricketScraper extending BaseLLMScraper
3. Implement get_planning_prompt() for cricket
4. Create CricketStatsExtractor for extracting scores
Let's start with step 1."
```

```
"The LLM validation in llm_scraper/core/llm_agent.py is failing
for matches with missing data. Read that file and the
ValidationResult schema, then help me add better handling
for partial data."
```

```
"Review rugby_scraper/extractors.py and suggest optimizations
for the regex patterns. Focus on performance and readability."
```

#### ❌ BAD Prompts

```
"Add cricket"  # ❌ Too vague
```

```
"Fix the scraper"  # ❌ Which scraper? What's broken?
```

```
"Make it better"  # ❌ What aspect?
```

---

## Maintenance Checklist

### Monthly

- ✅ Review and refactor modules >300 lines
- ✅ Update dependencies (`pip list --outdated`)
- ✅ Check for unused imports (`pylint --disable=all --enable=unused-import`)
- ✅ Review and update documentation
- ✅ Clean up commented code
- ✅ Review agent decision logs for patterns

### Before Major Features

- ✅ Plan module structure
- ✅ Estimate file sizes
- ✅ Consider extraction needs
- ✅ Document design decisions
- ✅ Choose appropriate agent
- ✅ Review existing similar implementations

### After Refactoring

- ✅ Verify syntax (`python -m py_compile`)
- ✅ Test all affected features
- ✅ Update imports across project
- ✅ Update documentation
- ✅ Commit with clear message
- ✅ Update agents.md if workflow changed

---

## Testing Guidelines

### Manual Testing

```bash
# Test rugby scraper
python run_rugby_scraper.py --matches-file matches_to_scrape.json

# Test with config file
python run_rugby_scraper.py --config rugby_scraper/config.yml --headless

# Test imports
python -c "from llm_scraper.core.base_scraper import BaseLLMScraper; print('OK')"
```

### Unit Testing (Future)

```python
# tests/test_extractors.py
import pytest
from rugby_scraper.extractors import RugbyStatsExtractor

def test_extract_score():
    extractor = RugbyStatsExtractor()
    score = extractor._extract_score("Final Score: 25 - 18")
    assert score == (25, 18)

def test_extract_tries():
    extractor = RugbyStatsExtractor()
    # Test extraction logic
```

---

## Code Review Checklist

### Before Requesting Review

- ✅ Code follows project structure (framework vs domain)
- ✅ Proper type hints on functions
- ✅ Docstrings on classes and complex functions
- ✅ No hardcoded values (use config)
- ✅ Error handling implemented
- ✅ Logging added for important operations
- ✅ No circular imports
- ✅ Files are reasonable size (<400 lines)

### Review Focus Areas

- ✅ **Architecture:** Is it in the right place? (framework vs domain)
- ✅ **Modularity:** Could this be split into smaller pieces?
- ✅ **Reusability:** Can this be used by other scrapers?
- ✅ **Error handling:** What happens when things fail?
- ✅ **Documentation:** Can someone understand this in 6 months?
- ✅ **Testing:** How do we verify this works?

---

## Resources

### Python Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Real Python Tutorials](https://realpython.com/)

### LLM Development
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

### Web Scraping
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Project-Specific
- [FRAMEWORK.md](docs/FRAMEWORK.md) - Framework development guide
- [agents.md](agents.md) - Agent system documentation
- [README.md](README.md) - Project overview

---

## Questions?

If you encounter issues or have questions:

1. ✅ **Check this guide first**
2. ✅ **Review existing code** for patterns
3. ✅ **Search codebase** with grep/glob
4. ✅ **Consult agents.md** for the right agent
5. ✅ **Ask Claude** with specific context
6. ✅ **Document the solution** for future reference

---

## Version History

- **v1.0** (2025-11-14) - Initial guide based on StudentLeaderboardClaude
- Adapted for Python/web scraping project
- Added framework-specific guidelines
- Added agent usage guide

---

**Last Updated:** November 14, 2025
**Maintained By:** Project Manager Agent
**Based On:** StudentLeaderboardClaude development guide
