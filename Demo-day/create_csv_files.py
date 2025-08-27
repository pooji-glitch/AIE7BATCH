import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate realistic credit application data
np.random.seed(42)
n_applications = 1000

data = {
    'application_id': [f'APP{i:04d}' for i in range(1, n_applications + 1)],
    'credit_score': np.random.normal(700, 100, n_applications).astype(int),
    'income': np.random.normal(65000, 25000, n_applications).astype(int),
    'debt_to_income': np.random.uniform(0.1, 0.8, n_applications),
    'payment_history': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], n_applications),
    'credit_utilization': np.random.uniform(0.05, 0.9, n_applications),
    'length_of_credit': np.random.uniform(1, 30, n_applications),
    'number_of_accounts': np.random.poisson(8, n_applications),
    'derogatory_marks': np.random.poisson(0.5, n_applications),
    'inquiries_last_6_months': np.random.poisson(2, n_applications),
    'employment_length': np.random.uniform(0, 20, n_applications),
    'home_ownership': np.random.choice(['Own', 'Rent', 'Mortgage'], n_applications),
    'loan_amount': np.random.uniform(10000, 500000, n_applications),
    'loan_term': np.random.choice([12, 24, 36, 48, 60], n_applications),
    'interest_rate': np.random.uniform(3.0, 15.0, n_applications)
}

df = pd.DataFrame(data)

# Calculate risk level and decision
df['risk_level'] = pd.cut(df['credit_score'], 
                         bins=[0, 580, 670, 740, 800, 850], 
                         labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])

df['decision'] = np.where(
    (df['credit_score'] >= 700) & (df['debt_to_income'] <= 0.43),
    'Approve',
    np.where(
        (df['credit_score'] >= 650) & (df['debt_to_income'] <= 0.5),
        'Review',
        'Decline'
    )
)

# Save to CSV
df.to_csv("data/csv_files/credit_applications.csv", index=False)
print("✅ Created: credit_applications.csv")

# Create market data
dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
market_data = {
    'date': dates,
    'interest_rate': np.random.normal(6.5, 1.5, len(dates)),
    'unemployment_rate': np.random.normal(3.7, 0.5, len(dates)),
    'gdp_growth': np.random.normal(2.1, 0.8, len(dates)),
    'inflation_rate': np.random.normal(3.0, 1.0, len(dates)),
    'market_volatility': np.random.uniform(0.1, 0.3, len(dates))
}

market_df = pd.DataFrame(market_data)
market_df.to_csv("data/csv_files/market_data.csv", index=False)
print("✅ Created: market_data.csv")

print("✅ All CSV files created successfully!")
