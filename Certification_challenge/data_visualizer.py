"""
Tesla Investment Tracker - Data Visualizer
Visualization module for Tesla investment data analysis.
"""

import matplotlib.pyplot as plt
# import seaborn as sns  # Comment out this line
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('default')
# sns.set_palette("husl")  # Comment out this line

class TeslaDataVisualizer:
    """
    Data visualization class for Tesla investment analysis.
    Creates charts and visualizations from parsed data.
    """
    
    def __init__(self, data_parser):
        """
        Initialize the visualizer with a data parser.
        
        Args:
            data_parser: TeslaDataParser instance
        """
        self.parser = data_parser
        self.figsize = (12, 8)
        
    def plot_financial_trends(self, metrics: List[str] = None) -> None:
        """
        Plot financial trends over time.
        
        Args:
            metrics: List of metrics to plot (default: revenue, deliveries, net_income)
        """
        if metrics is None:
            metrics = ['revenue_millions', 'deliveries', 'net_income_millions']
        
        financial_df = self.parser.load_financial_metrics()
        
        if financial_df.empty:
            print("❌ No financial data available")
            return
        
        fig, axes = plt.subplots(len(metrics), 1, figsize=(self.figsize[0], 4*len(metrics)))
        if len(metrics) == 1:
            axes = [axes]
        
        for i, metric in enumerate(metrics):
            if metric in financial_df.columns:
                axes[i].plot(financial_df['date'], financial_df[metric], marker='o', linewidth=2)
                axes[i].set_title(f'Tesla {metric.replace("_", " ").title()} Over Time')
                axes[i].set_xlabel('Date')
                axes[i].set_ylabel(metric.replace("_", " ").title())
                axes[i].grid(True, alpha=0.3)
                
                # Add trend line
                z = np.polyfit(range(len(financial_df)), financial_df[metric], 1)
                p = np.poly1d(z)
                axes[i].plot(financial_df['date'], p(range(len(financial_df))), 
                           "--", alpha=0.8, color='red', label='Trend')
                axes[i].legend()
        
        plt.tight_layout()
        plt.show()
    
    def plot_sentiment_analysis(self, days: int = 20) -> None:
        """
        Plot sentiment analysis over time.
        
        Args:
            days: Number of days to analyze
        """
        sentiment_df = self.parser.load_market_sentiment()
        
        if sentiment_df.empty:
            print("❌ No sentiment data available")
            return
        
        # Get recent data
        recent_data = sentiment_df.tail(days)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], 10))
        
        # Sentiment score over time
        ax1.plot(recent_data['date'], recent_data['sentiment_score'], 
                marker='o', linewidth=2, color='blue')
        ax1.set_title(f'Tesla Market Sentiment (Last {days} Days)')
        ax1.set_ylabel('Sentiment Score')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Neutral')
        ax1.legend()
        
        # Volume over time
        ax2.bar(recent_data['date'], recent_data['volume'], alpha=0.7, color='green')
        ax2.set_title('Market Volume')
        ax2.set_ylabel('Volume')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_product_analysis(self) -> None:
        """
        Plot product analysis and ratings.
        """
        product_data = self.parser.load_product_reviews()
        
        if product_data['products'].empty or product_data['reviews'].empty:
            print("❌ No product data available")
            return
        
        products_df = product_data['products']
        reviews_df = product_data['reviews']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Product prices
        ax1.bar(products_df['product_name'], products_df['current_price'], 
               color='skyblue', alpha=0.7)
        ax1.set_title('Tesla Product Prices')
        ax1.set_ylabel('Price ($)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Average ratings by product
        avg_ratings = reviews_df.groupby('product_name')['rating'].mean()
        ax2.bar(avg_ratings.index, avg_ratings.values, color='lightgreen', alpha=0.7)
        ax2.set_title('Average Product Ratings')
        ax2.set_ylabel('Rating')
        ax2.set_ylim(0, 5)
        ax2.tick_params(axis='x', rotation=45)
        
        # Investment ratings distribution
        if 'investment_rating' in reviews_df.columns:
            rating_counts = reviews_df['investment_rating'].value_counts()
            ax3.pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%')
            ax3.set_title('Investment Rating Distribution')
        
        # Review count by product
        review_counts = reviews_df['product_name'].value_counts()
        ax4.bar(review_counts.index, review_counts.values, color='orange', alpha=0.7)
        ax4.set_title('Number of Reviews by Product')
        ax4.set_ylabel('Number of Reviews')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def plot_competitor_analysis(self) -> None:
        """
        Plot competitor analysis.
        """
        competitor_df = self.parser.load_competitor_analysis()
        
        if competitor_df.empty:
            print("❌ No competitor data available")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Market cap comparison
        if 'market_cap_billions' in competitor_df.columns:
            top_competitors = competitor_df.nlargest(10, 'market_cap_billions')
            ax1.barh(top_competitors['company'], top_competitors['market_cap_billions'], 
                    color='gold', alpha=0.7)
            ax1.set_title('Market Cap Comparison (Top 10)')
            ax1.set_xlabel('Market Cap (Billions $)')
        
        # EV deliveries comparison
        if 'ev_deliveries' in competitor_df.columns:
            ev_data = competitor_df.dropna(subset=['ev_deliveries'])
            ax2.bar(ev_data['company'], ev_data['ev_deliveries'], 
                   color='lightblue', alpha=0.7)
            ax2.set_title('EV Deliveries Comparison')
            ax2.set_ylabel('Deliveries')
            ax2.tick_params(axis='x', rotation=45)
        
        # Revenue comparison
        if 'revenue_millions' in competitor_df.columns:
            revenue_data = competitor_df.dropna(subset=['revenue_millions'])
            ax3.bar(revenue_data['company'], revenue_data['revenue_millions'], 
                   color='lightcoral', alpha=0.7)
            ax3.set_title('Revenue Comparison')
            ax3.set_ylabel('Revenue (Millions $)')
            ax3.tick_params(axis='x', rotation=45)
        
        # Analyst ratings
        if 'analyst_rating' in competitor_df.columns:
            rating_data = competitor_df.dropna(subset=['analyst_rating'])
            ax4.bar(rating_data['company'], rating_data['analyst_rating'], 
                   color='lightgreen', alpha=0.7)
            ax4.set_title('Analyst Ratings')
            ax4.set_ylabel('Rating')
            ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def create_dashboard(self) -> None:
        """
        Create a comprehensive dashboard with all key metrics.
        """
        print("📊 Creating Tesla Investment Dashboard...")
        
        # Load all data
        data = self.parser.load_all_data()
        
        # Create dashboard
        fig = plt.figure(figsize=(20, 16))
        
        # Financial metrics
        if not data['financial_metrics'].empty:
            ax1 = plt.subplot(3, 3, 1)
            latest_financial = data['financial_metrics'].iloc[0]
            metrics = ['revenue_millions', 'net_income_millions', 'deliveries']
            values = [latest_financial[m] for m in metrics if m in latest_financial.index]
            labels = [m.replace('_', ' ').title() for m in metrics if m in latest_financial.index]
            
            if values:
                ax1.bar(labels, values, color=['blue', 'green', 'orange'], alpha=0.7)
                ax1.set_title('Latest Financial Metrics')
                ax1.tick_params(axis='x', rotation=45)
        
        # Sentiment trend
        if not data['market_sentiment'].empty:
            ax2 = plt.subplot(3, 3, 2)
            recent_sentiment = data['market_sentiment'].tail(10)
            ax2.plot(recent_sentiment['date'], recent_sentiment['sentiment_score'], 
                    marker='o', linewidth=2)
            ax2.set_title('Recent Sentiment Trend')
            ax2.set_ylabel('Sentiment Score')
            ax2.grid(True, alpha=0.3)
        
        # Product ratings
        if 'product_reviews' in data and not data['product_reviews']['reviews'].empty:
            ax3 = plt.subplot(3, 3, 3)
            reviews_df = data['product_reviews']['reviews']
            if 'rating' in reviews_df.columns:
                avg_ratings = reviews_df.groupby('product_name')['rating'].mean()
                ax3.bar(avg_ratings.index, avg_ratings.values, color='skyblue', alpha=0.7)
                ax3.set_title('Product Ratings')
                ax3.set_ylabel('Average Rating')
                ax3.tick_params(axis='x', rotation=45)
        
        # Market cap trend
        if not data['financial_metrics'].empty:
            ax4 = plt.subplot(3, 3, 4)
            financial_df = data['financial_metrics']
            if 'market_cap_billions' in financial_df.columns:
                ax4.plot(financial_df['date'], financial_df['market_cap_billions'], 
                        marker='o', linewidth=2, color='purple')
                ax4.set_title('Market Cap Trend')
                ax4.set_ylabel('Market Cap (Billions $)')
                ax4.grid(True, alpha=0.3)
        
        # Sentiment distribution
        if not data['market_sentiment'].empty:
            ax5 = plt.subplot(3, 3, 5)
            sentiment_df = data['market_sentiment']
            sentiment_df['sentiment_category'].value_counts().plot(kind='pie', ax=ax5)
            ax5.set_title('Sentiment Distribution')
        
        # Revenue growth
        if not data['financial_metrics'].empty:
            ax6 = plt.subplot(3, 3, 6)
            financial_df = data['financial_metrics']
            if 'revenue_millions' in financial_df.columns:
                revenue_growth = financial_df['revenue_millions'].pct_change() * 100
                ax6.plot(financial_df['date'], revenue_growth, marker='o', linewidth=2, color='red')
                ax6.set_title('Revenue Growth Rate')
                ax6.set_ylabel('Growth Rate (%)')
                ax6.grid(True, alpha=0.3)
        
        # Competitor market caps
        if not data['competitor_analysis'].empty:
            ax7 = plt.subplot(3, 3, 7)
            competitor_df = data['competitor_analysis']
            if 'market_cap_billions' in competitor_df.columns:
                top_competitors = competitor_df.nlargest(5, 'market_cap_billions')
                ax7.barh(top_competitors['company'], top_competitors['market_cap_billions'], 
                        color='gold', alpha=0.7)
                ax7.set_title('Top 5 Competitors by Market Cap')
                ax7.set_xlabel('Market Cap (Billions $)')
        
        # Delivery trend
        if not data['financial_metrics'].empty:
            ax8 = plt.subplot(3, 3, 8)
            financial_df = data['financial_metrics']
            if 'deliveries' in financial_df.columns:
                ax8.plot(financial_df['date'], financial_df['deliveries'], 
                        marker='o', linewidth=2, color='green')
                ax8.set_title('Vehicle Deliveries Trend')
                ax8.set_ylabel('Deliveries')
                ax8.grid(True, alpha=0.3)
        
        # Investment summary
        ax9 = plt.subplot(3, 3, 9)
        summary_data = {
            'Financial': len(data['financial_metrics']),
            'Sentiment': len(data['market_sentiment']),
            'Products': len(data['product_reviews']['products']) if 'product_reviews' in data else 0,
            'Competitors': len(data['competitor_analysis']),
            'Research': len(data['research_papers'])
        }
        ax9.bar(summary_data.keys(), summary_data.values(), color='lightblue', alpha=0.7)
        ax9.set_title('Data Coverage Summary')
        ax9.set_ylabel('Number of Records')
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Dashboard created successfully!")

# Example usage
if __name__ == "__main__":
    from data_parser import TeslaDataParser
    
    # Initialize parser and visualizer
    parser = TeslaDataParser()
    visualizer = TeslaDataVisualizer(parser)
    
    # Create visualizations
    print("📊 Creating Tesla Investment Visualizations...")
    
    # Financial trends
    visualizer.plot_financial_trends()
    
    # Sentiment analysis
    visualizer.plot_sentiment_analysis()
    
    # Product analysis
    visualizer.plot_product_analysis()
    
    # Competitor analysis
    visualizer.plot_competitor_analysis()
    
    # Comprehensive dashboard
    visualizer.create_dashboard()
    
    print("✅ All visualizations completed!") 