import os
os.environ["UVLOOP_DISABLE"] = "1"

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime

# Set up API keys before importing modules (optional)
if "OPENAI_API_KEY" not in os.environ:
    print("⚠️ OpenAI API key not set. App will run in fallback mode.")
    print("   To enable full LLM features, set: export OPENAI_API_KEY='your-key'")

if "TAVILY_API_KEY" not in os.environ:
    print("⚠️ Tavily API key not set. Web search features will be disabled.")
    print("   To enable web search, set: export TAVILY_API_KEY='your-key'")

# Import your Tesla analysis modules
try:
    from agentic_rag_bm25 import AgenticRAGBM25
    from advanced_retriever_builder import AdvancedTeslaRetrieverBuilder
    from data_parser import TeslaDataParser
    # from ragas_evaluation import run_ragas_evaluation  # Commented out due to uvloop conflict
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tesla Investment Analysis AI",
    description="Advanced RAG system for Tesla investment analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class AnalysisRequest(BaseModel):
    question: str

class AnalysisResponse(BaseModel):
    response: str
    context_sources: List[Dict[str, Any]]
    retrieval_evaluation: Dict[str, Any]  # Changed from Dict[str, float] to Dict[str, Any]
    timestamp: str
    query: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# Global variables for initialized components
tesla_agent = None
data_parser = None
retriever_builder = None

def initialize_components():
    """Initialize Tesla analysis components."""
    global tesla_agent, data_parser, retriever_builder
    
    try:
        # Initialize data parser
        data_parser = TeslaDataParser()
        logger.info("✅ Data parser initialized")
        
        # Initialize agentic RAG with proper setup (this works without API keys)
        tesla_agent = AgenticRAGBM25()
        # Load data and create retriever
        tesla_agent.load_tesla_data()
        tesla_agent.create_bm25_retriever()
        logger.info("✅ Tesla agent initialized")
        
        # Try to initialize advanced retriever builder (optional - requires API keys)
        try:
            retriever_builder = AdvancedTeslaRetrieverBuilder()
            retriever_builder.load_and_process_data()
            retriever_builder.create_vectorstore()
            logger.info("✅ Advanced retriever builder initialized")
        except Exception as advanced_error:
            logger.warning(f"⚠️ Advanced retriever builder not available (requires API keys): {advanced_error}")
            retriever_builder = None
        
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        # Don't fail completely - try to initialize at least the basic agent
        try:
            tesla_agent = AgenticRAGBM25()
            tesla_agent.load_tesla_data()
            tesla_agent.create_bm25_retriever()
            logger.info("✅ Tesla agent initialized (fallback mode)")
            return True
        except Exception as fallback_error:
            logger.error(f"❌ Failed to initialize even basic components: {fallback_error}")
            return False

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    logger.info("🚀 Starting Tesla Investment Analysis AI...")
    success = initialize_components()
    if success:
        logger.info("✅ All components initialized successfully")
    else:
        logger.warning("⚠️ Some components failed to initialize")

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the frontend HTML file."""
    html_file = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    return FileResponse(html_file)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_tesla_investment(request: AnalysisRequest):
    """Analyze Tesla investment question using AI."""
    try:
        if not tesla_agent:
            raise HTTPException(status_code=500, detail="Tesla agent not initialized")
        
        logger.info(f"📝 Processing query: {request.question}")
        
        # Get analysis from Tesla agent
        result = tesla_agent.run_comprehensive_analysis(request.question)
        
        # Extract relevant information
        response = result.get('response', 'No analysis available')
        
        # Handle context sources properly
        context_sources_formatted = []
        if 'context' in result and isinstance(result['context'], list):
            for doc in result['context']:
                if hasattr(doc, 'page_content'):
                    context_sources_formatted.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata
                    })
        elif isinstance(result.get('context_sources'), list):
            # If context_sources is already a list of strings, convert to proper format
            for source in result['context_sources']:
                context_sources_formatted.append({
                    'content': f"Source: {source}",
                    'metadata': {'source': source}
                })
        
        # Handle retrieval evaluation properly - extract only simple numeric values
        retrieval_evaluation = result.get('retrieval_evaluation', {})
        if isinstance(retrieval_evaluation, dict):
            # Extract only the numeric values for the API response
            api_retrieval_evaluation = {
                'avg_relevance': float(retrieval_evaluation.get('avg_relevance', 0.0)),
                'num_results': int(retrieval_evaluation.get('num_results', 0))
            }
        else:
            api_retrieval_evaluation = {
                'avg_relevance': 0.0,
                'num_results': 0
            }
        
        logger.info(f"✅ Analysis completed for query: {request.question}")
        
        return AnalysisResponse(
            response=response,
            context_sources=context_sources_formatted,
            retrieval_evaluation=api_retrieval_evaluation,
            timestamp=datetime.now().isoformat(),
            query=request.question
        )
        
    except Exception as e:
        logger.error(f"❌ Error analyzing query: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Remove this duplicate section - it's conflicting with the frontend route
@app.get("/data/summary")
async def get_data_summary():
    """Get summary of available Tesla data."""
    try:
        if not data_parser:
            raise HTTPException(status_code=500, detail="Data parser not initialized")
        
        # Load and summarize data
        financial_data = data_parser.load_financial_metrics()
        sentiment_data = data_parser.load_market_sentiment()
        research_data = data_parser.load_research_papers()
        reviews_data = data_parser.load_product_reviews()
        competitor_data = data_parser.load_competitor_analysis()
        
        summary = {
            "financial_metrics": {
                "quarters": len(financial_data),
                "latest_quarter": financial_data.iloc[-1]['quarter'] if not financial_data.empty else None,
                "latest_revenue": financial_data.iloc[-1]['revenue_millions'] if not financial_data.empty else None
            },
            "market_sentiment": {
                "data_points": len(sentiment_data),
                "avg_sentiment": sentiment_data['sentiment_score'].mean() if not sentiment_data.empty else None
            },
            "research_papers": {
                "papers": len(research_data),
                "topics": research_data['topic'].nunique() if not research_data.empty else None
            },
            "product_reviews": {
                "reviews": len(reviews_data),
                "avg_rating": reviews_data['rating'].mean() if not reviews_data.empty else None
            },
            "competitor_analysis": {
                "competitors": len(competitor_data),
                "metrics_compared": len(competitor_data.columns) if not competitor_data.empty else None
            }
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"❌ Error getting data summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get data summary: {str(e)}")

@app.get("/evaluation/ragas")
async def run_evaluation():
    """Run RAGAS evaluation on the system."""
    try:
        logger.info("🔍 Running RAGAS evaluation...")
        
        # Run RAGAS evaluation
        results, scores = run_ragas_evaluation()
        
        evaluation_results = {
            "metrics": scores,
            "overall_score": sum(scores.values()) / len(scores) if scores else 0,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        logger.info("✅ RAGAS evaluation completed")
        return evaluation_results
        
    except Exception as e:
        logger.error(f"❌ Error running RAGAS evaluation: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@app.get("/retrievers/available")
async def get_available_retrievers():
    """Get list of available retrievers."""
    try:
        if not retriever_builder:
            raise HTTPException(status_code=500, detail="Retriever builder not initialized")
        
        retrievers = {
            "bm25": "BM25 Keyword Retriever",
            "semantic": "Semantic Vector Retriever", 
            "ensemble": "Ensemble Retriever (BM25 + Semantic)",
            "compression": "Contextual Compression Retriever",
            "multi_query": "Multi-Query Retriever",
            "time_weighted": "Time-Weighted Retriever"
        }
        
        return {
            "available_retrievers": retrievers,
            "current_retriever": "bm25",
            "description": "BM25 keyword-based retrieval for precise Tesla investment analysis"
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting retrievers: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get retrievers: {str(e)}")

@app.get("/api/status")
async def get_api_status():
    """Get comprehensive API status."""
    components_status = {
        "data_parser": data_parser is not None,
        "retriever_builder": retriever_builder is not None,
        "tesla_agent": tesla_agent is not None
    }
    
    return {
        "status": "running",
        "components": components_status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Mount static files
import os
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 