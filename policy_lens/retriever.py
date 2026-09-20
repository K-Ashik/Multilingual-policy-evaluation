import chromadb
from sentence_transformers import SentenceTransformer

class PolicyRetriever:
    def __init__(self, db_path="./policy_vector_db", collection_name="english_baseline"):
        """Initializes the embedding model and connects to the local vector database."""
        print("Initializing PolicyRetriever...")
        self.model = SentenceTransformer("BAAI/bge-m3")
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Connect to existing database or create a new one
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def search_baseline(self, foreign_clause, top_k=1):
        """Converts a foreign clause to a vector and retrieves the matching English standard."""
        query_embedding = self.model.encode([foreign_clause]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        if not results['documents'][0]:
            return None
            
        return {
            "matched_text": results['documents'][0][0],
            "match_id": results['ids'][0][0],
            "distance": results['distances'][0][0]
        }