"""Tools for Solar specialist agent."""

from typing import Dict, Any


def calculate_solar_savings(
    monthly_electric_bill: float,
    location: str = "US",
    roof_size_sqft: int = 1000,
) -> Dict[str, Any]:
    """Calculate potential solar energy savings."""
    # Simplified calculation
    avg_cost_per_watt = 3.0
    system_size_kw = roof_size_sqft / 100  # Rough estimate: 100 sqft per kW
    installation_cost = system_size_kw * 1000 * avg_cost_per_watt

    annual_production_kwh = system_size_kw * 1200  # Rough estimate
    annual_savings = monthly_electric_bill * 12 * 0.7  # 70% offset typical

    payback_years = installation_cost / annual_savings if annual_savings > 0 else 0

    return {
        "system_size_kw": round(system_size_kw, 1),
        "estimated_cost": round(installation_cost, 0),
        "annual_savings": round(annual_savings, 0),
        "payback_period_years": round(payback_years, 1),
        "25_year_savings": round(annual_savings * 25 - installation_cost, 0),
        "federal_tax_credit": round(installation_cost * 0.30, 0),  # 30% ITC
    }


def check_solar_incentives(state: str = "US", system_size_kw: float = 10) -> Dict[str, Any]:
    """Check available solar incentives and rebates."""
    installation_cost = system_size_kw * 1000 * 3.0

    return {
        "federal_tax_credit": {
            "percentage": 30,
            "amount": round(installation_cost * 0.30, 0),
            "expires": "2032",
        },
        "state_incentives": "Varies by state - check DSIRE database",
        "net_metering": "Available in most states",
        "estimated_total_incentive": round(installation_cost * 0.35, 0),
    }


def assess_roof_solar_suitability(
    roof_direction: str,
    roof_age: int,
    shading: str = "none",
) -> Dict[str, Any]:
    """Assess if roof is suitable for solar installation."""
    # Optimal directions
    optimal_directions = ["south", "southwest", "southeast"]
    direction_lower = roof_direction.lower()

    is_optimal = any(d in direction_lower for d in optimal_directions)

    return {
        "suitable": is_optimal and roof_age < 15 and shading != "heavy",
        "roof_direction": roof_direction,
        "direction_rating": "Excellent" if is_optimal else "Good" if "west" in direction_lower or "east" in direction_lower else "Poor",
        "roof_age_concern": roof_age > 10,
        "shading_concern": shading != "none",
        "recommendations": [
            "Consider roof replacement first" if roof_age > 15 else "Roof age is good",
            "Tree trimming may improve output" if shading != "none" else "Minimal shading is ideal",
        ],
    }


solar_tools = [calculate_solar_savings, check_solar_incentives, assess_roof_solar_suitability]
