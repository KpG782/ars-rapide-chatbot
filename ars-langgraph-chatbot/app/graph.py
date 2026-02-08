"""
ARS Rapide Chatbot — Graph State Machine
Defines the conversation state and LangGraph structure.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from langgraph.graph import StateGraph, END


class ChatState(BaseModel):
    """
    The conversation state that flows through all graph nodes.
    Every node can read and write to this state.
    """
    # User input
    user_message: str = ""
    
    # Conversation tracking
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    
    # Intent classification
    intent: Optional[str] = None  # diagnose | cost | book | general
    
    # Symptom collection
    symptoms: List[str] = Field(default_factory=list)
    
    # Car details
    car_details: Dict[str, Any] = Field(default_factory=dict)
    
    # Diagnosis results
    diagnosis: Optional[str] = None
    confidence: Optional[float] = None
    urgency_level: Optional[str] = None  # EMERGENCY | DON'T DRIVE | DRIVE CAREFULLY | CAN DRIVE
    
    # Cost estimation
    cost_estimate: Optional[Dict[str, Any]] = None
    
    # Booking information
    booking_info: Optional[Dict[str, Any]] = None
    
    # Response generation
    response: str = ""
    needs_more_info: bool = False
    
    class Config:
        arbitrary_types_allowed = True


def build_graph() -> StateGraph:
    """
    Build the LangGraph state machine for Phase 3.
    
    Flow: User Message → Taglish Normalize → Classifier → Diagnosis → Cost Estimate → Response
    """
    from app.nodes.taglish import preprocess_taglish
    from app.nodes.classifier import classify_intent
    from app.nodes.diagnosis import diagnose_problem
    from app.nodes.cost_estimator import estimate_cost
    
    graph = StateGraph(ChatState)
    
    # Add nodes (Phase 3: added taglish preprocessing and cost estimation)
    graph.add_node("taglish", preprocess_taglish)
    graph.add_node("classify", classify_intent)
    graph.add_node("diagnose", diagnose_problem)
    graph.add_node("cost_estimate", estimate_cost)
    
    # Define routing logic based on intent
    def route_after_classification(state: ChatState) -> str:
        """Route to appropriate node based on classified intent."""
        intent = state.intent
        
        if intent == "DIAGNOSIS":
            return "diagnose"
        elif intent == "COST_ESTIMATE":
            # Direct cost inquiry (Phase 3)
            return END
        elif intent == "BOOKING":
            # Phase 4: will route to booking
            return END
        else:  # GENERAL
            return END
    
    # Set up graph flow (Phase 3: taglish → classify → diagnose → cost_estimate)
    graph.set_entry_point("taglish")
    graph.add_edge("taglish", "classify")
    graph.add_conditional_edges(
        "classify",
        route_after_classification,
        {
            "diagnose": "diagnose",
            END: END
        }
    )
    graph.add_edge("diagnose", "cost_estimate")
    graph.add_edge("cost_estimate", END)
    
    return graph
