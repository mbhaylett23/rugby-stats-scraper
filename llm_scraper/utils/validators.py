"""
Data validation utilities for scraped data.

Provides base classes and common validation patterns.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class BaseValidator(ABC):
    """
    Abstract base class for data validators.

    Validators check if scraped data meets quality standards.
    """

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data.

        Args:
            data: Data to validate

        Returns:
            Dictionary with validation results:
            {
                'is_valid': bool,
                'issues': List[str],
                'warnings': List[str]
            }
        """
        pass


class FieldPresenceValidator(BaseValidator):
    """
    Validates that required fields are present and non-empty.
    """

    def __init__(self, required_fields: List[str], optional_fields: List[str] = None):
        """
        Initialize validator.

        Args:
            required_fields: Fields that must be present
            optional_fields: Fields that are nice to have but not required
        """
        self.required_fields = required_fields
        self.optional_fields = optional_fields or []

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if required fields are present.

        Args:
            data: Data to validate

        Returns:
            Validation results
        """
        issues = []
        warnings = []

        # Check required fields
        for field in self.required_fields:
            if field not in data:
                issues.append(f"Missing required field: {field}")
            elif data[field] is None or data[field] == '':
                issues.append(f"Required field is empty: {field}")

        # Check optional fields
        for field in self.optional_fields:
            if field not in data or data[field] is None:
                warnings.append(f"Optional field missing: {field}")

        is_valid = len(issues) == 0

        return {
            'is_valid': is_valid,
            'issues': issues,
            'warnings': warnings
        }


class NumericRangeValidator(BaseValidator):
    """
    Validates that numeric fields are within expected ranges.
    """

    def __init__(self, field_ranges: Dict[str, tuple]):
        """
        Initialize validator.

        Args:
            field_ranges: Dictionary mapping field names to (min, max) tuples
        """
        self.field_ranges = field_ranges

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if numeric fields are in valid ranges.

        Args:
            data: Data to validate

        Returns:
            Validation results
        """
        issues = []
        warnings = []

        for field, (min_val, max_val) in self.field_ranges.items():
            if field not in data:
                continue

            value = data[field]

            # Skip if None
            if value is None:
                continue

            # Try to convert to float
            try:
                value = float(value)
            except (ValueError, TypeError):
                issues.append(f"Field {field} is not numeric: {value}")
                continue

            # Check range
            if min_val is not None and value < min_val:
                issues.append(f"Field {field} below minimum: {value} < {min_val}")
            elif max_val is not None and value > max_val:
                issues.append(f"Field {field} above maximum: {value} > {max_val}")

        is_valid = len(issues) == 0

        return {
            'is_valid': is_valid,
            'issues': issues,
            'warnings': warnings
        }


class LogicalConsistencyValidator(BaseValidator):
    """
    Validates logical consistency between related fields.

    Example: For sports stats, tries * conversion_points should be <= total_points
    """

    def __init__(self, consistency_rules: List[Dict[str, Any]]):
        """
        Initialize validator.

        Args:
            consistency_rules: List of rule dictionaries with:
                - 'description': Rule description
                - 'check': Callable that takes data and returns bool
        """
        self.consistency_rules = consistency_rules

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check logical consistency rules.

        Args:
            data: Data to validate

        Returns:
            Validation results
        """
        issues = []
        warnings = []

        for rule in self.consistency_rules:
            try:
                if not rule['check'](data):
                    issues.append(f"Consistency check failed: {rule['description']}")
            except Exception as e:
                warnings.append(f"Could not check rule '{rule['description']}': {e}")

        is_valid = len(issues) == 0

        return {
            'is_valid': is_valid,
            'issues': issues,
            'warnings': warnings
        }


class CompositeValidator(BaseValidator):
    """
    Combines multiple validators.
    """

    def __init__(self, validators: List[BaseValidator]):
        """
        Initialize composite validator.

        Args:
            validators: List of validators to run
        """
        self.validators = validators

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all validators and combine results.

        Args:
            data: Data to validate

        Returns:
            Combined validation results
        """
        all_issues = []
        all_warnings = []

        for validator in self.validators:
            result = validator.validate(data)
            all_issues.extend(result.get('issues', []))
            all_warnings.extend(result.get('warnings', []))

        is_valid = len(all_issues) == 0

        return {
            'is_valid': is_valid,
            'issues': all_issues,
            'warnings': all_warnings
        }
