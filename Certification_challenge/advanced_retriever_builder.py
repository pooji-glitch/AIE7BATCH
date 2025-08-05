"""
Tesla Investment Tracker - Advanced Retriever Builder
Comprehensive advanced retriever with multiple strategies and optimizations.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.retrievers import (
    BM25Retriever,
    EnsembleRetriever,
    ContextualCompressionRetriever,
    TimeWeightedVectorStoreRetriever,
    MultiQueryRetriever
)
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from operator import itemgetter
import json
import warnings
warnings.filterwarnings('ignore')

class AdvancedTeslaRetrieverBuilder:
    """
    Advanced retriever builder for Tesla investment analysis.
    Implements multiple retrieval strategies and optimizations.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the advanced retriever builder.
        
        Args:
            data_dir: Directory containing Tesla data files
        """
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings()
        self.documents = []
        self.vectorstore = None
        self.retrievers = {}
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        
    def load_and_process_data(self) -> List[Document]:
        """
        Load and process Tesla data into documents.
        
        Returns:
            List of processed documents
        """
        print("📊 Loading Tesla data for advanced retrieval...")
        
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
        Create vector store for semantic search.
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
    
    def build_semantic_retriever(self, k: int = 5) -> Any:
        """
        Build semantic retriever using embeddings.
        
        Args:
            k: Number of results to return
            
        Returns:
            Semantic retriever
        """
        print("🔍 Building semantic retriever...")
        
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        
        self.retrievers["semantic"] = retriever
        print("✅ Built semantic retriever")
        return retriever
    
    def build_bm25_retriever(self, k: int = 5) -> Any:
        """
        Build BM25 retriever for keyword-based search.
        
        Args:
            k: Number of results to return
            
        Returns:
            BM25 retriever
        """
        print("🔍 Building BM25 retriever...")
        
        retriever = BM25Retriever.from_documents(self.documents)
        retriever.k = k
        
        self.retrievers["bm25"] = retriever
        print("✅ Built BM25 retriever")
        return retriever
    
    def build_ensemble_retriever(self, weights: List[float] = None) -> Any:
        """
        Build ensemble retriever combining multiple strategies.
        
        Args:
            weights: Weights for different retrievers
            
        Returns:
            Ensemble retriever
        """
        print("🔍 Building ensemble retriever...")
        
        if weights is None:
            weights = [0.7, 0.3]  # More weight to semantic search
        
        # Get base retrievers
        semantic_retriever = self.retrievers.get("semantic", self.build_semantic_retriever())
        bm25_retriever = self.retrievers.get("bm25", self.build_bm25_retriever())
        
        # Create ensemble
        ensemble_retriever = EnsembleRetriever(
            retrievers=[semantic_retriever, bm25_retriever],
            weights=weights
        )
        
        self.retrievers["ensemble"] = ensemble_retriever
        print("✅ Built ensemble retriever")
        return ensemble_retriever
    
    def build_compression_retriever(self) -> Any:
        """
        Build contextual compression retriever.
        
        Returns:
            Contextual compression retriever
        """
        print("🔍 Building contextual compression retriever...")
        
        # Get base retriever
        base_retriever = self.retrievers.get("semantic", self.build_semantic_retriever())
        
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
        compression_retriever = ContextualCompressionRetriever(
            base_retriever=base_retriever,
            base_compressor=compressor
        )
        
        self.retrievers["compression"] = compression_retriever
        print("✅ Built contextual compression retriever")
        return compression_retriever
    
    def build_multi_query_retriever(self) -> Any:
        """
        Build multi-query retriever with query expansion.
        
        Returns:
            Multi-query retriever
        """
        print("🔍 Building multi-query retriever...")
        
        # Get base retriever
        base_retriever = self.retrievers.get("semantic", self.build_semantic_retriever())
        
        # Create multi-query retriever
        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever,
            llm=self.llm
        )
        
        self.retrievers["multi_query"] = multi_query_retriever
        print("✅ Built multi-query retriever")
        return multi_query_retriever
    
    def build_time_weighted_retriever(self, decay_rate: float = 0.01) -> Any:
        """
        Build time-weighted retriever prioritizing recent information.
        
        Args:
            decay_rate: Rate of time decay
            
        Returns:
            Time-weighted retriever
        """
        print("🔍 Building time-weighted retriever...")
        
        # Create time-weighted retriever
        time_weighted_retriever = TimeWeightedVectorStoreRetriever(
            vectorstore=self.vectorstore,
            decay_rate=decay_rate,
            k=5
        )
        
        self.retrievers["time_weighted"] = time_weighted_retriever
        print("✅ Built time-weighted retriever")
        return time_weighted_retriever
    
    def build_source_specific_retriever(self, source: str) -> Any:
        """
        Build source-specific retriever.
        
        Args:
            source: Data source to focus on
            
        Returns:
            Source-specific retriever
        """
        print(f"🔍 Building source-specific retriever for {source}...")
        
        # Filter documents by source
        source_docs = [doc for doc in self.documents if doc.metadata.get('source') == source]
        
        if not source_docs:
            print(f"⚠️ No documents found for source: {source}")
            return None
        
        # Create temporary vector store for source-specific search
        temp_vectorstore = FAISS.from_documents(
            documents=source_docs,
            embedding=self.embeddings
        )
        
        retriever = temp_vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        self.retrievers[f"source_{source}"] = retriever
        print(f"✅ Built source-specific retriever for {source}")
        return retriever
    
    def build_advanced_chain(self, retriever_type: str = "ensemble") -> Any:
        """
        Build advanced retrieval chain.
        
        Args:
            retriever_type: Type of retriever to use
            
        Returns:
            Advanced retrieval chain
        """
        print(f"🔍 Building advanced chain with {retriever_type} retriever...")
        
        # Get the specified retriever
        retriever = self.retrievers.get(retriever_type)
        if not retriever:
            print(f"⚠️ Retriever {retriever_type} not found, using ensemble")
            retriever = self.retrievers.get("ensemble", self.build_ensemble_retriever())
        
        # Create RAG prompt
        rag_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are a Tesla investment analyst. Use the following context to answer the question.
            
            Context: {context}
            
            Question: {question}
            
            Provide a comprehensive answer based on the context. Include specific data points and insights.
            """
        )
        
        # Create the advanced retrieval chain
        advanced_chain = (
            {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
            | RunnablePassthrough.assign(context=itemgetter("context"))
            | {"response": rag_prompt | self.llm, "context": itemgetter("context")}
        )
        
        print("✅ Built advanced retrieval chain")
        return advanced_chain
    
    def compare_retrievers(self, query: str, k: int = 5) -> Dict[str, List[Document]]:
        """
        Compare different retrievers for a query.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Dictionary with results from different retrievers
        """
        print(f"🔍 Comparing retrievers for: {query}")
        
        results = {}
        
        # Test each retriever
        for name, retriever in self.retrievers.items():
            try:
                docs = retriever.get_relevant_documents(query)
                results[name] = docs[:k]
            except Exception as e:
                print(f"⚠️ Error with {name} retriever: {e}")
                results[name] = []
        
        return results
    
    def get_retriever(self, retriever_type: str) -> Any:
        """
        Get a specific retriever by type.
        
        Args:
            retriever_type: Type of retriever
            
        Returns:
            Retriever instance
        """
        return self.retrievers.get(retriever_type)
    
    def list_retrievers(self) -> List[str]:
        """
        List all available retrievers.
        
        Returns:
            List of retriever names
        """
        return list(self.retrievers.keys())

def main():
    """
    Example usage of advanced retriever builder.
    """
    print("🚀 Tesla Investment - Advanced Retriever Builder")
    print("=" * 60)
    
    # Initialize builder
    builder = AdvancedTeslaRetrieverBuilder()
    
    # Load and process data
    documents = builder.load_and_process_data()
    
    # Create vector store
    builder.create_vectorstore()
    
    # Build different retrievers
    builder.build_semantic_retriever()
    builder.build_bm25_retriever()
    builder.build_ensemble_retriever()
    builder.build_compression_retriever()
    builder.build_multi_query_retriever()
    builder.build_time_weighted_retriever()
    
    # Build source-specific retrievers
    builder.build_source_specific_retriever("financial")
    builder.build_source_specific_retriever("sentiment")
    
    # List available retrievers
    print(f"\n📋 Available retrievers: {builder.list_retrievers()}")
    
    # Test queries
    test_queries = [
        "What was Tesla's revenue in 2023?",
        "How is Tesla's market sentiment?",
        "What are the latest product reviews?",
        "Who are Tesla's main competitors?",
        "What do research papers say about Tesla?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: {query}")
        
        # Compare different retrievers
        results = builder.compare_retrievers(query, k=3)
        
        for retriever_name, docs in results.items():
            print(f"\n  📊 {retriever_name.upper()} RESULTS:")
            for i, doc in enumerate(docs):
                print(f"    {i+1}. {doc.page_content[:100]}...")
                print(f"       Source: {doc.metadata.get('source', 'Unknown')}")
    
    # Build advanced chain
    advanced_chain = builder.build_advanced_chain("ensemble")
    
    # Test the chain
    test_query = "What was Tesla's revenue and delivery performance in Q4 2023?"
    result = advanced_chain.invoke({"question": test_query})
    
    print(f"\n🔍 Advanced Chain Result:")
    print(f"Response: {result['response'].content}")
    print(f"Context used: {len(result['context'])} documents")
    
    print("\n✅ Advanced retriever builder demonstration completed!")

if __name__ == "__main__":
    main() 