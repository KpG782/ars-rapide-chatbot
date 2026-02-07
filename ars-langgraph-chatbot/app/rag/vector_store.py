"""
In-memory vector store for car problems using sentence embeddings.
Alternative to ChromaDB for Python 3.14 compatibility.
"""
import json
import os
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SimpleVectorStore:
    """Lightweight in-memory vector store with semantic search."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector store with sentence transformer model.
        
        Args:
            model_name: HuggingFace model for embeddings (default: fast + accurate)
        """
        self.model = SentenceTransformer(model_name)
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray = None
        self.is_loaded = False
        
    def load_documents(self, json_path: str) -> int:
        """
        Load car problems from JSON file and generate embeddings.
        
        Args:
            json_path: Path to car_problems.json
            
        Returns:
            Number of documents loaded
        """
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Knowledge base not found: {json_path}")
            
        with open(json_path, 'r', encoding='utf-8') as f:
            self.documents = json.load(f)
        
        # Create searchable text combining all relevant fields
        texts_to_embed = []
        for doc in self.documents:
            # Combine multiple fields for better semantic matching
            # Handle both old and new JSON formats
            title = doc.get('title') or doc.get('problem', '')
            symptoms = doc.get('symptoms', [])
            taglish_symptoms = doc.get('taglish_symptoms', [])
            diagnosis = doc.get('diagnosis', '')
            causes = doc.get('possible_causes') or doc.get('causes', [])
            category = doc.get('category', '')
            
            searchable_text = (
                f"{title} "
                f"{' '.join(symptoms)} "
                f"{' '.join(taglish_symptoms)} "
                f"{diagnosis} "
                f"{' '.join(causes)} "
                f"{category}"
            )
            texts_to_embed.append(searchable_text)
        
        # Generate embeddings (384-dimensional vectors)
        print(f"Generating embeddings for {len(texts_to_embed)} documents...")
        self.embeddings = self.model.encode(texts_to_embed, show_progress_bar=True)
        self.is_loaded = True
        
        print(f"✓ Loaded {len(self.documents)} car problems into vector store")
        return len(self.documents)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Semantic search for most relevant car problems.
        
        Args:
            query: User's problem description
            top_k: Number of results to return (default: 3)
            
        Returns:
            List of dicts with 'document' and 'score' keys
        """
        if not self.is_loaded:
            raise RuntimeError("Vector store not loaded. Call load_documents() first.")
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top K indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Build results with similarity scores
        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "score": float(similarities[idx])
            })
        
        return results
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Return all documents in the knowledge base."""
        return self.documents


# Global instance (initialized once)
_vector_store = None


def get_vector_store() -> SimpleVectorStore:
    """
    Get or create the global vector store instance.
    Loads documents automatically on first call.
    """
    global _vector_store
    
    if _vector_store is None:
        _vector_store = SimpleVectorStore()
        
        # Auto-load knowledge base
        kb_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "knowledge_base",
            "car_problems.json"
        )
        _vector_store.load_documents(kb_path)
    
    return _vector_store


if __name__ == "__main__":
    # Test the vector store
    print("Testing Simple Vector Store...\n")
    
    store = get_vector_store()
    
    test_queries = [
        "my car won't start and the lights are dim",
        "engine is too hot and steam coming out",
        "brakes making squeaking sound"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 60)
        results = store.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            doc = result['document']
            score = result['score']
            title = doc.get('title') or doc.get('problem', 'Unknown')
            print(f"\n{i}. {title}")
            print(f"   Category: {doc.get('category', 'N/A')}")
            print(f"   Diagnosis: {doc.get('diagnosis', 'N/A')}")
            print(f"   Urgency: {doc.get('urgency', 'N/A')}")
            print(f"   Similarity: {score:.3f}")
