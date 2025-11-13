"""
Phase execution for the 5-phase LLM scraping workflow.

Phases:
1. PLAN - Create scraping plan
2. SCRAPE - Execute the plan
3. VALIDATE - Check data quality
4. DECIDE - Choose action (accept/retry/reject)
5. CORRECT - Suggest fixes for retry
"""

import logging
import time
from typing import Dict, Any, Optional, Tuple

from llm_scraper.core.llm_agent import LLMAgent
from llm_scraper.models.schemas import (
    ScrapingPlan,
    ScrapedData,
    ValidationResult,
    AgentDecision,
    CorrectionSuggestion,
    DecisionAction
)

logger = logging.getLogger(__name__)


class PhaseExecutor:
    """
    Executes the 5-phase workflow for intelligent scraping.

    This class coordinates between the LLM agent and the scraper
    to execute each phase of the workflow.
    """

    def __init__(
        self,
        llm_agent: LLMAgent,
        scraper_instance: Any,  # The actual scraper implementation
        config: Any  # ScraperConfig
    ):
        """
        Initialize the phase executor.

        Args:
            llm_agent: LLM agent for decision-making
            scraper_instance: Instance of scraper implementation
            config: Configuration object
        """
        self.llm_agent = llm_agent
        self.scraper = scraper_instance
        self.config = config
        self.agent_log = []

    def execute_workflow(
        self,
        target_info: Dict[str, Any]
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Execute the complete 5-phase workflow with retries.

        Args:
            target_info: Information about what to scrape

        Returns:
            Tuple of (success, result_data)
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"AGENT WORKFLOW: {self._format_target(target_info)}")
        logger.info(f"{'='*80}\n")

        attempt = 0
        max_retries = self.config.max_retries

        while attempt < max_retries:
            attempt += 1
            logger.info(f"\n--- Attempt {attempt}/{max_retries} ---")

            # PHASE 1: PLAN
            plan = self.phase_1_plan(target_info, attempt)
            if plan is None:
                continue

            # PHASE 2: SCRAPE
            scraped_data = self.phase_2_scrape(plan)
            if not scraped_data.success:
                logger.warning(f"Scraping failed: {scraped_data.error}")
                time.sleep(self.config.retry_delay)
                continue

            # PHASE 3: VALIDATE
            validation = self.phase_3_validate(target_info, scraped_data)
            if validation is None:
                continue

            # PHASE 4: DECIDE
            decision = self.phase_4_decide(validation)
            if decision is None:
                continue

            # Handle decision
            if decision.action == DecisionAction.ACCEPT:
                logger.info("✓ Agent decision: ACCEPT - Data is valid!")
                return True, {
                    'success': True,
                    'data': scraped_data.data,
                    'metadata': scraped_data.metadata,
                    'agent_log': self.agent_log
                }

            elif decision.action == DecisionAction.RETRY:
                logger.info(f"⟳ Agent decision: RETRY - {decision.reason}")
                # PHASE 5: CORRECT
                target_info = self.phase_5_correct(target_info, decision, validation)
                time.sleep(self.config.retry_delay)
                continue

            elif decision.action == DecisionAction.REJECT:
                logger.error(f"✗ Agent decision: REJECT - {decision.reason}")
                break

        # Failed after all retries
        logger.error("✗ Failed after maximum retries")
        return False, {
            'success': False,
            'error': 'Failed after maximum retries',
            'agent_log': self.agent_log
        }

    def phase_1_plan(
        self,
        target_info: Dict[str, Any],
        attempt: int
    ) -> Optional[ScrapingPlan]:
        """
        PHASE 1: Create a scraping plan using LLM.

        Args:
            target_info: Information about scraping target
            attempt: Current attempt number

        Returns:
            ScrapingPlan or None if planning fails
        """
        logger.info("PHASE 1: PLANNING")

        try:
            # Get domain-specific planning prompt
            planning_prompt = self.scraper.get_planning_prompt()

            # Ask LLM to create plan
            plan = self.llm_agent.generate_plan(
                target_info=target_info,
                attempt=attempt,
                domain_prompt=planning_prompt
            )

            # Log the plan
            self.agent_log.append({
                'phase': 'PLAN',
                'attempt': attempt,
                'plan': {
                    'strategy': plan.strategy.value,
                    'url': plan.url_to_try,
                    'reasoning': plan.reasoning
                }
            })

            return plan

        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return None

    def phase_2_scrape(
        self,
        plan: ScrapingPlan
    ) -> ScrapedData:
        """
        PHASE 2: Execute the scraping plan.

        Args:
            plan: The scraping plan to execute

        Returns:
            ScrapedData with results
        """
        logger.info("PHASE 2: SCRAPING")

        try:
            # Call domain-specific scraping logic
            scraped_data = self.scraper.execute_scraping(plan)

            return scraped_data

        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            return ScrapedData(
                success=False,
                error=str(e)
            )

    def phase_3_validate(
        self,
        target_info: Dict[str, Any],
        scraped_data: ScrapedData
    ) -> Optional[ValidationResult]:
        """
        PHASE 3: Validate scraped data using LLM.

        Args:
            target_info: Expected target information
            scraped_data: The scraped data to validate

        Returns:
            ValidationResult or None if validation fails
        """
        logger.info("PHASE 3: VALIDATING")

        try:
            # Get domain-specific validation prompt
            validation_prompt = self.scraper.get_validation_prompt()

            # Ask LLM to validate
            validation = self.llm_agent.validate_data(
                target_info=target_info,
                scraped_data=scraped_data.data,
                page_sample=scraped_data.page_content_sample or "",
                domain_prompt=validation_prompt
            )

            # Log validation
            self.agent_log.append({
                'phase': 'VALIDATE',
                'validation': {
                    'is_valid': validation.is_valid,
                    'confidence': validation.confidence,
                    'assessment': validation.overall_assessment
                }
            })

            return validation

        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return None

    def phase_4_decide(
        self,
        validation: ValidationResult
    ) -> Optional[AgentDecision]:
        """
        PHASE 4: Decide what to do based on validation.

        Args:
            validation: Validation results

        Returns:
            AgentDecision or None if decision fails
        """
        logger.info("PHASE 4: DECIDING")

        try:
            # Get optional domain-specific decision criteria
            decision_prompt = self.scraper.get_decision_prompt()

            # Ask LLM to decide
            decision = self.llm_agent.make_decision(
                validation=validation,
                confidence_threshold=self.config.confidence_threshold,
                domain_prompt=decision_prompt
            )

            # Log decision
            self.agent_log.append({
                'phase': 'DECIDE',
                'decision': {
                    'action': decision.action.value,
                    'reason': decision.reason
                }
            })

            return decision

        except Exception as e:
            logger.error(f"Decision failed: {e}")
            return None

    def phase_5_correct(
        self,
        target_info: Dict[str, Any],
        decision: AgentDecision,
        validation: ValidationResult
    ) -> Dict[str, Any]:
        """
        PHASE 5: Get correction suggestions from LLM.

        Args:
            target_info: Current target information
            decision: The decision that was made
            validation: Validation results

        Returns:
            Updated target information
        """
        logger.info("PHASE 5: CORRECTING")

        try:
            # Get domain-specific correction prompt
            correction_prompt = self.scraper.get_correction_prompt()

            # Ask LLM for corrections
            correction = self.llm_agent.suggest_corrections(
                target_info=target_info,
                validation=validation,
                decision=decision,
                domain_prompt=correction_prompt
            )

            # Update target info with corrections
            updated_info = target_info.copy()
            updated_info.update(correction.updated_target_info)

            # Log correction
            self.agent_log.append({
                'phase': 'CORRECT',
                'correction': {
                    'reasoning': correction.reasoning,
                    'updated_info': correction.updated_target_info
                }
            })

            return updated_info

        except Exception as e:
            logger.error(f"Correction failed: {e}")
            return target_info

    def _format_target(self, target_info: Dict[str, Any]) -> str:
        """Format target info for logging."""
        # Try common formats
        if 'home' in target_info and 'away' in target_info:
            return f"{target_info['home']} vs {target_info['away']}"
        elif 'url' in target_info:
            return target_info['url']
        else:
            return str(target_info)
