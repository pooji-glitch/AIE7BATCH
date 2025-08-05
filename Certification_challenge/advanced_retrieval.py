"""
Tesla Investment Tracker - Advanced Retrieval Methods
Comprehensive advanced retrieval system with multiple search strategies.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, FAISS
from langchain.retrievers import (
    BM25Retriever,
    EnsembleRetriever,
    ContextualCompressionRetriever,
    TimeWeightedVectorStoreRetriever
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import json
import warnings
warnings.filterwarnings('ignore')

class AdvancedTeslaRetriever:
    """
    Advanced retrieval system for Tesla investment analysis.
    Implements multiple retrieval strategies for comprehensive search.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the advanced retriever.
        
        Args:
            data_dir: Directory containing Tesla data files
        """
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings()
        self.documents = []
        self.vectorstore = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        
    def load_and_process_data(self) -> List[Document]:
        """
        Load and process all Tesla data into documents.
        
        Returns:
            List of processed documents
        """
        print("📊 Loading and processing Tesla data...")
        
        documents = []
        
        # Load financial data
        financial_df = pd.read_csv(f"{self.data_dir}/tesla_financial_metrics.csv")
        for _, row in financial_df.iterrows():
            doc = Document(
                page_content=f"Tesla financial data for {row['quarter']} {row['year']}: Revenue ${row['revenue_millions']}M, Deliveries {row['deliveries']}, Market Cap ${row['market_cap_billions']}B",
                metadata={"source": "financial", "quarter": row['quarter'], "year": row['year']}
            )
            documents.append(doc)
        
        # Load sentiment data
        sentiment_df = pd.read_csv(f"{self.data_dir}/market_sentiment_data.csv")
        for _, row in sentiment_df.iterrows():
            doc = Document(
                page_content=f"Market sentiment on {row['date']}: Score {row['sentiment_score']}, Source {row['source']}, Topics {row['key_topics']}",
                metadata={"source": "sentiment", "date": row['date'], "score": row['sentiment_score']}
            )
            documents.append(doc)
        
        # Load research papers
        research_df = pd.read_csv(f"{self.data_dir}/tesla_research_papers.csv")
        for _, row in research_df.iterrows():
            doc = Document(
                page_content=f"Research paper: {row['title']} by {row['authors']}. Findings: {row['key_findings']}. Sentiment: {row['sentiment']}",
                metadata={"source": "research", "year": row['publication_year'], "sentiment": row['sentiment']}
            )
            documents.append(doc)
        
        # Load competitor data
        competitor_df = pd.read_csv(f"{self.data_dir}/competitor_analysis.csv")
        for _, row in competitor_df.iterrows():
            doc = Document(
                page_content=f"Competitor: {row['company']}, Market Cap ${row['market_cap_billions']}B, EV Deliveries {row.get('ev_deliveries', 'N/A')}",
                metadata={"source": "competitor", "company": row['company']}
            )
            documents.append(doc)
        
        # Load product reviews
        with open(f"{self.data_dir}/tesla_product_reviews.json", 'r') as f:
            product_data = json.load(f)
        
        for product in product_data['tesla_products']:
            for review in product['reviews']:
                doc = Document(
                    page_content=f"Product review for {product['product_name']}: Rating {review['rating']}/5. Summary: {review['summary']}. Investment rating: {review['investment_rating']}",
                    metadata={"source": "product", "product": product['product_name'], "rating": review['rating']}
                )
                documents.append(doc)
        
        self.documents = documents
        print(f"✅ Loaded {len(documents)} documents")
        return documents
    
    def create_vectorstore(self) -> None:
        """
        Create vector store for semantic search.
        """
        print("🔍 Creating vector store...")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        split_docs = text_splitter.split_documents(self.documents)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings
        )
        
        print(f"✅ Created vector store with {len(split_docs)} chunks")
    
    def create_bm25_retriever(self) -> None:
        """
        Create BM25 retriever for keyword-based search.
        """
        print("🔍 Creating BM25 retriever...")
        
        # Extract text content
        texts = [doc.page_content for doc in self.documents]
        
        # Create BM25 retriever
        self.bm25_retriever = BM25Retriever.from_documents(self.documents)
        
        print("✅ Created BM25 retriever")
    
    def create_ensemble_retriever(self) -> None:
        """
        Create ensemble retriever combining multiple strategies.
        """
        print("🔍 Creating ensemble retriever...")
        
        # Create vector store retriever
        vector_retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        # Create ensemble
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, self.bm25_retriever],
            weights=[0.7, 0.3]  # Give more weight to semantic search
        )
        
        print("✅ Created ensemble retriever")
    
    def hybrid_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform hybrid search combining semantic and keyword search.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        print(f"🔍 Performing hybrid search for: {query}")
        
        # Semantic search
        semantic_results = self.vectorstore.similarity_search(query, k=k)
        
        # Keyword search
        keyword_results = self.bm25_retriever.get_relevant_documents(query)
        
        # Combine and deduplicate
        all_results = semantic_results + keyword_results[:k//2]
        unique_results = []
        seen_content = set()
        
        for doc in all_results:
            if doc.page_content not in seen_content:
                unique_results.append(doc)
                seen_content.add(doc.page_content)
        
        return unique_results[:k]
    
    def contextual_compression_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform contextual compression search.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of compressed relevant documents
        """
        print(f"🔍 Performing contextual compression search for: {query}")
        
        # Get initial results
        initial_results = self.vectorstore.similarity_search(query, k=k*2)
        
        # Apply contextual compression
        compressed_retriever = ContextualCompressionRetriever(
            base_retriever=self.vectorstore.as_retriever(),
            base_compressor=self.embeddings
        )
        
        return compressed_retriever.get_relevant_documents(query)
    
    def time_weighted_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform time-weighted search prioritizing recent information.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of time-weighted relevant documents
        """
        print(f"🔍 Performing time-weighted search for: {query}")
        
        # Create time-weighted retriever
        time_weighted_retriever = TimeWeightedVectorStoreRetriever(
            vectorstore=self.vectorstore,
            decay_rate=0.01,
            k=k
        )
        
        return time_weighted_retriever.get_relevant_documents(query)
    
    def multi_query_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform multi-query search with query expansion.
        
        Args:
            query: Original query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        print(f"🔍 Performing multi-query search for: {query}")
        
        # Generate related queries
        related_queries = self._generate_related_queries(query)
        
        all_results = []
        
        # Search with original query
        results = self.vectorstore.similarity_search(query, k=k//2)
        all_results.extend(results)
        
        # Search with related queries
        for related_query in related_queries[:2]:
            results = self.vectorstore.similarity_search(related_query, k=k//4)
            all_results.extend(results)
        
        # Deduplicate and return
        unique_results = []
        seen_content = set()
        
        for doc in all_results:
            if doc.page_content not in seen_content:
                unique_results.append(doc)
                seen_content.add(doc.page_content)
        
        return unique_results[:k]
    
    def _generate_related_queries(self, query: str) -> List[str]:
        """
        Generate related queries for query expansion.
        
        Args:
            query: Original query
            
        Returns:
            List of related queries
        """
        # Simple query expansion based on Tesla investment topics
        tesla_topics = {
            "revenue": ["financial performance", "earnings", "quarterly results"],
            "deliveries": ["vehicle sales", "production", "manufacturing"],
            "sentiment": ["market mood", "investor confidence", "social sentiment"],
            "competition": ["competitors", "market share", "competitive analysis"],
            "products": ["vehicle reviews", "customer satisfaction", "product ratings"]
        }
        
        related_queries = []
        query_lower = query.lower()
        
        for topic, expansions in tesla_topics.items():
            if topic in query_lower:
                related_queries.extend(expansions)
        
        return related_queries
    
    def semantic_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform semantic search using embeddings.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of semantically relevant documents
        """
        print(f"🔍 Performing semantic search for: {query}")
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def keyword_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform keyword-based search using BM25.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of keyword-relevant documents
        """
        print(f"🔍 Performing keyword search for: {query}")
        
        return self.bm25_retriever.get_relevant_documents(query)[:k]
    
    def ensemble_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform ensemble search combining multiple retrievers.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of ensemble-relevant documents
        """
        print(f"🔍 Performing ensemble search for: {query}")
        
        return self.ensemble_retriever.get_relevant_documents(query)
    
    def search_by_source(self, query: str, source: str, k: int = 5) -> List[Document]:
        """
        Search within a specific data source.
        
        Args:
            query: Search query
            source: Data source to search in
            k: Number of results to return
            
        Returns:
            List of relevant documents from the specified source
        """
        print(f"🔍 Searching {source} for: {query}")
        
        # Filter documents by source
        source_docs = [doc for doc in self.documents if doc.metadata.get('source') == source]
        
        # Create temporary vector store for source-specific search
        temp_vectorstore = Chroma.from_documents(
            documents=source_docs,
            embedding=self.embeddings
        )
        
        return temp_vectorstore.similarity_search(query, k=k)
    
    def compare_search_methods(self, query: str, k: int = 5) -> Dict[str, List[Document]]:
        """
        Compare different search methods for a query.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Dictionary with results from different search methods
        """
        print(f"🔍 Comparing search methods for: {query}")
        
        results = {
            "semantic": self.semantic_search(query, k),
            "keyword": self.keyword_search(query, k),
            "hybrid": self.hybrid_search(query, k),
            "ensemble": self.ensemble_search(query, k),
            "multi_query": self.multi_query_search(query, k)
        }
        
        return results

def main():
    """
    Example usage of advanced retrieval methods.
    """
    print("🚀 Tesla Investment - Advanced Retrieval System")
    print("=" * 50)
    
    # Initialize retriever
    retriever = AdvancedTeslaRetriever()
    
    # Load and process data
    documents = retriever.load_and_process_data()
    
    # Create retrieval components
    retriever.create_vectorstore()
    retriever.create_bm25_retriever()
    retriever.create_ensemble_retriever()
    
    # Test different search methods
    test_queries = [
        "What was Tesla's revenue in 2023?",
        "How is Tesla's market sentiment?",
        "What are the latest product reviews?",
        "Who are Tesla's main competitors?",
        "What do research papers say about Tesla?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: {query}")
        
        # Compare different methods
        results = retriever.compare_search_methods(query, k=3)
        
        for method, docs in results.items():
            print(f"\n  {method.upper()} Search Results:")
            for i, doc in enumerate(docs):
                print(f"    {i+1}. {doc.page_content[:100]}...")
    
    print("\n✅ Advanced retrieval system demonstration completed!")

if __name__ == "__main__":
    main() 