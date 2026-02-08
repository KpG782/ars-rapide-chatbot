"""
Cost estimator node - provides pricing estimates for diagnosed problems.
"""
import json
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph import ChatState
from app.utils.prompts import COST_ESTIMATION_PROMPT


def load_pricing_data() -> list[Dict[str, Any]]:
    """Load pricing data from JSON file."""
    kb_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "knowledge_base",
        "pricing.json"
    )
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_relevant_pricing(diagnosis: str, pricing_data: list) -> list[Dict[str, Any]]:
    """
    Find relevant pricing entries based on diagnosis.
    Simple keyword matching for common services.
    """
    diagnosis_lower = diagnosis.lower()
    relevant = []
    
    # Keywords to pricing mappings
    keyword_map = {
        "battery": ["battery_replacement"],
        "oil": ["oil_change"],
        "brake": ["brake_pad_replacement", "brake_pad_and_disc"],
        "alternator": ["alternator_replacement"],
        "starter": ["starter_motor_replacement"],
        "radiator": ["radiator_replacement"],
        "water pump": ["water_pump_replacement"],
        "coolant": ["coolant_flush"],
        "thermostat": ["thermostat_replacement"],
        "transmission": ["transmission_fluid_change", "transmission_repair"],
        "clutch": ["clutch_replacement"],
        "suspension": ["suspension_repair"],
        "shock": ["shock_absorber_replacement"],
        "tire": ["tire_replacement"],
        "alignment": ["wheel_alignment"],
        "timing belt": ["timing_belt_replacement"],
        "spark plug": ["spark_plug_replacement"]
    }
    
    # Find matching services
    matched_ids = set()
    for keyword, service_ids in keyword_map.items():
        if keyword in diagnosis_lower:
            matched_ids.update(service_ids)
    
    # Get pricing for matched services
    for price_entry in pricing_data:
        if price_entry["service_id"] in matched_ids:
            relevant.append(price_entry)
    
    return relevant[:3]  # Return top 3 relevant


def estimate_cost(state: ChatState) -> ChatState:
    """
    Estimate repair costs based on diagnosis.
    
    Args:
        state: Current conversation state with diagnosis
        
    Returns:
        Updated state with cost estimate
    """
    if not state.diagnosis:
        # No diagnosis yet, skip cost estimation
        return state
    
    # Load pricing data
    pricing_data = load_pricing_data()
    
    # Find relevant pricing
    relevant_pricing = find_relevant_pricing(state.diagnosis, pricing_data)
    
    if not relevant_pricing:
        # No specific pricing found, provide general estimate
        state.cost_estimate = {
            "message": "Cost depends on specific diagnosis. Visit ARS Rapide for accurate quote.",
            "services": []
        }
        print("✓ No specific pricing found, using general estimate")
        return state
    
    # Format pricing context for LLM
    pricing_context = []
    for service in relevant_pricing:
        context = f"""
Service: {service['service_name']}
Description: {service['description']}
Talyer Price: ₱{service['talyer_price_php']['low']:,} - ₱{service['talyer_price_php']['high']:,}
Casa Price: ₱{service['casa_price_php']['low']:,} - ₱{service['casa_price_php']['high']:,}
Duration: {service['duration_minutes']} minutes
Parts: {', '.join(service['parts_included'])}
Notes: {service.get('notes', 'N/A')}
""".strip()
        pricing_context.append(context)
    
    pricing_text = "\n\n---\n\n".join(pricing_context)
    
    # Generate cost estimate with Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.4,  # Balanced for accurate yet natural responses
        max_tokens=200  # Keep cost estimate concise (80-120 words)
    )
    
    prompt = COST_ESTIMATION_PROMPT.format(
        pricing_context=pricing_text,
        diagnosis=state.diagnosis,
        car_details=state.car_details or "Not specified"
    )
    
    response = llm.invoke(prompt)
    cost_text = response.content.strip()
    
    # Store cost estimate
    state.cost_estimate = {
        "message": cost_text,
        "services": relevant_pricing
    }
    
    print(f"✓ Generated cost estimate for {len(relevant_pricing)} services")
    
    return state


if __name__ == "__main__":
    # Test cost estimator
    print("Testing Cost Estimator...\n")
    
    # Load environment variables for testing
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create test state with diagnosis
    test_state = ChatState(
        user_message="my car won't start",
        diagnosis="Dead battery. Needs jump-start or replacement.",
        urgency_level="DON'T DRIVE"
    )
    
    # Estimate cost
    result = estimate_cost(test_state)
    
    print("\nDiagnosis:")
    print(result.diagnosis)
    print("\nCost Estimate:")
    print(result.cost_estimate["message"])
    print("\nRelevant Services:")
    for service in result.cost_estimate["services"]:
        print(f"  - {service['service_name']}")
