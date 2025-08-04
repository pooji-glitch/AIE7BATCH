#!/usr/bin/env python3
"""
Tesla Investment Tracker - Data Loading Script
Loads all data files from the data/ folder
"""

import pandas as pd
import json
import os
from typing import Dict, List, Any
# Note: These imports are not actually used in this script, but kept for reference
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain_community.document_loaders.json_loader import JSONLoader
from langchain.schema import Document

class TeslaDataLoader:
    """Loads and manages Tesla investment data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.data = {}
        
    def load_all_data(self) -> Dict[str, Any]:
        """Load all data files from the data directory"""
        print("🚀 Loading Tesla Investment Data...")
        
        # Load CSV files
        self._load_research_papers()
        self._load_market_sentiment()
        self._load_financial_metrics()
        self._load_competitor_analysis()
        
        # Load JSON files
        self._load_product_reviews()
        
        print(f"✅ All data loaded successfully!")
        self._print_summary()
        
        return self.data
    
    def _load_research_papers(self):
        """Load Tesla research papers data"""
        try:
            file_path = os.path.join(self.data_dir, "tesla_research_papers.csv")
            df = pd.read_csv(file_path)
            self.data['research_papers'] = df
            print(f"📄 Research Papers: {len(df)} papers loaded")
        except Exception as e:
            print(f"❌ Error loading research papers: {e}")
    
    def _load_market_sentiment(self):
        """Load market sentiment data"""
        try:
            file_path = os.path.join(self.data_dir, "market_sentiment_data.csv")
            df = pd.read_csv(file_path)
            self.data['market_sentiment'] = df
            print(f"📊 Market Sentiment: {len(df)} data points loaded")
        except Exception as e:
            print(f"❌ Error loading market sentiment: {e}")
    
    def _load_financial_metrics(self):
        """Load Tesla financial metrics"""
        try:
            file_path = os.path.join(self.data_dir, "tesla_financial_metrics.csv")
            df = pd.read_csv(file_path)
            self.data['financial_metrics'] = df
            print(f"💰 Financial Metrics: {len(df)} quarters loaded")
        except Exception as e:
            print(f"❌ Error loading financial metrics: {e}")
    
    def _load_competitor_analysis(self):
        """Load competitor analysis data"""
        try:
            file_path = os.path.join(self.data_dir, "competitor_analysis.csv")
            df = pd.read_csv(file_path)
            self.data['competitor_analysis'] = df
            print(f"🏢 Competitor Analysis: {len(df)} companies loaded")
        except Exception as e:
            print(f"❌ Error loading competitor analysis: {e}")
    
    def _load_product_reviews(self):
        """Load Tesla product reviews"""
        try:
            file_path = os.path.join(self.data_dir, "tesla_product_reviews.json")
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.data['product_reviews'] = data
            print(f"🚗 Product Reviews: {len(data.get('tesla_products', []))} products loaded")
        except Exception as e:
            print(f"❌ Error loading product reviews: {e}")
    
    def _print_summary(self):
        """Print summary of loaded data"""
        print("\n📋 Data Summary:")
        print("=" * 50)
        for key, value in self.data.items():
            if isinstance(value, pd.DataFrame):
                print(f"📊 {key.replace('_', ' ').title()}: {len(value)} rows")
            elif isinstance(value, dict):
                if 'tesla_products' in value:
                    print(f"🚗 {key.replace('_', ' ').title()}: {len(value['tesla_products'])} products")
                else:
                    print(f"📄 {key.replace('_', ' ').title()}: {len(value)} items")
        print("=" * 50)
    
    def get_research_papers(self) -> pd.DataFrame:
        """Get research papers data"""
        return self.data.get('research_papers', pd.DataFrame())
    
    def get_market_sentiment(self) -> pd.DataFrame:
        """Get market sentiment data"""
        return self.data.get('market_sentiment', pd.DataFrame())
    
    def get_financial_metrics(self) -> pd.DataFrame:
        """Get financial metrics data"""
        return self.data.get('financial_metrics', pd.DataFrame())
    
    def get_competitor_analysis(self) -> pd.DataFrame:
        """Get competitor analysis data"""
        return self.data.get('competitor_analysis', pd.DataFrame())
    
    def get_product_reviews(self) -> Dict:
        """Get product reviews data"""
        return self.data.get('product_reviews', {})
    
    def get_positive_sentiment_data(self) -> pd.DataFrame:
        """Get only positive sentiment data"""
        sentiment_df = self.get_market_sentiment()
        if not sentiment_df.empty:
            return sentiment_df[sentiment_df['sentiment_score'] > 0.6]
        return pd.DataFrame()
    
    def get_recent_financial_data(self, quarters: int = 8) -> pd.DataFrame:
        """Get recent financial data (last N quarters)"""
        financial_df = self.get_financial_metrics()
        if not financial_df.empty:
            return financial_df.head(quarters)
        return pd.DataFrame()
    
    def get_top_competitors(self, top_n: int = 5) -> pd.DataFrame:
        """Get top N competitors by market cap"""
        competitor_df = self.get_competitor_analysis()
        if not competitor_df.empty:
            return competitor_df.head(top_n)
        return pd.DataFrame()

def load_tesla_data() -> TeslaDataLoader:
    """Convenience function to load all Tesla data"""
    loader = TeslaDataLoader()
    loader.load_all_data()
    return loader

if __name__ == "__main__":
    # Test the data loading
    loader = load_tesla_data()
    
    # Show some sample data
    print("\n🔍 Sample Data Preview:")
    print("\n1. Research Papers (first 2 rows):")
    print(loader.get_research_papers().head(2))
    
    print("\n2. Market Sentiment (first 2 rows):")
    print(loader.get_market_sentiment().head(2))
    
    print("\n3. Financial Metrics (first 2 rows):")
    print(loader.get_financial_metrics().head(2))
    
    print("\n4. Competitor Analysis (first 2 rows):")
    print(loader.get_competitor_analysis().head(2))
    
    print("\n5. Product Reviews (first product):")
    products = loader.get_product_reviews().get('tesla_products', [])
    if products:
        print(f"Product: {products[0]['product_name']}")
        print(f"Category: {products[0]['category']}")
        print(f"Price: ${products[0]['current_price']:,}") 