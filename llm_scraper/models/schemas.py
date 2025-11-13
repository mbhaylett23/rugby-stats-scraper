"""
Data models and schemas for the LLM scraping framework.

These dataclasses define the structure of data passed between different
phases of the scraping workflow.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class DecisionAction(Enum):
    """Possible actions the agent can decide to take."""
    ACCEPT = "ACCEPT"
    RETRY = "RETRY"
    REJECT = "REJECT"


class ScrapeStrategy(Enum):
    """Strategies for finding and scraping content."""
    DIRECT_URL = "direct_url"
    CONSTRUCT_URL = "construct_url"
    SEARCH_REQUIRED = "search_required"


@dataclass
class ScrapingPlan:
    """
    Plan created by LLM for scraping a target.

    Attributes:
        strategy: The strategy to use for finding content
        url_to_try: The URL to attempt scraping
        reasoning: LLM's explanation for this approach
        adjustments: Any adjustments to make (e.g., team names)
        metadata: Additional metadata for the plan
    """
    strategy: ScrapeStrategy
    url_to_try: str
    reasoning: str
    adjustments: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ScrapingPlan':
        """Create a ScrapingPlan from a dictionary."""
        return cls(
            strategy=ScrapeStrategy(data.get('strategy', 'direct_url')),
            url_to_try=data['url_to_try'],
            reasoning=data['reasoning'],
            adjustments=data.get('team_name_adjustments', {}),
            metadata={k: v for k, v in data.items()
                     if k not in ['strategy', 'url_to_try', 'reasoning', 'team_name_adjustments']}
        )


@dataclass
class ScrapedData:
    """
    Data scraped from a web page.

    Attributes:
        success: Whether scraping succeeded
        url: The URL that was scraped
        data: The extracted data (structure depends on implementation)
        page_content_sample: Sample of page content for validation
        metadata: Additional metadata (game_id, timestamps, etc.)
        error: Error message if scraping failed
    """
    success: bool
    url: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    page_content_sample: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class ValidationResult:
    """
    Result of validating scraped data.

    Attributes:
        is_valid: Whether data passes validation
        confidence: Confidence level (0-100)
        issues: List of issues found
        missing_data: List of missing required fields
        suspicious_values: List of suspicious values detected
        overall_assessment: Summary assessment from LLM
    """
    is_valid: bool
    confidence: int
    issues: List[str] = field(default_factory=list)
    missing_data: List[str] = field(default_factory=list)
    suspicious_values: List[str] = field(default_factory=list)
    overall_assessment: str = ""

    @classmethod
    def from_dict(cls, data: Dict) -> 'ValidationResult':
        """Create a ValidationResult from a dictionary."""
        return cls(
            is_valid=data['is_valid'],
            confidence=data['confidence'],
            issues=data.get('issues', []),
            missing_data=data.get('missing_stats', []),
            suspicious_values=data.get('suspicious_values', []),
            overall_assessment=data.get('overall_assessment', '')
        )


@dataclass
class AgentDecision:
    """
    Decision made by the agent on how to proceed.

    Attributes:
        action: The action to take (ACCEPT, RETRY, REJECT)
        reason: Explanation for the decision
        suggested_fixes: List of fixes to try if action is RETRY
        metadata: Additional decision metadata
    """
    action: DecisionAction
    reason: str
    suggested_fixes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentDecision':
        """Create an AgentDecision from a dictionary."""
        return cls(
            action=DecisionAction(data['action']),
            reason=data['reason'],
            suggested_fixes=data.get('suggested_fixes', []),
            metadata={k: v for k, v in data.items()
                     if k not in ['action', 'reason', 'suggested_fixes']}
        )


@dataclass
class CorrectionSuggestion:
    """
    Corrections suggested by the agent for retry attempts.

    Attributes:
        updated_target_info: Updated information about the scraping target
        reasoning: Explanation for these corrections
        alternative_strategies: Alternative strategies to try
    """
    updated_target_info: Dict[str, Any]
    reasoning: str
    alternative_strategies: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> 'CorrectionSuggestion':
        """Create a CorrectionSuggestion from a dictionary."""
        return cls(
            updated_target_info=data.get('updated_match_info', data.get('updated_target_info', {})),
            reasoning=data['reasoning'],
            alternative_strategies=data.get('alternative_strategies', [])
        )
