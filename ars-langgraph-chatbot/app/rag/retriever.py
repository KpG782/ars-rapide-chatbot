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
            
            context = f"""
Problem {i} (Relevance: {score:.2%}):
Category: {doc['category']}
Issue: {doc['problem']}
Diagnosis: {doc['diagnosis']}
Symptoms: {', '.join(doc['symptoms'])}
Causes: {', '.join(doc['causes'])}
Urgency: {doc['urgency']}
Typical Cost: ₱{doc['typical_cost_php']['min']:,} - ₱{doc['typical_cost_php']['max']:,}
Repair Time: {doc['repair_time_hours']} hours
Notes: {doc['notes']}
""".strip()
            
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
        print(f"{i}. {doc['problem']}")
        print(f"   Diagnosis: {doc['diagnosis']}")
        print(f"   Urgency: {doc['urgency']}")
        print(f"   Score: {result['score']:.3f}\n")
    
    print("\n" + "="*60)
    print("Formatted Context for LLM:")
    print("="*60)
    print(retriever.format_context_for_llm(results))
