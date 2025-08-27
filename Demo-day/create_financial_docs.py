import json

# Create sample financial news
financial_news = [
    {
        "title": "AI Revolution in Credit Risk Assessment",
        "content": "Financial institutions are increasingly adopting AI and machine learning for credit risk assessment. Traditional models are being enhanced with advanced algorithms that can process vast amounts of data including transaction history, social media activity, and alternative data sources.",
        "source": "financial_news",
        "date": "2024-01-15",
        "category": "credit_risk"
    },
    {
        "title": "Debt-to-Income Ratio Analysis in 2024",
        "content": "Debt-to-Income (DTI) ratio remains a critical metric in credit risk assessment. A DTI ratio below 36% is generally considered favorable, while ratios above 43% may indicate higher risk of default.",
        "source": "financial_news",
        "date": "2024-01-20",
        "category": "credit_metrics"
    }
]

# Save financial news
with open("data/financial_news/financial_news.json", "w") as f:
    json.dump(financial_news, f, indent=2)

print("✅ Created financial news documents")
