"""Tools for Roofing specialist agent."""

from typing import Dict, Any


def assess_roof_damage(damage_description: str, roof_age: int = None) -> Dict[str, Any]:
    """Assess roof damage and provide recommendations."""
    return {
        "damage_type": damage_description,
        "severity": "Moderate",
        "urgent": "storm damage" in damage_description.lower() or "leak" in damage_description.lower(),
        "recommended_action": "Schedule inspection within 48 hours" if "leak" in damage_description.lower() else "Schedule inspection within 1 week",
    }


def estimate_roofing_cost(project_type: str, square_footage: int = 2000) -> Dict[str, Any]:
    """Estimate roofing project costs."""
    cost_per_sqft = {
        "repair": (5, 15),
        "replacement": (5, 12),
        "new_installation": (7, 15),
    }

    project_key = project_type.lower()
    cost_range = cost_per_sqft.get(project_key, (5, 10))

    return {
        "project_type": project_type,
        "square_footage": square_footage,
        "estimated_cost_min": cost_range[0] * square_footage,
        "estimated_cost_max": cost_range[1] * square_footage,
        "factors": ["Material choice", "Roof pitch", "Accessibility", "Removal of old roof"],
    }


def get_roofing_materials_info(material_type: str = None) -> Dict[str, Any]:
    """Get information about roofing materials."""
    materials = {
        "asphalt_shingles": {
            "lifespan": "15-30 years",
            "cost": "Low to Moderate",
            "pros": ["Affordable", "Easy to install", "Variety of colors"],
            "cons": ["Shorter lifespan", "Less eco-friendly"],
        },
        "metal": {
            "lifespan": "40-70 years",
            "cost": "Moderate to High",
            "pros": ["Durable", "Energy efficient", "Low maintenance"],
            "cons": ["Higher upfront cost", "Can be noisy in rain"],
        },
        "tile": {
            "lifespan": "50-100 years",
            "cost": "High",
            "pros": ["Very durable", "Fire resistant", "Beautiful"],
            "cons": ["Heavy", "Expensive", "Requires strong support"],
        },
    }

    if material_type:
        return materials.get(material_type.lower().replace(" ", "_"), materials["asphalt_shingles"])

    return materials


roofing_tools = [assess_roof_damage, estimate_roofing_cost, get_roofing_materials_info]
