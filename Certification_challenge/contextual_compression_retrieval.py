"""
Tesla Investment Tracker - Contextual Compression Advanced Retrieval
Advanced retrieval system with contextual compression for better RAG performance.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import json
import warnings
warnings.filterwarnings('ignore')

class ContextualCompressionTeslaRetriever:
    """
    Advanced contextual compression retriever for Tesla investment analysis.
    Compresses and focuses relevant content for improved RAG performance.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the contextual compression retriever.
        
        Args:
            data_dir: Directory containing Tesla data files
        """
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings()
        self.documents = []
        self.vectorstore = None
        self.compression_retriever = None
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        
    def load_tesla_data(self) -> List[Document]:
        """
        Load and process Tesla data into documents.
        
        Returns:
            List of processed documents
        """
        print("📊 Loading Tesla data for contextual compression...")
        
        documents = []
        
        # Load financial data
        financial_df = pd.read_csv(f"{self.data_dir}/tesla_financial_metrics.csv")
        for _, row in financial_df.iterrows():
            doc = Document(
                page_content=f"Tesla financial data for {row['quarter']} {row['year']}: Revenue ${row['revenue_millions']}M, Deliveries {row['deliveries']}, Market Cap ${row['market_cap_billions']}B, Net Income ${row['net_income_millions']}M, Gross Margin {row['gross_margin']}%",
                metadata={"source": "financial", "quarter": row['quarter'], "year": row['year'], "type": "financial_metrics"}
            )
            documents.append(doc)
        
        # Load sentiment data
        sentiment_df = pd.read_csv(f"{self.data_dir}/market_sentiment_data.csv")
        for _, row in sentiment_df.iterrows():
            doc = Document(
                page_content=f"Market sentiment on {row['date']}: Score {row['sentiment_score']}, Source {row['source']}, Topics {row['key_topics']}, Volume {row['volume']}, Positive mentions {row['positive_mentions']}, Negative mentions {row['negative_mentions']}",
                metadata={"source": "sentiment", "date": row['date'], "score": row['sentiment_score'], "type": "market_sentiment"}
            )
            documents.append(doc)
        
        # Load research papers
        research_df = pd.read_csv(f"{self.data_dir}/tesla_research_papers.csv")
        for _, row in research_df.iterrows():
            doc = Document(
                page_content=f"Research paper: {row['title']} by {row['authors']} ({row['publication_year']}). Abstract: {row['abstract']}. Key findings: {row['key_findings']}. Investment implications: {row['investment_implications']}. Sentiment: {row['sentiment']}",
                metadata={"source": "research", "year": row['publication_year'], "sentiment": row['sentiment'], "type": "research_paper"}
            )
            documents.append(doc)
        
        # Load competitor data
        competitor_df = pd.read_csv(f"{self.data_dir}/competitor_analysis.csv")
        for _, row in competitor_df.iterrows():
            doc = Document(
                page_content=f"Competitor analysis: {row['company']}, Market Cap ${row['market_cap_billions']}B, EV Deliveries {row.get('ev_deliveries', 'N/A')}, Revenue ${row.get('revenue_millions', 'N/A')}M, Analyst Rating {row.get('analyst_rating', 'N/A')}",
                metadata={"source": "competitor", "company": row['company'], "type": "competitor_analysis"}
            )
            documents.append(doc)
        
        # Load product reviews
        with open(f"{self.data_dir}/tesla_product_reviews.json", 'r') as f:
            product_data = json.load(f)
        
        for product in product_data['tesla_products']:
            for review in product['reviews']:
                doc = Document(
                    page_content=f"Product review for {product['product_name']} ({product['category']}): Rating {review['rating']}/5. Source: {review['source']}. Summary: {review['summary']}. Pros: {', '.join(review['pros'])}. Cons: {', '.join(review['cons'])}. Investment rating: {review['investment_rating']}",
                    metadata={"source": "product", "product": product['product_name'], "rating": review['rating'], "type": "product_review"}
                )
                documents.append(doc)
        
        self.documents = documents
        print(f"✅ Loaded {len(documents)} documents")
        return documents
    
    def create_vectorstore(self) -> None:
        """
        Create vector store for retrieval.
        """
        print("🔍 Creating vector store...")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        split_docs = text_splitter.split_documents(self.documents)
        
        # Create vector store using FAISS
        self.vectorstore = FAISS.from_documents(
            documents=split_docs,
            embedding=self.embeddings
        )
        
        print(f"✅ Created vector store with {len(split_docs)} chunks")
    
    def create_compression_retriever(self) -> None:
        """
        Create contextual compression retriever.
        """
        print("🔍 Creating contextual compression retriever...")
        
        # Create base retriever
        base_retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}
        )
        
        # Create LLM-based compressor
        compressor_prompt = PromptTemplate(
            input_variables=["question", "context"],
            template="""
            Given the following question and context, extract only the information that is relevant to the question.
            
            Question: {question}
            Context: {context}
            
            Extract only the information that directly answers the question or provides relevant context. Remove any irrelevant information.
            
            Relevant information:
            """
        )
        
        compressor = LLMChainExtractor.from_llm(
            llm=self.llm,
            prompt=compressor_prompt
        )
        
        # Create contextual compression retriever
        self.compression_retriever = ContextualCompressionRetriever(
            base_retriever=base_retriever,
            base_compressor=compressor
        )
        
        print("✅ Created contextual compression retriever")
    
    def compress_and_retrieve(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform contextual compression retrieval.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of compressed relevant documents
        """
        print(f"🔍 Performing contextual compression retrieval for: {query}")
        
        if not self.compression_retriever:
            self.create_compression_retriever()
        
        # Get compressed results
        results = self.compression_retriever.get_relevant_documents(query)
        
        return results[:k]
    
    def semantic_search_with_compression(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform semantic search with contextual compression.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of compressed semantically relevant documents
        """
        print(f"🔍 Performing semantic search with compression for: {query}")
        
        # Get initial semantic results
        initial_results = self.vectorstore.similarity_search(query, k=k*2)
        
        # Apply compression to each result
        compressed_results = []
        for doc in initial_results:
            compressed_doc = self._compress_document(doc, query)
            if compressed_doc:
                compressed_results.append(compressed_doc)
        
        return compressed_results[:k]
    
    def _compress_document(self, doc: Document, query: str) -> Optional[Document]:
        """
        Compress a single document based on the query.
        
        Args:
            doc: Document to compress
            query: Query to focus compression on
            
        Returns:
            Compressed document or None
        """
        try:
            # Create compression prompt
            compression_prompt = f"""
            Given the following question and document content, extract only the information that is relevant to the question.
            
            Question: {query}
            Document: {doc.page_content}
            
            Extract only the information that directly answers the question or provides relevant context. Remove any irrelevant information.
            
            Compressed content:
            """
            
            # Use LLM to compress
            compressed_content = self.llm.predict(compression_prompt)
            
            if compressed_content and len(compressed_content.strip()) > 10:
                return Document(
                    page_content=compressed_content.strip(),
                    metadata=doc.metadata
                )
            
            return None
            
        except Exception as e:
            print(f"Warning: Could not compress document: {e}")
            return doc
    
    def source_specific_compression(self, query: str, source: str, k: int = 5) -> List[Document]:
        """
        Perform source-specific contextual compression.
        
        Args:
            query: Search query
            source: Data source to search in
            k: Number of results to return
            
        Returns:
            List of compressed relevant documents from the specified source
        """
        print(f"🔍 Performing source-specific compression for {source}: {query}")
        
        # Filter documents by source
        source_docs = [doc for doc in self.documents if doc.metadata.get('source') == source]
        
        if not source_docs:
            print(f"⚠️ No documents found for source: {source}")
            return []
        
        # Create temporary vector store for source-specific search
        temp_vectorstore = FAISS.from_documents(
            documents=source_docs,
            embedding=self.embeddings
        )
        
        # Get initial results
        initial_results = temp_vectorstore.similarity_search(query, k=k*2)
        
        # Apply compression
        compressed_results = []
        for doc in initial_results:
            compressed_doc = self._compress_document(doc, query)
            if compressed_doc:
                compressed_results.append(compressed_doc)
        
        return compressed_results[:k]
    
    def multi_stage_compression(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform multi-stage compression for complex queries.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of multi-stage compressed documents
        """
        print(f"🔍 Performing multi-stage compression for: {query}")
        
        # Stage 1: Initial retrieval
        initial_results = self.vectorstore.similarity_search(query, k=k*3)
        
        # Stage 2: First compression
        first_compressed = []
        for doc in initial_results:
            compressed = self._compress_document(doc, query)
            if compressed:
                first_compressed.append(compressed)
        
        # Stage 3: Re-rank and re-compress
        if len(first_compressed) > k:
            # Re-rank based on relevance
            relevance_scores = []
            for doc in first_compressed:
                score = self._calculate_relevance_score(doc, query)
                relevance_scores.append((score, doc))
            
            # Sort by relevance and take top k
            relevance_scores.sort(key=lambda x: x[0], reverse=True)
            top_docs = [doc for _, doc in relevance_scores[:k]]
            
            # Final compression
            final_compressed = []
            for doc in top_docs:
                final_compressed_doc = self._compress_document(doc, query)
                if final_compressed_doc:
                    final_compressed.append(final_compressed_doc)
            
            return final_compressed
        
        return first_compressed[:k]
    
    def _calculate_relevance_score(self, doc: Document, query: str) -> float:
        """
        Calculate relevance score between document and query.
        
        Args:
            doc: Document
            query: Query
            
        Returns:
            Relevance score
        """
        # Simple keyword-based relevance scoring
        query_words = set(query.lower().split())
        doc_words = set(doc.page_content.lower().split())
        
        intersection = query_words.intersection(doc_words)
        union = query_words.union(doc_words)
        
        if len(union) == 0:
            return 0.0
        
        return len(intersection) / len(union)
    
    def compare_compression_methods(self, query: str, k: int = 5) -> Dict[str, List[Document]]:
        """
        Compare different compression methods for a query.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Dictionary with results from different compression methods
        """
        print(f"🔍 Comparing compression methods for: {query}")
        
        results = {
            "basic_compression": self.compress_and_retrieve(query, k),
            "semantic_compression": self.semantic_search_with_compression(query, k),
            "multi_stage_compression": self.multi_stage_compression(query, k),
            "financial_compression": self.source_specific_compression(query, "financial", k),
            "sentiment_compression": self.source_specific_compression(query, "sentiment", k)
        }
        
        return results

def main():
    """
    Example usage of contextual compression retrieval.
    """
    print("🚀 Tesla Investment - Contextual Compression Retrieval")
    print("=" * 60)
    
    # Initialize retriever
    retriever = ContextualCompressionTeslaRetriever()
    
    # Load data
    documents = retriever.load_tesla_data()
    
    # Create vector store
    retriever.create_vectorstore()
    
    # Create compression retriever
    retriever.create_compression_retriever()
    
    # Test queries
    test_queries = [
        "What was Tesla's revenue and delivery performance in Q4 2023?",
        "How is Tesla's market sentiment trending?",
        "What are the latest product reviews for Tesla Model 3?",
        "Who are Tesla's main competitors and how do they compare?",
        "What do research papers say about Tesla's investment potential?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: {query}")
        
        # Compare different compression methods
        results = retriever.compare_compression_methods(query, k=3)
        
        for method, docs in results.items():
            print(f"\n  📊 {method.upper()} RESULTS:")
            for i, doc in enumerate(docs):
                print(f"    {i+1}. {doc.page_content[:150]}...")
                print(f"       Source: {doc.metadata.get('source', 'Unknown')}")
    
    print("\n✅ Contextual compression retrieval demonstration completed!")

if __name__ == "__main__":
    main() 