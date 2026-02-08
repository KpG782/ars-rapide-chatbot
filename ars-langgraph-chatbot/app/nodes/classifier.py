"""
Classifier node - determines user intent and routes conversation flow.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph import ChatState
from app.utils.prompts import CLASSIFICATION_PROMPT


def classify_intent(state: ChatState) -> ChatState:
    """
    Classify the user's intent from their message.
    
    Routes to:
    - DIAGNOSIS: User describing car problem/symptoms
    - COST_ESTIMATE: User asking about repair costs
    - BOOKING: User wants to schedule service
    - GENERAL: General inquiry/greeting
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with intent classification
    """
    user_message = state.user_message
    
    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,  # Lower for more consistent classification
        max_tokens=50  # Classification only needs short response
    )
    
    # Format the prompt with user message
    prompt = CLASSIFICATION_PROMPT.format(user_message=user_message)
    
    # Get classification
    response = llm.invoke(prompt)
    intent = response.content.strip().upper()
    
    # Validate intent (must be one of the four options)
    valid_intents = ["DIAGNOSIS", "COST_ESTIMATE", "BOOKING", "GENERAL"]
    if intent not in valid_intents:
        # Default to DIAGNOSIS if unclear
        intent = "DIAGNOSIS"
    
    # Update state
    state.intent = intent
    
    print(f"✓ Classified intent: {intent}")
    
    return state


if __name__ == "__main__":
    # Test the classifier
    from pydantic import BaseModel
    
    test_cases = [
        "my car won't start and the battery light is on",
        "how much does it cost to replace brake pads?",
        "I'd like to book an appointment for next Tuesday",
        "hello, what services do you offer?"
    ]
    
    print("Testing Intent Classifier...\n")
    
    for message in test_cases:
        print(f"Message: '{message}'")
        
        # Create test state
        test_state = ChatState(user_message=message)
        
        # Classify
        result = classify_intent(test_state)
        
        print(f"Intent: {result.intent}")
        print("-" * 60 + "\n")
