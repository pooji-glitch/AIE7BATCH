# Improved RAGAS Evaluation for GPT-4.1 Mini

import pandas as pd
import numpy as np
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    answer_correctness,
    answer_similarity
)

def run_improved_ragas_evaluation():
    """Run improved RAGAS evaluation with better debugging and error handling."""
    
    # Create evaluation dataset for GPT-4.1 Mini
    evaluation_data = [
        {
            "question": "What was Tesla's revenue in Q4 2023?",
            "contexts": ["Tesla's revenue in Q4 2023 was $25,167 million."],
            "answer": "Tesla's revenue in Q4 2023 was $25,167 million.",
            "ground_truth": "Tesla's revenue in Q4 2023 was $25,167 million."
        },
        {
            "question": "How many vehicles did Tesla deliver in Q4 2023?",
            "contexts": ["Tesla delivered 484,507 vehicles in Q4 2023."],
            "answer": "Tesla delivered 484,507 vehicles in Q4 2023.",
            "ground_truth": "Tesla delivered 484,507 vehicles in Q4 2023."
        },
        {
            "question": "What is Tesla's current market capitalization?",
            "contexts": ["Tesla's market capitalization is $810.2 billion."],
            "answer": "Tesla's current market capitalization is $810.2 billion.",
            "ground_truth": "Tesla's market capitalization is $810.2 billion."
        },
        {
            "question": "What is the average sentiment score for Tesla?",
            "contexts": ["Recent market sentiment analysis shows an average score of 0.72 over the last 5 days."],
            "answer": "The current market sentiment for Tesla is 0.72 on a scale of 0-1.",
            "ground_truth": "Tesla's current market sentiment score is 0.72 based on recent analysis."
        },
        {
            "question": "What is the average rating for Tesla Model 3?",
            "contexts": ["The Tesla Model 3 has an average rating of 4.6 out of 5 stars based on customer reviews."],
            "answer": "The Tesla Model 3 has an average rating of 4.6 out of 5 stars.",
            "ground_truth": "The Tesla Model 3's average rating is 4.6 stars."
        }
    ]

    # Convert to RAGAS Dataset format
    dataset_dict = {
        "question": [item["question"] for item in evaluation_data],
        "contexts": [item["contexts"] for item in evaluation_data],
        "answer": [item["answer"] for item in evaluation_data],
        "ground_truth": [item["ground_truth"] for item in evaluation_data]
    }

    dataset = Dataset.from_dict(dataset_dict)

    print("🔍 Running RAGAS evaluation for GPT-4.1 Mini...")

    # Run evaluation with all metrics
    metrics = [faithfulness, answer_relevancy, context_recall, answer_correctness, answer_similarity]
    results = evaluate(dataset, metrics)

    # Display results with better debugging
    print("\n" + "="*50)
    print("📊 RAGAS EVALUATION RESULTS - GPT-4.1 Mini")
    print("="*50)

    # Print raw results first to debug
    print("Raw results object:", results)
    print("Results type:", type(results))
    print("Available attributes:", dir(results))

    # Try different ways to access results
    evaluation_scores = {}

    # Method 1: Try accessing as attributes
    for metric in metrics:
        metric_name = metric.name if hasattr(metric, 'name') else str(metric)
        print(f"\nTrying to access {metric_name}...")
        
        # Try different access patterns
        if hasattr(results, metric_name):
            score = getattr(results, metric_name)
            evaluation_scores[metric_name] = float(score)
            print(f"✅ {metric_name}: {score:.3f}")
        elif hasattr(results, metric_name.lower()):
            score = getattr(results, metric_name.lower())
            evaluation_scores[metric_name] = float(score)
            print(f"✅ {metric_name}: {score:.3f}")
        else:
            print(f"❌ Could not access {metric_name}")

    # Method 2: Try accessing as dictionary
    if hasattr(results, '__dict__'):
        print("\nResults as dictionary:")
        for key, value in results.__dict__.items():
            if not key.startswith('_'):
                print(f"{key}: {value}")

    # Method 3: Try iterating over results
    if hasattr(results, 'items'):
        print("\nResults as items:")
        for key, value in results.items():
            print(f"{key}: {value}")

    # Method 4: Try accessing results directly
    try:
        print("\nDirect access to results:")
        print(f"Faithfulness: {results.faithfulness}")
        print(f"Answer Relevancy: {results.answer_relevancy}")
        print(f"Context Recall: {results.context_recall}")
        print(f"Answer Correctness: {results.answer_correctness}")
        print(f"Answer Similarity: {results.answer_similarity}")
        
        # Update evaluation scores
        evaluation_scores.update({
            'faithfulness': float(results.faithfulness),
            'answer_relevancy': float(results.answer_relevancy),
            'context_recall': float(results.context_recall),
            'answer_correctness': float(results.answer_correctness),
            'answer_similarity': float(results.answer_similarity)
        })
    except Exception as e:
        print(f"Direct access failed: {e}")

    # Overall assessment
    if evaluation_scores:
        avg_score = np.mean(list(evaluation_scores.values()))
        print(f"\n📈 Average Score: {avg_score:.3f}")
        if avg_score >= 0.8:
            print("🟢 Status: Excellent - GPT-4.1 Mini performing very well")
        elif avg_score >= 0.6:
            print("🟡 Status: Good - GPT-4.1 Mini performing adequately")
        else:
            print("🔴 Status: Needs Improvement - GPT-4.1 Mini requires optimization")
    else:
        print("\n⚠️ No scores could be extracted from results")

    print("\n✅ RAGAS evaluation completed!")
    return results, evaluation_scores

if __name__ == "__main__":
    results, scores = run_improved_ragas_evaluation() 