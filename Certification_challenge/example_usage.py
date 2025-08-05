"""
Tesla Investment Tracker - Example Usage
Simple example showing how to use the data parser and visualizer.
"""

from data_parser import TeslaDataParser
from data_visualizer import TeslaDataVisualizer
import pandas as pd

def main():
    """
    Main function demonstrating data parsing and visualization.
    """
    print("🚀 Tesla Investment Tracker - Data Analysis Example")
    print("=" * 50)
    
    # Initialize parser
    parser = TeslaDataParser()
    
    # Load all data
    print("\n📊 Loading Tesla investment data...")
    data = parser.load_all_data()
    
    # Display data summary
    print("\n📈 Data Summary:")
    for key, value in data.items():
        if isinstance(value, pd.DataFrame):
            print(f"  {key}: {len(value)} records")
        elif isinstance(value, dict) and 'products' in value:
            print(f"  {key}: {len(value['products'])} products, {len(value['reviews'])} reviews")
    
    # Generate summaries
    print("\n💰 Financial Summary:")
    financial_summary = parser.get_financial_summary()
    for key, value in financial_summary.items():
        print(f"  {key}: {value}")
    
    print("\n📊 Sentiment Summary:")
    sentiment_summary = parser.get_sentiment_summary()
    for key, value in sentiment_summary.items():
        print(f"  {key}: {value}")
    
    print("\n🚗 Product Summary:")
    product_summary = parser.get_product_summary()
    for key, value in product_summary.items():
        print(f"  {key}: {value}")
    
    # Export analysis report
    print("\n📄 Exporting analysis report...")
    parser.export_analysis_report("tesla_analysis_report.json")
    
    # Create visualizations
    print("\n📊 Creating visualizations...")
    visualizer = TeslaDataVisualizer(parser)
    
    # Financial trends
    print("  📈 Plotting financial trends...")
    visualizer.plot_financial_trends(['revenue_millions', 'deliveries'])
    
    # Sentiment analysis
    print("  📊 Plotting sentiment analysis...")
    visualizer.plot_sentiment_analysis(days=10)
    
    # Product analysis
    print("  🚗 Plotting product analysis...")
    visualizer.plot_product_analysis()
    
    # Competitor analysis
    print("  🏢 Plotting competitor analysis...")
    visualizer.plot_competitor_analysis()
    
    # Comprehensive dashboard
    print("  📊 Creating comprehensive dashboard...")
    visualizer.create_dashboard()
    
    print("\n✅ Analysis complete! Check the generated visualizations and report.")

if __name__ == "__main__":
    main() 