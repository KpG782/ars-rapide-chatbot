"""
ARS Rapide Chatbot — Main Entry Point
Validates environment and starts the application.
"""

import warnings
# Suppress Pydantic V1 deprecation warning (known issue with LangChain + Python 3.14)
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core._api.deprecation")

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir.parent))

from app.graph import build_graph, ChatState


def validate_environment() -> None:
    """Validate that all required environment variables are set."""
    required_vars = ["GOOGLE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Copy .env.example to .env and fill in your API keys")
        print("   Get your Google API key at: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    print("✓ Environment validated")


def main() -> None:
    """Main application entry point."""
    # Load environment variables
    load_dotenv()
    
    # Validate environment
    validate_environment()
    
    # Build the graph
    graph = build_graph()
    compiled_graph = graph.compile()
    
    print("✓ ARS Rapide Chatbot ready")
    print("\n" + "="*60)
    print("Phase 3 — Cost Estimation & Taglish: Interactive Mode")
    print("="*60)
    print("\nDescribe your car problem and get instant diagnosis with pricing!")
    print("Type 'quit' or 'exit' to stop.\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thanks for using ARS Rapide Chatbot!")
                break
            
            # Create initial state
            initial_state = ChatState(user_message=user_input)
            
            # Run the graph
            print("\n🔄 Processing...")
            result = compiled_graph.invoke(initial_state)
            
            # Display results
            print("\n" + "-"*60)
            if result.get("diagnosis"):
                print(f"🔧 DIAGNOSIS:\n{result['diagnosis']}\n")
                
                # Display confidence if available
                if result.get("confidence"):
                    confidence_pct = f"{result['confidence']*100:.0f}%"
                    confidence_bar = "█" * int(result['confidence'] * 10)
                    print(f"📊 CONFIDENCE: {confidence_pct} {confidence_bar}\n")
                
                if result.get("urgency_level"):
                    urgency_icon = {
                        "EMERGENCY": "🚨",
                        "DON'T DRIVE": "🛑",
                        "DRIVE CAREFULLY": "⚠️",
                        "CAN DRIVE": "✅"
                    }.get(result["urgency_level"], "ℹ️")
                    print(f"{urgency_icon} URGENCY: {result['urgency_level']}\n")
                
                # Display cost estimate (Phase 3)
                if result.get("cost_estimate"):
                    cost_data = result["cost_estimate"]
                    print("💰 COST ESTIMATE:")
                    print(cost_data["message"])
                    print()
            else:
                print("💬 General inquiry detected. Ready to help!")
            print("-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using ARS Rapide Chatbot!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            continue


if __name__ == "__main__":
    main()
