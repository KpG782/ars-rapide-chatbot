"""
Diagnosis node - retrieves relevant problems and generates diagnosis using RAG + LLM.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph import ChatState
from app.rag.retriever import get_retriever
from app.utils.prompts import DIAGNOSIS_PROMPT


def diagnose_problem(state: ChatState) -> ChatState:
    """
    Diagnose car problem using RAG (Retrieval-Augmented Generation).
    
    Process:
    1. Retrieve relevant car problems from knowledge base
    2. Inject context into LLM prompt
    3. Generate diagnosis with urgency level
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with diagnosis, urgency, and symptoms
    """
    user_message = state.user_message
    
    # Step 1: Retrieve relevant problems (semantic search)
    retriever = get_retriever(top_k=3)
    results = retriever.retrieve(user_message)
    
    # Format context for LLM
    retrieved_context = retriever.format_context_for_llm(results)
    
    print(f"✓ Retrieved {len(results)} relevant problems from knowledge base")
    
    # Step 2: Generate diagnosis with LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.5  # Balanced for accurate yet natural responses
    )
    
    # Format prompt with user message and retrieved context
    prompt = DIAGNOSIS_PROMPT.format(
        user_message=user_message,
        context=retrieved_context
    )
    
    # Get diagnosis from Gemini
    response = llm.invoke(prompt)
    diagnosis_text = response.content.strip()
    
    # Parse urgency from response (look for EMERGENCY, DON'T DRIVE, etc.)
    urgency = "CAN DRIVE"  # Default
    if "EMERGENCY" in diagnosis_text.upper():
        urgency = "EMERGENCY"
    elif "DON'T DRIVE" in diagnosis_text.upper() or "DO NOT DRIVE" in diagnosis_text.upper():
        urgency = "DON'T DRIVE"
    elif "DRIVE CAREFULLY" in diagnosis_text.upper():
        urgency = "DRIVE CAREFULLY"
    
    # Update state
    state.diagnosis = diagnosis_text
    state.urgency_level = urgency
    state.symptoms = user_message  # Store original symptoms
    
    print(f"✓ Generated diagnosis with urgency: {urgency}")
    
    return state


if __name__ == "__main__":
    # Test the diagnosis node
    print("Testing Diagnosis Node...\n")
    
    test_cases = [
        "my car won't start, the lights are dim, and I hear clicking when I turn the key",
        "engine temperature gauge is in the red zone and steam is coming from the hood",
        "brakes are making a loud squealing noise"
    ]
    
    for message in test_cases:
        print(f"\nSymptoms: '{message}'")
        print("=" * 70)
        
        # Create test state
        test_state = ChatState(user_message=message)
        
        # Diagnose
        result = diagnose_problem(test_state)
        
        print(f"\nDiagnosis:\n{result.diagnosis}")
        print(f"\nUrgency Level: {result.urgency_level}")
        print("\n" + "-" * 70)
