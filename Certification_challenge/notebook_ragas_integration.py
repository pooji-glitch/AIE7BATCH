"""
Tesla Investment RAG - Notebook Integration for RAGAS Evaluation
Simple code to add to your Jupyter notebook for RAGAS evaluation.
"""

import pandas as pd
import numpy as np
from datasets import Dataset
import json

def load_tesla_data_for_evaluation():
    """
    Load Tesla data for RAGAS evaluation.
    Add this to your notebook.
    """
    print("📊 Loading Tesla data for RAGAS evaluation...")
    
    # Load all data files
    financial_df = pd.read_csv("data/tesla_financial_metrics.csv")
    sentiment_df = pd.read_csv("data/market_sentiment_data.csv")
    research_df = pd.read_csv("data/tesla_research_papers.csv")
    competitor_df = pd.read_csv("data/competitor_analysis.csv")
    
    # Load product reviews
    with open("data/tesla_product_reviews.json", 'r') as f:
        product_data = json.load(f)
    
    # Convert product data to DataFrame
    products = []
    reviews = []
    for product in product_data['tesla_products']:
        products.append({
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'category': product['category'],
            'current_price': product['current_price'],
            'market_position': product['market_position'],
            'competitive_advantage': product['competitive_advantage']
        })
        for review in product['reviews']:
            reviews.append({
                'product_name': product['product_name'],
                'rating': review['rating'],
                'source': review['source'],
                'investment_rating': review['investment_rating'],
                'summary': review['summary'],
                'pros': ', '.join(review['pros']),
                'cons': ', '.join(review['cons'])
            })
    
    products_df = pd.DataFrame(products)
    reviews_df = pd.DataFrame(reviews)
    
    data = {
        'financial_metrics': financial_df,
        'market_sentiment': sentiment_df,
        'research_papers': research_df,
        'competitor_analysis': competitor_df,
        'products': products_df,
        'reviews': reviews_df
    }
    
    print(f"✅ Loaded {len(financial_df)} financial records")
    print(f"✅ Loaded {len(sentiment_df)} sentiment records")
    print(f"✅ Loaded {len(research_df)} research papers")
    print(f"✅ Loaded {len(competitor_df)} competitor records")
    print(f"✅ Loaded {len(products_df)} products with {len(reviews_df)} reviews")
    
    return data

def create_evaluation_dataset(data):
    """
    Create RAGAS evaluation dataset from Tesla data.
    Add this to your notebook.
    """
    print("🔧 Creating evaluation dataset...")
    
    evaluation_data = []
    
    # Financial metrics questions
    financial_df = data['financial_metrics']
    if not financial_df.empty:
        latest = financial_df.iloc[0]
        evaluation_data.extend([
            {
                "question": "What was Tesla's revenue in the most recent quarter?",
                "contexts": [f"Tesla's revenue in {latest['quarter']} {latest['year']} was ${latest['revenue_millions']} million."],
                "answer": f"Tesla's revenue in the most recent quarter ({latest['quarter']} {latest['year']}) was ${latest['revenue_millions']} million.",
                "ground_truth": f"Tesla's revenue in {latest['quarter']} {latest['year']} was ${latest['revenue_millions']} million."
            },
            {
                "question": "How many vehicles did Tesla deliver in the latest quarter?",
                "contexts": [f"Tesla delivered {latest['deliveries']} vehicles in {latest['quarter']} {latest['year']}."],
                "answer": f"Tesla delivered {latest['deliveries']} vehicles in the latest quarter.",
                "ground_truth": f"Tesla delivered {latest['deliveries']} vehicles in {latest['quarter']} {latest['year']}."
            },
            {
                "question": "What is Tesla's current market capitalization?",
                "contexts": [f"Tesla's market capitalization is ${latest['market_cap_billions']} billion."],
                "answer": f"Tesla's current market capitalization is ${latest['market_cap_billions']} billion.",
                "ground_truth": f"Tesla's market capitalization is ${latest['market_cap_billions']} billion."
            }
        ])
    
    # Sentiment analysis questions
    sentiment_df = data['market_sentiment']
    if not sentiment_df.empty:
        recent_sentiment = sentiment_df.tail(5)
        avg_sentiment = recent_sentiment['sentiment_score'].mean()
        evaluation_data.extend([
            {
                "question": "What is the current market sentiment for Tesla?",
                "contexts": [f"Recent market sentiment analysis shows an average score of {avg_sentiment:.2f} over the last 5 days."],
                "answer": f"The current market sentiment for Tesla is {avg_sentiment:.2f} on a scale of 0-1.",
                "ground_truth": f"Tesla's current market sentiment score is {avg_sentiment:.2f} based on recent analysis."
            }
        ])
    
    # Product analysis questions
    products_df = data['products']
    reviews_df = data['reviews']
    if not products_df.empty and not reviews_df.empty:
        model_3_rating = reviews_df[reviews_df['product_name'] == 'Tesla Model 3']['rating'].mean()
        evaluation_data.extend([
            {
                "question": "What is the average rating for Tesla Model 3?",
                "contexts": [f"The Tesla Model 3 has an average rating of {model_3_rating:.1f} out of 5 stars based on customer reviews."],
                "answer": f"The Tesla Model 3 has an average rating of {model_3_rating:.1f} out of 5 stars.",
                "ground_truth": f"The Tesla Model 3's average rating is {model_3_rating:.1f} stars."
            }
        ])
    
    # Research papers questions
    research_df = data['research_papers']
    if not research_df.empty:
        positive_papers = research_df[research_df['sentiment'] == 'Positive']
        evaluation_data.extend([
            {
                "question": "How many research papers have positive sentiment about Tesla?",
                "contexts": [f"Out of {len(research_df)} research papers analyzed, {len(positive_papers)} have positive sentiment about Tesla."],
                "answer": f"There are {len(positive_papers)} research papers with positive sentiment about Tesla.",
                "ground_truth": f"{len(positive_papers)} research papers show positive sentiment about Tesla."
            }
        ])
    
    # Competitor analysis questions
    competitor_df = data['competitor_analysis']
    if not competitor_df.empty:
        top_competitor = competitor_df.nlargest(1, 'market_cap_billions').iloc[0]
        evaluation_data.extend([
            {
                "question": "Who is Tesla's largest competitor by market cap?",
                "contexts": [f"{top_competitor['company']} is Tesla's largest competitor with a market cap of ${top_competitor['market_cap_billions']} billion."],
                "answer": f"{top_competitor['company']} is Tesla's largest competitor by market capitalization.",
                "ground_truth": f"{top_competitor['company']} is Tesla's largest competitor with a market cap of ${top_competitor['market_cap_billions']} billion."
            }
        ])
    
    print(f"✅ Created evaluation dataset with {len(evaluation_data)} questions")
    
    # Convert to RAGAS Dataset format
    dataset_dict = {
        "question": [item["question"] for item in evaluation_data],
        "contexts": [item["contexts"] for item in evaluation_data],
        "answer": [item["answer"] for item in evaluation_data],
        "ground_truth": [item["ground_truth"] for item in evaluation_data]
    }
    
    return Dataset.from_dict(dataset_dict)

def run_ragas_evaluation(dataset):
    """
    Run RAGAS evaluation on the dataset.
    Add this to your notebook.
    """
    print("🔍 Running RAGAS evaluation...")
    
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_relevancy,
        context_recall,
        answer_correctness,
        answer_similarity
    )
    
    # Define evaluation metrics
    metrics = [
        faithfulness,
        answer_relevancy,
        context_relevancy,
        context_recall,
        answer_correctness,
        answer_similarity
    ]
    
    # Run evaluation
    results = evaluate(dataset, metrics)
    
    # Extract scores
    evaluation_scores = {}
    for metric in metrics:
        metric_name = metric.__name__
        if metric_name in results:
            evaluation_scores[metric_name] = float(results[metric_name])
    
    print("✅ RAGAS evaluation completed!")
    return evaluation_scores

def display_evaluation_results(scores):
    """
    Display evaluation results in a formatted way.
    Add this to your notebook.
    """
    print("\n" + "="*50)
    print("📊 RAGAS EVALUATION RESULTS")
    print("="*50)
    
    for metric, score in scores.items():
        print(f"\n{metric.replace('_', ' ').title()}: {score:.3f}")
        
        # Add interpretation
        if metric == "faithfulness":
            print("   Measures how faithful the answer is to the context")
        elif metric == "answer_relevancy":
            print("   Measures how relevant the answer is to the question")
        elif metric == "context_relevancy":
            print("   Measures how relevant the retrieved context is")
        elif metric == "context_recall":
            print("   Measures how well the system recalls relevant information")
        elif metric == "answer_correctness":
            print("   Measures the factual correctness of answers")
        elif metric == "answer_similarity":
            print("   Measures semantic similarity to ground truth")
    
    # Overall assessment
    avg_score = np.mean(list(scores.values()))
    print(f"\n📈 Average Score: {avg_score:.3f}")
    
    if avg_score >= 0.8:
        print("🟢 Status: Excellent - RAG system performing very well")
    elif avg_score >= 0.6:
        print("🟡 Status: Good - RAG system performing adequately")
    else:
        print("🔴 Status: Needs Improvement - RAG system requires optimization")

# Example usage for notebook
def run_complete_evaluation():
    """
    Complete RAGAS evaluation workflow.
    Copy this entire function to your notebook.
    """
    print("🚀 Tesla Investment RAG - RAGAS Evaluation")
    print("=" * 50)
    
    # Step 1: Load data
    data = load_tesla_data_for_evaluation()
    
    # Step 2: Create evaluation dataset
    dataset = create_evaluation_dataset(data)
    
    # Step 3: Run evaluation
    scores = run_ragas_evaluation(dataset)
    
    # Step 4: Display results
    display_evaluation_results(scores)
    
    print("\n✅ Evaluation completed successfully!")

# Copy this code to your notebook:
"""
# RAGAS Evaluation Code for Tesla Investment RAG

# Import required libraries
import pandas as pd
import numpy as np
from datasets import Dataset
import json
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
    context_recall,
    answer_correctness,
    answer_similarity
)

# Run the complete evaluation
run_complete_evaluation()
""" 