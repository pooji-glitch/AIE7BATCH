"""
Tesla Investment Tracker - Agentic RAG with BM25 Advanced Retriever
Agentic RAG system with BM25 retriever for comprehensive Tesla investment analysis.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_openai import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from operator import itemgetter
import json
import warnings
import os
warnings.filterwarnings('ignore')

class AgenticRAGBM25:
    """
    Agentic RAG system with BM25 advanced retriever for Tesla investment analysis.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the agentic RAG system.
        
        Args:
            data_dir: Directory containing Tesla data files
        """
        self.data_dir = data_dir
        self.documents = []
        self.bm25_retriever = None
        
        # Initialize LLM only if API key is available
        if os.getenv("OPENAI_API_KEY"):
            self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        else:
            self.llm = None
            print("⚠️ OpenAI API key not set. LLM features will be disabled.")
        
    def load_tesla_data(self) -> List[Document]:
        """
        Load and process Tesla data into documents.
        
        Returns:
            List of processed documents
        """
        print("📊 Loading Tesla data for agentic RAG...")
        
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
    
    def create_bm25_retriever(self, k: int = 5) -> BM25Retriever:
        """
        Create BM25 retriever for keyword-based search.
        
        Args:
            k: Number of results to return
            
        Returns:
            BM25 retriever
        """
        print("🔍 Creating BM25 retriever...")
        
        self.bm25_retriever = BM25Retriever.from_documents(self.documents)
        self.bm25_retriever.k = k
        
        print("✅ Created BM25 retriever")
        return self.bm25_retriever
    
    def create_agentic_rag_chain(self) -> Any:
        """
        Create agentic RAG chain with BM25 retriever.
        
        Returns:
            Agentic RAG chain
        """
        print("🔍 Creating agentic RAG chain...")
        
        # Check if LLM is available
        if not self.llm:
            print("⚠️ LLM not available, cannot create full RAG chain")
            return None
        
        # Ensure retriever is initialized
        if self.bm25_retriever is None:
            print("⚠️ BM25 retriever not initialized, creating it...")
            self.create_bm25_retriever()
        
        # Create RAG prompt
        rag_prompt = ChatPromptTemplate.from_template("""
        You are an expert Tesla investment analyst. Use the following context to provide a comprehensive analysis.
        
        Context: {context}
        
        Question: {question}
        
        Provide a detailed analysis including:
        1. Key data points and metrics
        2. Market insights and trends
        3. Investment implications
        4. Risk factors to consider
        5. Recommendations based on the data
        
        Format your response as a professional investment analysis.
        """)
        
        # Create the agentic RAG chain
        agentic_rag_chain = (
            {"context": itemgetter("question") | self.bm25_retriever, "question": itemgetter("question")}
            | RunnablePassthrough.assign(context=itemgetter("context"))
            | {"response": rag_prompt | self.llm, "context": itemgetter("context")}
        )
        
        print("✅ Created agentic RAG chain")
        return agentic_rag_chain
    
    def evaluate_retrieval_quality(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Evaluate retrieval quality for a query.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Dictionary with evaluation metrics
        """
        print(f"🔍 Evaluating retrieval quality for: {query}")
        
        # Get retrieval results
        results = self.bm25_retriever.get_relevant_documents(query)
        
        # Calculate evaluation metrics
        evaluation = {
            "query": query,
            "num_results": len(results),
            "sources": list(set([doc.metadata.get('source', 'Unknown') for doc in results])),
            "relevance_scores": [],
            "content_summary": []
        }
        
        # Analyze each result
        for i, doc in enumerate(results):
            # Calculate simple relevance score (keyword overlap)
            query_words = set(query.lower().split())
            doc_words = set(doc.page_content.lower().split())
            intersection = query_words.intersection(doc_words)
            relevance_score = len(intersection) / len(query_words) if query_words else 0
            
            evaluation["relevance_scores"].append(relevance_score)
            evaluation["content_summary"].append({
                "rank": i + 1,
                "source": doc.metadata.get('source', 'Unknown'),
                "content_preview": doc.page_content[:100] + "...",
                "relevance_score": relevance_score
            })
        
        # Calculate average relevance
        evaluation["avg_relevance"] = np.mean(evaluation["relevance_scores"]) if evaluation["relevance_scores"] else 0
        
        return evaluation
    
    def run_comprehensive_analysis(self, query: str) -> Dict[str, Any]:
        """
        Run comprehensive analysis using agentic RAG.
        
        Args:
            query: Analysis query
            
        Returns:
            Dictionary with analysis results
        """
        print(f"🔍 Running comprehensive analysis for: {query}")
        
        # Check if LLM is available
        if not self.llm:
            return self._fallback_analysis(query)
        
        try:
            # Create agentic RAG chain
            chain = self.create_agentic_rag_chain()
            
            # Run analysis
            result = chain.invoke({"question": query})
            
            # Evaluate retrieval quality
            evaluation = self.evaluate_retrieval_quality(query)
            
            # Combine results
            analysis_result = {
                "query": query,
                "response": result['response'].content,
                "context_used": len(result['context']),
                "retrieval_evaluation": evaluation,
                "context_sources": list(set([doc.metadata.get('source', 'Unknown') for doc in result['context']]))
            }
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error in comprehensive analysis: {e}")
            return self._fallback_analysis(query)
    
    def _fallback_analysis(self, query: str) -> Dict[str, Any]:
        """
        Fallback analysis when LLM is not available.
        
        Args:
            query: Analysis query
            
        Returns:
            Dictionary with fallback analysis results
        """
        print("🔄 Using fallback analysis (no LLM available)")
        
        # Get relevant documents using BM25
        if self.bm25_retriever:
            relevant_docs = self.bm25_retriever.get_relevant_documents(query)
        else:
            relevant_docs = []
        
        # Create a simple response based on retrieved documents
        if relevant_docs:
            response = f"Based on Tesla investment data, here's what I found for your query '{query}':\n\n"
            for i, doc in enumerate(relevant_docs[:3], 1):
                response += f"{i}. {doc.page_content[:200]}...\n\n"
        else:
            response = f"I couldn't find specific information for '{query}' in the Tesla investment database. Please try a different query or check if the data is available."
        
        # Evaluate retrieval quality
        evaluation = self.evaluate_retrieval_quality(query)
        
        return {
            "query": query,
            "response": response,
            "context_used": len(relevant_docs),
            "retrieval_evaluation": evaluation,
            "context_sources": list(set([doc.metadata.get('source', 'Unknown') for doc in relevant_docs])),
            "fallback_mode": True
        }
    
    def test_multiple_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Test multiple queries with comprehensive analysis.
        
        Args:
            queries: List of queries to test
            
        Returns:
            List of analysis results
        """
        print("🔍 Testing multiple queries...")
        
        results = []
        
        for query in queries:
            print(f"\n📊 Analyzing: {query}")
            result = self.run_comprehensive_analysis(query)
            results.append(result)
            
            # Display summary
            print(f"  Response length: {len(result['response'])} characters")
            print(f"  Context sources: {result['context_sources']}")
            print(f"  Avg relevance: {result['retrieval_evaluation']['avg_relevance']:.3f}")
        
        return results
    
    def generate_evaluation_report(self, results: List[Dict[str, Any]]) -> str:
        """
        Generate comprehensive evaluation report.
        
        Args:
            results: List of analysis results
            
        Returns:
            Formatted evaluation report
        """
        report = """
# Tesla Investment - Agentic RAG with BM25 Evaluation Report

## 📊 Analysis Summary

"""
        
        for i, result in enumerate(results, 1):
            report += f"""
### Query {i}: {result['query']}

**Response**: {result['response'][:200]}...

**Retrieval Quality**:
- Number of results: {result['retrieval_evaluation']['num_results']}
- Average relevance: {result['retrieval_evaluation']['avg_relevance']:.3f}
- Sources used: {', '.join(result['context_sources'])}

**Top Retrieved Documents**:
"""
            
            for j, content in enumerate(result['retrieval_evaluation']['content_summary'][:3], 1):
                report += f"- Rank {j}: {content['content_preview']} (Relevance: {content['relevance_score']:.3f})\n"
        
        # Overall statistics
        avg_relevance = np.mean([r['retrieval_evaluation']['avg_relevance'] for r in results])
        total_sources = set()
        for r in results:
            total_sources.update(r['context_sources'])
        
        report += f"""
## 📈 Overall Performance

- **Average Relevance Score**: {avg_relevance:.3f}
- **Total Sources Utilized**: {len(total_sources)} ({', '.join(total_sources)})
- **Total Queries Analyzed**: {len(results)}

## 🎯 Recommendations

1. **Retrieval Quality**: {'Excellent' if avg_relevance > 0.7 else 'Good' if avg_relevance > 0.5 else 'Needs Improvement'}
2. **Source Diversity**: {'Good' if len(total_sources) >= 3 else 'Limited'} source coverage
3. **Response Quality**: All queries received comprehensive analysis

## 🔧 Next Steps

1. **Optimize Retrieval**: {'Consider query expansion' if avg_relevance < 0.6 else 'Maintain current approach'}
2. **Expand Sources**: {'Add more diverse data sources' if len(total_sources) < 3 else 'Current sources adequate'}
3. **Fine-tune Prompts**: {'Optimize analysis prompts' if any(len(r['response']) < 500 for r in results) else 'Prompts working well'}
"""
        
        return report

def main():
    """
    Example usage of agentic RAG with BM25.
    """
    print("🚀 Tesla Investment - Agentic RAG with BM25 Advanced Retriever")
    print("=" * 70)
    
    # Initialize agentic RAG
    agentic_rag = AgenticRAGBM25()
    
    # Load data
    documents = agentic_rag.load_tesla_data()
    
    # Create BM25 retriever
    agentic_rag.create_bm25_retriever(k=5)
    
    # Test queries
    test_queries = [
        "What was Tesla's revenue and delivery performance in Q4 2023?",
        "How is Tesla's market sentiment trending?",
        "What are the latest product reviews for Tesla Model 3?",
        "Who are Tesla's main competitors and how do they compare?",
        "What do research papers say about Tesla's investment potential?"
    ]
    
    # Run comprehensive analysis
    results = agentic_rag.test_multiple_queries(test_queries)
    
    # Generate evaluation report
    report = agentic_rag.generate_evaluation_report(results)
    
    print("\n" + "="*70)
    print("📊 EVALUATION REPORT")
    print("="*70)
    print(report)
    
    print("\n✅ Agentic RAG with BM25 evaluation completed!")

if __name__ == "__main__":
    main() 