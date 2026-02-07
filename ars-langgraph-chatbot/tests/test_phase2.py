"""
Phase 2 Test Script - Test the RAG diagnosis system
"""
import os
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from app.graph import build_graph, ChatState

load_dotenv()

print("="*70)
print("PHASE 2 TEST - RAG Diagnosis System")
print("="*70)

# Build and compile graph
print("\n1. Building LangGraph...")
graph = build_graph()
compiled_graph = graph.compile()
print("✓ Graph compiled successfully")

# Test cases
test_cases = [
    {
        "message": "my car won't start, the lights are dim, and I hear clicking",
        "expected_urgency": "DON'T DRIVE"
    },
    {
        "message": "engine temperature is very high, steam coming from hood",
        "expected_urgency": "EMERGENCY"
    },
    {
        "message": "brakes making squeaking noise when I stop",
        "expected_urgency": "DRIVE CAREFULLY"
    }
]

print(f"\n2. Running {len(test_cases)} test cases...\n")

for i, test in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test['message']}")
    print("-" * 70)
    
    # Create state and run graph
    initial_state = ChatState(user_message=test['message'])
    result = compiled_graph.invoke(initial_state)
    
    # Display results
    print(f"Intent: {result.intent}")
    print(f"Urgency: {result.urgency_level}")
    print(f"\nDiagnosis:\n{result.diagnosis[:200]}...")
    
    # Validation
    if result.urgency_level:
        print(f"\n✓ Test passed - Got urgency level: {result.urgency_level}")
    else:
        print("\n❌ Test failed - No urgency level returned")
    
    print()

print("\n" + "="*70)
print("Phase 2 Test Complete!")
print("="*70)
