"""Tools for HVAC specialist agent."""

from typing import Dict, Any


def check_hvac_system_status(system_type: str, issue_description: str) -> Dict[str, Any]:
    """
    Check HVAC system status and provide diagnostic info.

    Args:
        system_type: Type of system (heating, cooling, both)
        issue_description: Description of the issue

    Returns:
        Diagnostic information
    """
    # TODO: Integrate with knowledge base
    return {
        "system_type": system_type,
        "issue": issue_description,
        "possible_causes": ["Filter needs replacement", "Low refrigerant", "Thermostat issue"],
        "recommended_action": "Schedule inspection",
    }


def get_hvac_maintenance_schedule(last_service_date: str = None) -> Dict[str, Any]:
    """
    Get recommended maintenance schedule for HVAC systems.

    Args:
        last_service_date: Last service date if known

    Returns:
        Maintenance schedule recommendations
    """
    return {
        "recommended_frequency": "Every 6 months",
        "next_service": "Spring (before cooling season)",
        "checklist": [
            "Replace air filters",
            "Check refrigerant levels",
            "Inspect electrical connections",
            "Clean coils",
            "Test thermostat",
        ],
    }


def estimate_hvac_repair_cost(issue_type: str, system_age: int = None) -> Dict[str, Any]:
    """
    Provide cost estimate for HVAC repairs.

    Args:
        issue_type: Type of repair needed
        system_age: Age of system in years

    Returns:
        Cost estimate information
    """
    # TODO: Integrate with pricing database
    estimates = {
        "filter_replacement": (50, 100),
        "refrigerant_recharge": (200, 500),
        "compressor_replacement": (1500, 3000),
        "full_system_replacement": (3000, 8000),
    }

    issue_key = issue_type.lower().replace(" ", "_")
    cost_range = estimates.get(issue_key, (100, 500))

    return {
        "issue_type": issue_type,
        "estimated_cost_min": cost_range[0],
        "estimated_cost_max": cost_range[1],
        "factors": ["System age", "Brand", "Complexity", "Labor costs"],
        "warranty_may_apply": system_age and system_age < 10,
    }


hvac_tools = [check_hvac_system_status, get_hvac_maintenance_schedule, estimate_hvac_repair_cost]
