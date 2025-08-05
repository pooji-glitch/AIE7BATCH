"""
Tesla Investment Tracker - Data Parser
Comprehensive data parsing and analysis module for Tesla investment data.
"""

import pandas as pd
import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TeslaDataParser:
    """
    Comprehensive data parser for Tesla investment analysis.
    Handles CSV, JSON, and various data formats with validation and analysis.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data parser.
        
        Args:
            data_dir (str): Directory containing data files
        """
        self.data_dir = data_dir
        self.data_cache = {}
        self.validation_errors = []
        
    def load_all_data(self) -> Dict[str, Any]:
        """
        Load all available data files and return structured data.
        
        Returns:
            Dict containing all parsed data
        """
        data = {
            'financial_metrics': self.load_financial_metrics(),
            'market_sentiment': self.load_market_sentiment(),
            'research_papers': self.load_research_papers(),
            'product_reviews': self.load_product_reviews(),
            'competitor_analysis': self.load_competitor_analysis()
        }
        
        # Validate data quality
        self._validate_data_quality(data)
        
        return data
    
    def load_financial_metrics(self) -> pd.DataFrame:
        """
        Load and parse Tesla financial metrics CSV.
        
        Returns:
            DataFrame with financial metrics
        """
        try:
            df = pd.read_csv(f"{self.data_dir}/tesla_financial_metrics.csv")
            
            # Data cleaning and type conversion
            df['quarter'] = df['quarter'].astype(str)
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            
            # Convert monetary columns to numeric
            monetary_cols = ['revenue_millions', 'net_income_millions', 'free_cash_flow_millions', 
                           'rd_expense_millions', 'market_cap_billions']
            for col in monetary_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert percentage columns
            percentage_cols = ['gross_margin', 'operating_margin', 'debt_to_equity', 'pe_ratio']
            for col in percentage_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert deliveries to numeric
            df['deliveries'] = pd.to_numeric(df['deliveries'], errors='coerce')
            
            # Create date column for time series analysis
            df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + 
                                      df['quarter'].str.replace('Q', '') + '-01')
            
            # Sort by date
            df = df.sort_values('date').reset_index(drop=True)
            
            print(f"✅ Loaded financial metrics: {len(df)} quarters of data")
            return df
            
        except Exception as e:
            print(f"❌ Error loading financial metrics: {e}")
            return pd.DataFrame()
    
    def load_market_sentiment(self) -> pd.DataFrame:
        """
        Load and parse market sentiment data.
        
        Returns:
            DataFrame with sentiment data
        """
        try:
            df = pd.read_csv(f"{self.data_dir}/market_sentiment_data.csv")
            
            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            
            # Convert numeric columns
            numeric_cols = ['sentiment_score', 'confidence', 'volume', 'positive_mentions', 
                          'negative_mentions', 'neutral_mentions', 'total_mentions']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Create sentiment categories
            df['sentiment_category'] = pd.cut(df['sentiment_score'], 
                                           bins=[0, 0.4, 0.6, 1.0], 
                                           labels=['Negative', 'Neutral', 'Positive'])
            
            # Sort by date
            df = df.sort_values('date').reset_index(drop=True)
            
            print(f"✅ Loaded market sentiment: {len(df)} days of data")
            return df
            
        except Exception as e:
            print(f"❌ Error loading market sentiment: {e}")
            return pd.DataFrame()
    
    def load_research_papers(self) -> pd.DataFrame:
        """
        Load and parse research papers data.
        
        Returns:
            DataFrame with research papers data
        """
        try:
            df = pd.read_csv(f"{self.data_dir}/tesla_research_papers.csv")
            
            # Convert year to numeric
            df['publication_year'] = pd.to_numeric(df['publication_year'], errors='coerce')
            
            # Create sentiment mapping
            sentiment_mapping = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
            df['sentiment_numeric'] = df['sentiment'].map(sentiment_mapping)
            
            # Extract key topics
            df['key_topics_list'] = df['key_findings'].str.split(',').str[:3]
            
            print(f"✅ Loaded research papers: {len(df)} papers")
            return df
            
        except Exception as e:
            print(f"❌ Error loading research papers: {e}")
            return pd.DataFrame()
    
    def load_product_reviews(self) -> Dict[str, Any]:
        """
        Load and parse product reviews JSON data.
        
        Returns:
            Dict with structured product reviews data
        """
        try:
            with open(f"{self.data_dir}/tesla_product_reviews.json", 'r') as f:
                data = json.load(f)
            
            # Extract products and reviews
            products = []
            all_reviews = []
            
            for product in data.get('tesla_products', []):
                product_info = {
                    'product_id': product.get('product_id'),
                    'product_name': product.get('product_name'),
                    'category': product.get('category'),
                    'release_year': product.get('release_year'),
                    'current_price': product.get('current_price'),
                    'market_position': product.get('market_position'),
                    'competitive_advantage': product.get('competitive_advantage')
                }
                products.append(product_info)
                
                # Extract reviews
                for review in product.get('reviews', []):
                    review_data = {
                        'product_id': product.get('product_id'),
                        'product_name': product.get('product_name'),
                        **review
                    }
                    all_reviews.append(review_data)
            
            # Convert to DataFrames
            products_df = pd.DataFrame(products)
            reviews_df = pd.DataFrame(all_reviews)
            
            # Convert review date
            if 'review_date' in reviews_df.columns:
                reviews_df['review_date'] = pd.to_datetime(reviews_df['review_date'])
            
            # Convert rating to numeric
            if 'rating' in reviews_df.columns:
                reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
            
            print(f"✅ Loaded product reviews: {len(products_df)} products, {len(reviews_df)} reviews")
            
            return {
                'products': products_df,
                'reviews': reviews_df,
                'raw_data': data
            }
            
        except Exception as e:
            print(f"❌ Error loading product reviews: {e}")
            return {'products': pd.DataFrame(), 'reviews': pd.DataFrame(), 'raw_data': {}}
    
    def load_competitor_analysis(self) -> pd.DataFrame:
        """
        Load and parse competitor analysis data.
        
        Returns:
            DataFrame with competitor analysis
        """
        try:
            df = pd.read_csv(f"{self.data_dir}/competitor_analysis.csv")
            
            # Convert numeric columns
            numeric_cols = ['market_cap_billions', 'revenue_millions', 'ev_deliveries', 
                          'analyst_rating', 'price_target']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            print(f"✅ Loaded competitor analysis: {len(df)} companies")
            return df
            
        except Exception as e:
            print(f"❌ Error loading competitor analysis: {e}")
            return pd.DataFrame()
    
    def _validate_data_quality(self, data: Dict[str, Any]) -> None:
        """
        Validate data quality and report issues.
        
        Args:
            data: Dictionary containing all parsed data
        """
        print("\n🔍 Data Quality Validation:")
        
        # Check for missing data
        for key, value in data.items():
            if isinstance(value, pd.DataFrame) and value.empty:
                self.validation_errors.append(f"Empty DataFrame for {key}")
                print(f"❌ {key}: No data loaded")
            elif isinstance(value, dict) and not value.get('products', pd.DataFrame()).empty:
                print(f"✅ {key}: Data loaded successfully")
            elif isinstance(value, pd.DataFrame):
                print(f"✅ {key}: {len(value)} records loaded")
        
        # Check for missing values in key columns
        if 'financial_metrics' in data and not data['financial_metrics'].empty:
            missing_financial = data['financial_metrics'].isnull().sum()
            if missing_financial.sum() > 0:
                print(f"⚠️  Missing values in financial data: {missing_financial.sum()}")
        
        if 'market_sentiment' in data and not data['market_sentiment'].empty:
            missing_sentiment = data['market_sentiment'].isnull().sum()
            if missing_sentiment.sum() > 0:
                print(f"⚠️  Missing values in sentiment data: {missing_sentiment.sum()}")
    
    def get_financial_summary(self) -> Dict[str, Any]:
        """
        Generate financial metrics summary.
        
        Returns:
            Dictionary with financial summary statistics
        """
        financial_df = self.load_financial_metrics()
        
        if financial_df.empty:
            return {}
        
        # Latest quarter data
        latest = financial_df.iloc[0]
        
        # Calculate growth rates
        if len(financial_df) > 4:
            yoy_revenue_growth = ((latest['revenue_millions'] - 
                                  financial_df.iloc[4]['revenue_millions']) / 
                                 financial_df.iloc[4]['revenue_millions'] * 100)
        else:
            yoy_revenue_growth = None
        
        summary = {
            'latest_quarter': latest['quarter'],
            'latest_year': latest['year'],
            'revenue_millions': latest['revenue_millions'],
            'net_income_millions': latest['net_income_millions'],
            'deliveries': latest['deliveries'],
            'gross_margin': latest['gross_margin'],
            'market_cap_billions': latest['market_cap_billions'],
            'yoy_revenue_growth': yoy_revenue_growth,
            'total_quarters': len(financial_df)
        }
        
        return summary
    
    def get_sentiment_summary(self) -> Dict[str, Any]:
        """
        Generate sentiment analysis summary.
        
        Returns:
            Dictionary with sentiment summary statistics
        """
        sentiment_df = self.load_market_sentiment()
        
        if sentiment_df.empty:
            return {}
        
        summary = {
            'total_days': len(sentiment_df),
            'avg_sentiment_score': sentiment_df['sentiment_score'].mean(),
            'sentiment_trend': sentiment_df['sentiment_score'].iloc[-5:].mean() - 
                              sentiment_df['sentiment_score'].iloc[:5].mean(),
            'positive_days': len(sentiment_df[sentiment_df['sentiment_score'] > 0.6]),
            'negative_days': len(sentiment_df[sentiment_df['sentiment_score'] < 0.4]),
            'total_volume': sentiment_df['volume'].sum(),
            'top_sources': sentiment_df['source'].value_counts().head(3).to_dict()
        }
        
        return summary
    
    def get_product_summary(self) -> Dict[str, Any]:
        """
        Generate product analysis summary.
        
        Returns:
            Dictionary with product summary statistics
        """
        product_data = self.load_product_reviews()
        
        if product_data['products'].empty:
            return {}
        
        products_df = product_data['products']
        reviews_df = product_data['reviews']
        
        summary = {
            'total_products': len(products_df),
            'avg_price': products_df['current_price'].mean(),
            'price_range': {
                'min': products_df['current_price'].min(),
                'max': products_df['current_price'].max()
            },
            'total_reviews': len(reviews_df),
            'avg_rating': reviews_df['rating'].mean() if 'rating' in reviews_df.columns else None,
            'investment_ratings': reviews_df['investment_rating'].value_counts().to_dict() 
                                if 'investment_rating' in reviews_df.columns else {}
        }
        
        return summary
    
    def export_analysis_report(self, output_file: str = "tesla_analysis_report.json") -> None:
        """
        Export comprehensive analysis report.
        
        Args:
            output_file: Output file path
        """
        data = self.load_all_data()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'financial_summary': self.get_financial_summary(),
            'sentiment_summary': self.get_sentiment_summary(),
            'product_summary': self.get_product_summary(),
            'data_quality': {
                'validation_errors': self.validation_errors,
                'total_datasets': len(data)
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✅ Analysis report exported to {output_file}")
    
    def get_time_series_data(self, metric: str = 'revenue_millions') -> pd.DataFrame:
        """
        Get time series data for analysis.
        
        Args:
            metric: Metric to analyze
            
        Returns:
            DataFrame with time series data
        """
        financial_df = self.load_financial_metrics()
        
        if financial_df.empty or metric not in financial_df.columns:
            return pd.DataFrame()
        
        ts_data = financial_df[['date', metric]].copy()
        ts_data = ts_data.sort_values('date')
        
        return ts_data
    
    def get_sentiment_trends(self, days: int = 7) -> pd.DataFrame:
        """
        Get sentiment trends for the last N days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            DataFrame with sentiment trends
        """
        sentiment_df = self.load_market_sentiment()
        
        if sentiment_df.empty:
            return pd.DataFrame()
        
        # Get last N days
        recent_data = sentiment_df.tail(days)
        
        # Calculate daily trends
        recent_data['sentiment_change'] = recent_data['sentiment_score'].diff()
        recent_data['volume_change'] = recent_data['volume'].diff()
        
        return recent_data

# Example usage and testing
if __name__ == "__main__":
    # Initialize parser
    parser = TeslaDataParser()
    
    # Load all data
    print("🚀 Loading Tesla Investment Data...")
    data = parser.load_all_data()
    
    # Generate summaries
    print("\n📊 Financial Summary:")
    financial_summary = parser.get_financial_summary()
    for key, value in financial_summary.items():
        print(f"  {key}: {value}")
    
    print("\n📈 Sentiment Summary:")
    sentiment_summary = parser.get_sentiment_summary()
    for key, value in sentiment_summary.items():
        print(f"  {key}: {value}")
    
    print("\n🚗 Product Summary:")
    product_summary = parser.get_product_summary()
    for key, value in product_summary.items():
        print(f"  {key}: {value}")
    
    # Export report
    parser.export_analysis_report()
    
    print("\n✅ Data parsing complete!") 