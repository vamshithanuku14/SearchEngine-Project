import numpy as np
from typing import List, Dict, Any
from common.config import Config
from common.logger import setup_logger

logger = setup_logger(__name__)

class CosineSimilarity:
    """Cosine similarity calculator for vector comparison."""
    
    def __init__(self):
        self.config = Config()
    
    def calculate_similarity(self, vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            dot_product = np.dot(vector_a, vector_b)
            norm_a = np.linalg.norm(vector_a)
            norm_b = np.linalg.norm(vector_b)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            similarity = dot_product / (norm_a * norm_b)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {str(e)}")
            return 0.0
    
    def rank_documents(self, query_vector: np.ndarray, document_vectors: Dict[str, np.ndarray], top_k: int = 10) -> List[Dict[str, Any]]:
        """Rank documents by cosine similarity to query vector."""
        scores = []
        
        for doc_id, doc_vector in document_vectors.items():
            similarity = self.calculate_similarity(query_vector, doc_vector)
            scores.append({
                'document_id': doc_id,
                'similarity_score': similarity
            })
        
        # Sort by similarity score (descending)
        scores.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scores[:top_k]
    
    def batch_similarity(self, vectors: List[np.ndarray]) -> np.ndarray:
        """Calculate pairwise cosine similarities for a list of vectors."""
        try:
            # Normalize vectors
            normalized_vectors = []
            for vector in vectors:
                norm = np.linalg.norm(vector)
                if norm > 0:
                    normalized_vectors.append(vector / norm)
                else:
                    normalized_vectors.append(np.zeros_like(vector))
            
            # Convert to matrix
            matrix = np.array(normalized_vectors)
            
            # Calculate similarity matrix
            similarity_matrix = np.dot(matrix, matrix.T)
            
            return similarity_matrix
            
        except Exception as e:
            logger.error(f"Error in batch similarity calculation: {str(e)}")
            return np.zeros((len(vectors), len(vectors)))