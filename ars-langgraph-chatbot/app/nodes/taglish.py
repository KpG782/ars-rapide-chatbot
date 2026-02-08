"""
Taglish normalizer - maps Filipino-English terms to English for better semantic matching.
"""
import json
import os
from typing import Dict
from app.graph import ChatState


# Load Taglish dictionary
_taglish_dict = None


def load_taglish_dictionary() -> Dict[str, str]:
    """Load Taglish terms from JSON file."""
    global _taglish_dict
    
    if _taglish_dict is None:
        kb_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "knowledge_base",
            "taglish_terms.json"
        )
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Flatten all sections into single dictionary
        _taglish_dict = {}
        
        # Add car problems section
        if "car_problems_taglish" in data:
            _taglish_dict.update(data["car_problems_taglish"])
        
        # Add symptoms section
        if "symptoms_taglish" in data:
            _taglish_dict.update(data["symptoms_taglish"])
        
        # Add car parts section (lowercase for matching)
        if "car_parts" in data:
            for tagalog, english in data["car_parts"].items():
                _taglish_dict[tagalog.lower()] = english
        
        print(f"✓ Loaded {len(_taglish_dict)} Taglish terms")
    
    return _taglish_dict


def normalize_taglish(text: str) -> str:
    """
    Replace common Taglish terms with English equivalents.
    
    Args:
        text: User input possibly containing Taglish
        
    Returns:
        Text with Taglish terms replaced by English
    """
    taglish_dict = load_taglish_dictionary()
    
    normalized = text.lower()
    
    # Sort by length (longest first) to handle multi-word phrases
    sorted_terms = sorted(taglish_dict.keys(), key=len, reverse=True)
    
    for tagalog_term in sorted_terms:
        english_term = taglish_dict[tagalog_term]
        # Replace the Taglish term with English
        normalized = normalized.replace(tagalog_term, english_term)
    
    return normalized


def preprocess_taglish(state: ChatState) -> ChatState:
    """
    Node that preprocesses user message to normalize Taglish terms.
    This runs BEFORE classification and diagnosis for better semantic matching.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with normalized message stored separately
    """
    original_message = state.user_message
    normalized_message = normalize_taglish(original_message)
    
    # Store both for reference
    # We'll use normalized for RAG but keep original for context
    state.user_message = normalized_message
    
    if normalized_message != original_message.lower():
        print(f"✓ Normalized Taglish: '{original_message}' → '{normalized_message}'")
    
    return state


if __name__ == "__main__":
    # Test the normalizer
    print("Testing Taglish Normalizer...\n")
    
    test_cases = [
        "kumakatok ang engine ko",
        "umiinit ang kotse",
        "mahina ang preno",
        "hindi gumagana ang aircon",
        "may ingay sa gulong",
        "walang kuryente sa dashboard"
    ]
    
    taglish_dict = load_taglish_dictionary()
    
    for test in test_cases:
        normalized = normalize_taglish(test)
        print(f"Original:   '{test}'")
        print(f"Normalized: '{normalized}'")
        print()
