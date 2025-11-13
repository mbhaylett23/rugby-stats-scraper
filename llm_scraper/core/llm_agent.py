"""
LLM Agent for intelligent decision-making in web scraping.

This module handles all interactions with the Language Model, including:
- Generating scraping plans
- Validating scraped data
- Making decisions (accept/retry/reject)
- Suggesting corrections
"""

import json
import logging
from typing import Dict, Any, Optional
import google.generativeai as genai

from llm_scraper.models.schemas import (
    ScrapingPlan,
    ValidationResult,
    AgentDecision,
    CorrectionSuggestion
)

logger = logging.getLogger(__name__)


class LLMAgent:
    """
    Handles all LLM interactions for the scraping workflow.

    The agent uses structured prompts to get the LLM to:
    1. Plan how to find and scrape content
    2. Validate that scraped data is correct
    3. Decide whether to accept, retry, or reject
    4. Suggest corrections for retry attempts
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the LLM agent.

        Args:
            api_key: API key for the LLM service
            model_name: Name of the model to use
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        logger.info(f"✓ LLM Agent initialized with model: {model_name}")

    def generate_plan(
        self,
        target_info: Dict[str, Any],
        attempt: int,
        domain_prompt: str
    ) -> ScrapingPlan:
        """
        Ask LLM to create a scraping plan.

        Args:
            target_info: Information about what to scrape
            attempt: Current attempt number
            domain_prompt: Domain-specific instructions for planning

        Returns:
            ScrapingPlan with strategy and URL to try
        """
        prompt = f"""
You are an intelligent web scraping planning agent.

{domain_prompt}

TARGET INFORMATION:
{json.dumps(target_info, indent=2)}

ATTEMPT: {attempt}

OUTPUT FORMAT (JSON):
{{
  "strategy": "direct_url" or "construct_url" or "search_required",
  "url_to_try": "full URL to attempt",
  "reasoning": "why this approach",
  "team_name_adjustments": {{"key": "adjusted value"}},
  "additional_metadata": {{"any": "other useful info"}}
}}

Return ONLY valid JSON, no other text.
"""

        try:
            response = self.model.generate_content(prompt)
            plan_data = self._parse_json_response(response.text)
            plan = ScrapingPlan.from_dict(plan_data)

            logger.info(f"  Strategy: {plan.strategy.value}")
            logger.info(f"  URL: {plan.url_to_try}")
            logger.info(f"  Reasoning: {plan.reasoning}")

            return plan

        except Exception as e:
            logger.error(f"Error generating plan: {e}")
            raise

    def validate_data(
        self,
        target_info: Dict[str, Any],
        scraped_data: Dict[str, Any],
        page_sample: str,
        domain_prompt: str
    ) -> ValidationResult:
        """
        Ask LLM to validate scraped data.

        Args:
            target_info: Expected target information
            scraped_data: The data that was scraped
            page_sample: Sample of page content
            domain_prompt: Domain-specific validation instructions

        Returns:
            ValidationResult with assessment
        """
        prompt = f"""
You are a data validation agent for web scraping.

{domain_prompt}

EXPECTED TARGET:
{json.dumps(target_info, indent=2)}

SCRAPED DATA:
{json.dumps(scraped_data, indent=2)}

PAGE CONTENT SAMPLE:
{page_sample[:1000]}

OUTPUT FORMAT (JSON):
{{
  "is_valid": true/false,
  "confidence": 0-100,
  "issues": ["list of issues found"],
  "missing_stats": ["list of missing important data"],
  "suspicious_values": ["list of suspicious values"],
  "overall_assessment": "brief assessment"
}}

Return ONLY valid JSON, no other text.
"""

        try:
            response = self.model.generate_content(prompt)
            validation_data = self._parse_json_response(response.text)
            validation = ValidationResult.from_dict(validation_data)

            logger.info(f"  Valid: {validation.is_valid}")
            logger.info(f"  Confidence: {validation.confidence}%")
            logger.info(f"  Assessment: {validation.overall_assessment}")

            if validation.issues:
                logger.warning(f"  Issues: {', '.join(validation.issues)}")

            return validation

        except Exception as e:
            logger.error(f"Error validating data: {e}")
            raise

    def make_decision(
        self,
        validation: ValidationResult,
        confidence_threshold: int = 80,
        domain_prompt: Optional[str] = None
    ) -> AgentDecision:
        """
        Ask LLM to decide what to do based on validation.

        Args:
            validation: The validation result
            confidence_threshold: Minimum confidence to accept
            domain_prompt: Optional domain-specific decision criteria

        Returns:
            AgentDecision with action to take
        """
        domain_criteria = domain_prompt or ""

        prompt = f"""
You are a decision-making agent for web scraping.

TASK: Decide what to do based on validation results.

VALIDATION RESULTS:
{json.dumps({
    'is_valid': validation.is_valid,
    'confidence': validation.confidence,
    'issues': validation.issues,
    'missing_data': validation.missing_data,
    'suspicious_values': validation.suspicious_values,
    'overall_assessment': validation.overall_assessment
}, indent=2)}

DECISION OPTIONS:
1. ACCEPT - Data is good enough, proceed with it
2. RETRY - Try again with corrections
3. REJECT - Data is unusable, give up

DECISION CRITERIA:
- ACCEPT if: is_valid=true OR confidence≥{confidence_threshold} with minor issues
- RETRY if: confidence between 40-{confidence_threshold-1} OR fixable issues identified
- REJECT if: confidence<40 OR unfixable issues

{domain_criteria}

OUTPUT FORMAT (JSON):
{{
  "action": "ACCEPT" or "RETRY" or "REJECT",
  "reason": "explanation for decision",
  "suggested_fixes": ["list of fixes to try if RETRY"]
}}

Return ONLY valid JSON, no other text.
"""

        try:
            response = self.model.generate_content(prompt)
            decision_data = self._parse_json_response(response.text)
            decision = AgentDecision.from_dict(decision_data)

            logger.info(f"  Decision: {decision.action.value}")
            logger.info(f"  Reason: {decision.reason}")

            return decision

        except Exception as e:
            logger.error(f"Error making decision: {e}")
            raise

    def suggest_corrections(
        self,
        target_info: Dict[str, Any],
        validation: ValidationResult,
        decision: AgentDecision,
        domain_prompt: str
    ) -> CorrectionSuggestion:
        """
        Ask LLM to suggest corrections for retry.

        Args:
            target_info: Current target information
            validation: Validation results
            decision: Decision that was made
            domain_prompt: Domain-specific correction guidance

        Returns:
            CorrectionSuggestion with updated target info
        """
        prompt = f"""
You are a problem-solving agent for web scraping.

{domain_prompt}

CURRENT TARGET INFO:
{json.dumps(target_info, indent=2)}

VALIDATION ISSUES:
{json.dumps(validation.issues, indent=2)}

SUGGESTED FIXES:
{json.dumps(decision.suggested_fixes, indent=2)}

OUTPUT FORMAT (JSON):
{{
  "updated_target_info": {{
    "key": "corrected value",
    "...": "update any relevant fields"
  }},
  "reasoning": "why these corrections",
  "alternative_strategies": ["other approaches to try"]
}}

Return ONLY valid JSON, no other text.
"""

        try:
            response = self.model.generate_content(prompt)
            correction_data = self._parse_json_response(response.text)
            correction = CorrectionSuggestion.from_dict(correction_data)

            logger.info(f"  Corrections: {correction.reasoning}")

            return correction

        except Exception as e:
            logger.error(f"Error suggesting corrections: {e}")
            raise

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response, handling markdown code blocks.

        Args:
            response_text: Raw response from LLM

        Returns:
            Parsed JSON dictionary
        """
        # Remove markdown code blocks if present
        cleaned = response_text.strip()
        cleaned = cleaned.replace('```json', '').replace('```', '').strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {response_text}")
            raise ValueError(f"Invalid JSON from LLM: {e}")
