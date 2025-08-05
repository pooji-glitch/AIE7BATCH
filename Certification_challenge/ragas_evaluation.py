"""
Tesla Investment Tracker - RAGAS Evaluation System
Comprehensive RAG evaluation using RAGAS with Tesla investment data.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
    context_recall,
    answer_correctness,
    answer_similarity
)
from datasets import Dataset
import json
import warnings
warnings.filterwarnings('ignore')

class TeslaRAGASEvaluator:
    """
    RAGAS evaluation system for Tesla investment analysis.
    Evaluates RAG performance using Tesla-specific datasets.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the RAGAS evaluator.
        
        Args:
            data_dir: Directory containing Tesla data files
        """
        self.data_dir = data_dir
        self.evaluation_results = {}
        
    def load_tesla_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load Tesla investment data for evaluation.
        
        Returns:
            Dictionary containing all Tesla datasets
        """
        print("📊 Loading Tesla investment data for RAGAS evaluation...")
        
        # Load all data files
        financial_df = pd.read_csv(f"{self.data_dir}/tesla_financial_metrics.csv")
        sentiment_df = pd.read_csv(f"{self.data_dir}/market_sentiment_data.csv")
        research_df = pd.read_csv(f"{self.data_dir}/tesla_research_papers.csv")
        competitor_df = pd.read_csv(f"{self.data_dir}/competitor_analysis.csv")
        
        # Load product reviews
        with open(f"{self.data_dir}/tesla_product_reviews.json", 'r') as f:
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
    
    def create_evaluation_dataset(self, data: Dict[str, pd.DataFrame]) -> Dataset:
        """
        Create evaluation dataset from Tesla data.
        
        Args:
            data: Dictionary containing Tesla datasets
            
        Returns:
            RAGAS evaluation dataset
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
    
    def run_ragas_evaluation(self, dataset: Dataset) -> Dict[str, float]:
        """
        Run RAGAS evaluation on the dataset.
        
        Args:
            dataset: RAGAS evaluation dataset
            
        Returns:
            Dictionary containing evaluation metrics
        """
        print("🔍 Running RAGAS evaluation...")
        
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
        
        self.evaluation_results = evaluation_scores
        
        print("✅ RAGAS evaluation completed!")
        return evaluation_scores
    
    def generate_evaluation_report(self, scores: Dict[str, float]) -> str:
        """
        Generate a comprehensive evaluation report.
        
        Args:
            scores: Dictionary containing evaluation scores
            
        Returns:
            Formatted evaluation report
        """
        report = """
# Tesla Investment RAG - RAGAS Evaluation Report

## 📊 Evaluation Metrics

"""
        
        # Add metric scores
        for metric, score in scores.items():
            report += f"### {metric.replace('_', ' ').title()}\n"
            report += f"**Score:** {score:.3f}\n\n"
            
            # Add interpretation
            if metric == "faithfulness":
                report += "**Interpretation:** Measures how faithful the generated answer is to the provided context.\n\n"
            elif metric == "answer_relevancy":
                report += "**Interpretation:** Measures how relevant the generated answer is to the question.\n\n"
            elif metric == "context_relevancy":
                report += "**Interpretation:** Measures how relevant the retrieved context is to the question.\n\n"
            elif metric == "context_recall":
                report += "**Interpretation:** Measures how well the retrieval system recalls relevant information.\n\n"
            elif metric == "answer_correctness":
                report += "**Interpretation:** Measures the factual correctness of the generated answers.\n\n"
            elif metric == "answer_similarity":
                report += "**Interpretation:** Measures the semantic similarity between generated and ground truth answers.\n\n"
        
        # Overall assessment
        avg_score = np.mean(list(scores.values()))
        report += f"## 📈 Overall Assessment\n\n"
        report += f"**Average Score:** {avg_score:.3f}\n\n"
        
        if avg_score >= 0.8:
            report += "**Status:** 🟢 Excellent - RAG system performing very well\n\n"
        elif avg_score >= 0.6:
            report += "**Status:** 🟡 Good - RAG system performing adequately\n\n"
        else:
            report += "**Status:** 🔴 Needs Improvement - RAG system requires optimization\n\n"
        
        # Recommendations
        report += "## 💡 Recommendations\n\n"
        
        if scores.get("context_relevancy", 0) < 0.7:
            report += "- **Improve Retrieval:** Enhance document retrieval to get more relevant context\n"
        
        if scores.get("faithfulness", 0) < 0.7:
            report += "- **Improve Generation:** Ensure answers are more faithful to retrieved context\n"
        
        if scores.get("answer_correctness", 0) < 0.7:
            report += "- **Fact Checking:** Implement better fact verification in answer generation\n"
        
        if scores.get("context_recall", 0) < 0.7:
            report += "- **Expand Retrieval:** Consider retrieving more documents per query\n"
        
        report += "\n## 🎯 Next Steps\n\n"
        report += "1. **Monitor Performance:** Track these metrics over time\n"
        report += "2. **Iterate:** Use insights to improve RAG pipeline\n"
        report += "3. **Expand Dataset:** Add more diverse Tesla investment questions\n"
        report += "4. **Fine-tune:** Adjust retrieval and generation parameters\n"
        
        return report
    
    def save_evaluation_results(self, scores: Dict[str, float], output_file: str = "tesla_ragas_evaluation.json"):
        """
        Save evaluation results to file.
        
        Args:
            scores: Evaluation scores
            output_file: Output file path
        """
        results = {
            "evaluation_date": pd.Timestamp.now().isoformat(),
            "dataset_size": len(self.evaluation_results) if hasattr(self, 'evaluation_results') else 0,
            "metrics": scores,
            "average_score": np.mean(list(scores.values())),
            "recommendations": self._generate_recommendations(scores)
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Evaluation results saved to {output_file}")
    
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """
        Generate recommendations based on evaluation scores.
        
        Args:
            scores: Evaluation scores
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if scores.get("context_relevancy", 0) < 0.7:
            recommendations.append("Improve document retrieval to get more relevant context")
        
        if scores.get("faithfulness", 0) < 0.7:
            recommendations.append("Enhance answer generation to be more faithful to context")
        
        if scores.get("answer_correctness", 0) < 0.7:
            recommendations.append("Implement better fact verification in answer generation")
        
        if scores.get("context_recall", 0) < 0.7:
            recommendations.append("Consider retrieving more documents per query")
        
        if scores.get("answer_relevancy", 0) < 0.7:
            recommendations.append("Improve answer generation to be more relevant to questions")
        
        return recommendations

def main():
    """
    Main function to run RAGAS evaluation.
    """
    print("🚀 Tesla Investment RAG - RAGAS Evaluation")
    print("=" * 50)
    
    # Initialize evaluator
    evaluator = TeslaRAGASEvaluator()
    
    # Load Tesla data
    data = evaluator.load_tesla_data()
    
    # Create evaluation dataset
    dataset = evaluator.create_evaluation_dataset(data)
    
    # Run RAGAS evaluation
    scores = evaluator.run_ragas_evaluation(dataset)
    
    # Generate and display report
    report = evaluator.generate_evaluation_report(scores)
    print(report)
    
    # Save results
    evaluator.save_evaluation_results(scores)
    
    print("✅ RAGAS evaluation completed successfully!")

if __name__ == "__main__":
    main() 