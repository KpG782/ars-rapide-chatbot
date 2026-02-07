"""
RAG retriever for semantic search of car problems.
"""
from typing import List, Dict, Any
from app.rag.vector_store import get_vector_store


class CarProblemRetriever:
    """Retriever for car diagnostic knowledge base."""
    
    def __init__(self, top_k: int = 3):
        """
        Initialize retriever.
        
        Args:
            top_k: Number of relevant documents to retrieve
        """
        self.top_k = top_k
        self.vector_store = get_vector_store()
    
    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve most relevant car problems for the user's query.
        
        Args:
            query: User's symptom description
            
        Returns:
            List of relevant car problem documents with similarity scores
        """
        return self.vector_store.search(query, top_k=self.top_k)
    
    def format_context_for_llm(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context string for LLM prompt.
        
        Args:
            results: List of search results with documents and scores
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        
        for i, result in enumerate(results, 1):
            doc = result['document']
            score = result['score']
            
            # Handle both old and new JSON formats
            title = doc.get('title') or doc.get('problem', 'Unknown Issue')
            symptoms = doc.get('symptoms', [])
            taglish_symptoms = doc.get('taglish_symptoms', [])
            diagnosis = doc.get('diagnosis', 'No diagnosis available')
            causes = doc.get('possible_causes') or doc.get('causes', [])
            urgency = doc.get('urgency', 'UNKNOWN')
            category = doc.get('category', 'General')
            
            # Build context string
            context = f"""
Problem {i} (Relevance: {score:.2%}):
Category: {category}
Issue: {title}
Diagnosis: {diagnosis}
Symptoms: {', '.join(symptoms)}"""
            
            if taglish_symptoms:
                context += f"\nTaglish Symptoms: {', '.join(taglish_symptoms)}"
            
            context += f"\nPossible Causes: {', '.join(causes)}"
            context += f"\nUrgency: {urgency}"
            
            # Add cost/time info if available
            if 'typical_cost_php' in doc:
                cost = doc['typical_cost_php']
                context += f"\nTypical Cost: ₱{cost.get('min', 0):,} - ₱{cost.get('max', 0):,}"
            
            if 'repair_time_hours' in doc:
                context += f"\nRepair Time: {doc['repair_time_hours']} hours"
            
            if 'notes' in doc:
                context += f"\nNotes: {doc['notes']}"
            
            if 'estimated_fix' in doc:
                context += f"\nSuggested Fix: {doc['estimated_fix']}"
            
            context = context.strip()
            context_parts.append(context)
        
        return "\n\n" + "\n\n---\n\n".join(context_parts)


# Global retriever instance
_retriever = None


def get_retriever(top_k: int = 3) -> CarProblemRetriever:
    """Get or create the global retriever instance."""
    global _retriever
    
    if _retriever is None:
        _retriever = CarProblemRetriever(top_k=top_k)
    
    return _retriever


if __name__ == "__main__":
    # Test the retriever
    print("Testing Car Problem Retriever...\n")
    
    retriever = get_retriever(top_k=3)
    
    query = "my car won't start, the lights don't turn on, and I hear clicking"
    print(f"Query: {query}\n")
    
    results = retriever.retrieve(query)
    
    print(f"Found {len(results)} relevant problems:\n")
    for i, result in enumerate(results, 1):
        doc = result['document']
        title = doc.get('title') or doc.get('problem', 'Unknown')
        print(f"{i}. {title}")
        print(f"   Diagnosis: {doc.get('diagnosis', 'N/A')}")
        print(f"   Urgency: {doc.get('urgency', 'N/A')}")
        print(f"   Score: {result['score']:.3f}\n")
    
    print("\n" + "="*60)
    print("Formatted Context for LLM:")
    print("="*60)
    print(retriever.format_context_for_llm(results))
