#!/usr/bin/env python3
"""
Medical Text Embedding Module
Generates vector embeddings from clinical text
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import torch
import time

class MedicalEmbedder:
    """
    Generate embeddings for medical text
    Uses sentence-transformers for local, private embedding generation
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        
        Args:
            model_name: HuggingFace model name
            
        For production, consider medical-specific models:
        - "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"
        - "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"
        - "dmis-lab/biobert-base-cased-v1.2"
        """
        print(f"🔄 Loading embedding model: {model_name}")
        start_time = time.time()
        
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.2f}s")
        print(f"✅ Embedding dimension: {self.dimension}")
        
        # Check if GPU is available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✅ Using device: {self.device}")
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of medical text strings
            batch_size: Batch size for processing
            
        Returns:
            Numpy array of embeddings, shape (n_texts, embedding_dim)
        """
        if not texts:
            return np.array([])
        
        print(f"�� Generating embeddings for {len(texts)} texts...")
        start_time = time.time()
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            device=self.device
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Generated embeddings in {elapsed:.2f}s ({len(texts)/elapsed:.1f} texts/sec)")
        
        return embeddings
    
    def embed_records(self, records: List[Dict]) -> List[Dict]:
        """
        Add embeddings to medical records
        
        Args:
            records: List of prepared medical records
            
        Returns:
            Records with 'embedding' field added
        """
        # Extract texts
        texts = [r['text'] for r in records]
        
        # Generate embeddings
        embeddings = self.generate_embeddings(texts)
        
        # Add embeddings to records
        for record, embedding in zip(records, embeddings):
            record['embedding'] = embedding.tolist()
            record['embedding_model'] = self.model_name
            record['embedding_dim'] = self.dimension
        
        print(f"✅ Added embeddings to {len(records)} records")
        return records
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query
        
        Args:
            query: Clinical question or search query
            
        Returns:
            Query embedding vector
        """
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding
    
    def get_model_info(self) -> Dict:
        """Return model information"""
        return {
            'model_name': self.model_name,
            'dimension': self.dimension,
            'device': self.device,
            'max_seq_length': self.model.max_seq_length
        }


# Test the module
if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from src.data_prep import MedicalDataPrep
    import pandas as pd
    
    print("=" * 60)
    print("Testing Embedding Generation Module")
    print("=" * 60)
    
    # Load and prepare data
    print("\n[1/3] Loading data...")
    df = pd.read_csv('data/synthetic_records.csv')
    prep = MedicalDataPrep()
    records = prep.prepare_records(df[:10])  # Test with 10 records
    
    # Initialize embedder
    print("\n[2/3] Initializing embedder...")
    embedder = MedicalEmbedder()
    
    # Generate embeddings
    print("\n[3/3] Generating embeddings...")
    embedded_records = embedder.embed_records(records)
    
    # Show sample
    print("\n📊 Sample Embedded Record:")
    print("-" * 60)
    sample = embedded_records[0]
    print(f"Anonymized ID: {sample['anon_id']}")
    print(f"Text length: {len(sample['text'])} chars")
    print(f"Embedding dimension: {sample['embedding_dim']}")
    print(f"Embedding shape: {len(sample['embedding'])} values")
    print(f"First 5 embedding values: {sample['embedding'][:5]}")
    
    # Test query embedding
    print("\n🔍 Testing Query Embedding:")
    print("-" * 60)
    query = "What are treatment options for diabetes?"
    query_emb = embedder.embed_query(query)
    print(f"Query: {query}")
    print(f"Query embedding shape: {query_emb.shape}")
    print(f"First 5 values: {query_emb[:5]}")
    
    # Model info
    print("\n📋 Model Information:")
    print("-" * 60)
    info = embedder.get_model_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Embedding module working correctly!")
