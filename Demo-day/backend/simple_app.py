from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Mock database for demo
credit_applications = []
users = []

@app.route('/')
def home():
    return jsonify({
        'message': 'AI Credit Assistant Backend is Running!',
        'status': 'active',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/api/health',
            '/api/credit-analysis',
            '/api/chat',
            '/api/what-if',
            '/api/llm-concepts/demo'
        ]
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AI Credit Assistant Backend',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/credit-analysis', methods=['POST'])
def credit_analysis():
    try:
        data = request.get_json()
        
        # Extract credit score from the request
        credit_score = data.get('currentCreditScore', 700)
        
        # Calculate a realistic range based on the entered score
        score_range = f"{max(300, credit_score - 50)}-{min(850, credit_score + 50)}"
        
        # Educational analysis result
        result = {
            'analysisType': 'Educational Credit Analysis',
            'disclaimer': 'This is an educational tool. For your actual credit score, please check with official credit bureaus.',
            'creditScoreRange': f'Based on your inputs, your score would likely be in the {score_range} range',
            'enteredCreditScore': credit_score,
            'riskLevel': 'Educational Assessment',
            'confidence': 'Educational purposes only',
            'approvalRecommendation': 'Educational guidance only',
            'factors': [
                {
                    'factor': 'Payment History',
                    'impact': 'Educational',
                    'score': 'N/A',
                    'explanation': 'Payment history accounts for 35% of your FICO score. Always pay bills on time to maintain good credit.'
                },
                {
                    'factor': 'Credit Utilization',
                    'impact': 'Educational',
                    'score': 'N/A',
                    'explanation': 'Credit utilization should stay below 30%. This means if you have $10,000 in credit, keep balances under $3,000.'
                },
                {
                    'factor': 'Length of Credit History',
                    'impact': 'Educational',
                    'score': 'N/A',
                    'explanation': 'Longer credit history generally means better scores. Keep old accounts open when possible.'
                },
                {
                    'factor': 'Credit Mix',
                    'impact': 'Educational',
                    'score': 'N/A',
                    'explanation': 'Having different types of credit (credit cards, loans, mortgages) can improve your score.'
                },
                {
                    'factor': 'New Credit',
                    'impact': 'Educational',
                    'score': 'N/A',
                    'explanation': 'Opening too many new accounts quickly can temporarily lower your score. Space out applications.'
                }
            ],
            'aiInsights': [
                'This is an educational analysis to help you understand credit factors',
                'Your actual credit score may vary based on many factors',
                'Always check with official credit bureaus for your real score',
                'Focus on building good credit habits rather than obsessing over numbers'
            ],
            'recommendations': [
                'Pay all bills on time - this is the most important factor',
                'Keep credit card balances below 30% of your limit',
                'Don\'t close old credit accounts unless necessary',
                'Only apply for new credit when you really need it',
                'Monitor your credit report regularly for errors'
            ],
            'educationalTips': [
                'Credit scores range from 300-850, with 670+ considered good',
                'Payment history accounts for 35% of your FICO score',
                'Credit utilization should ideally stay below 30%',
                'Hard inquiries stay on your report for 2 years but only affect scores for 1 year',
                'Length of credit history accounts for 15% of your score',
                'You can get free credit reports from annualcreditreport.com'
            ]
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Credit analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_score = data.get('userScore', 700)
        
        # Simple AI responses based on common questions
        responses = {
            "Why did my credit score drop?": f"With your credit score of {user_score}, the most likely reasons for a drop are: 1) Increased credit utilization above 30%, 2) Recent credit inquiries, 3) Late payments, or 4) Reduced credit limits. To improve: focus on paying down balances and making all payments on time.",
            "What can I do to increase my score?": f"To improve your {user_score} score: 1) Pay down credit card balances to reduce utilization below 30%, 2) Continue making all payments on time, 3) Avoid opening new accounts for 6 months, 4) Consider becoming an authorized user on someone's account with good credit, 5) Check for errors on your credit report.",
            "How does credit utilization affect my score?": f"Credit utilization accounts for 30% of your FICO score. With your current score of {user_score}, keeping utilization below 30% is crucial. If your utilization is high, paying down balances could significantly improve your score.",
            "What's the impact of opening a new credit card?": f"For someone with a {user_score} score, opening a new credit card could temporarily lower your score by 5-10 points due to the hard inquiry. However, if managed well, it could help long-term by increasing your total credit limit and improving your credit mix.",
            "How long do late payments stay on my report?": f"Late payments can stay on your credit report for up to 7 years, but their impact decreases over time. With your {user_score} score, avoiding late payments is especially important as they can cause significant drops. Always pay on time!",
            "What's a good credit utilization ratio?": f"A good credit utilization ratio is 30% or less. With your {user_score} score, keeping utilization low is key. Aim for under 10% for optimal results. Lower utilization = higher score potential."
        }
        
        # Find the best matching response
        response = "I'm here to help you understand credit scores and provide educational guidance. What specific question do you have about your credit?"
        
        for key, value in responses.items():
            if key.lower() in message.lower():
                response = value
                break
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/what-if', methods=['POST'])
def what_if_scenario():
    try:
        data = request.get_json()
        scenario = data.get('scenario', '')
        base_score = data.get('baseScore', 700)
        
        scenarios = {
            "pay off credit card": {
                "title": "Paying Off Credit Card Balance",
                "currentScore": base_score,
                "newScore": base_score + 25,
                "impact": "+25 points",
                "explanation": "Paying off your credit card would reduce your utilization from 45% to 15%, significantly improving your score.",
                "timeline": "Impact would be seen within 1-2 billing cycles"
            },
            "open new credit card": {
                "title": "Opening New Credit Card",
                "currentScore": base_score,
                "newScore": base_score - 8,
                "impact": "-8 points",
                "explanation": "Opening a new card would add a hard inquiry and reduce average account age, but increase total credit limit.",
                "timeline": "Temporary dip, but could improve score long-term"
            },
            "miss payment": {
                "title": "Missing a Payment",
                "currentScore": base_score,
                "newScore": base_score - 60,
                "impact": "-60 points",
                "explanation": "Missing a payment would significantly damage your excellent payment history, the most important credit factor.",
                "timeline": "Impact would be immediate and long-lasting"
            },
            "reduce credit utilization": {
                "title": "Reducing Credit Utilization",
                "currentScore": base_score,
                "newScore": base_score + 15,
                "impact": "+15 points",
                "explanation": "Reducing your credit utilization from 45% to 30% would improve your score by showing better credit management.",
                "timeline": "Impact would be seen within 1-2 billing cycles"
            },
            "pay off student loan": {
                "title": "Paying Off Student Loan",
                "currentScore": base_score,
                "newScore": base_score + 10,
                "impact": "+10 points",
                "explanation": "Paying off a student loan would improve your debt-to-income ratio and show responsible debt management.",
                "timeline": "Impact would be seen within 1-2 months"
            }
        }
        
        result = scenarios.get(scenario.lower(), {
            "title": "Custom Scenario",
            "currentScore": base_score,
            "newScore": base_score + random.randint(-10, 20),
            "impact": "Variable impact",
            "explanation": "This scenario would have a moderate impact on your credit score.",
            "timeline": "Impact timeline varies"
        })
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"What-if scenario error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm-concepts/demo', methods=['POST'])
def llm_concepts_demo():
    try:
        data = request.get_json()
        query = data.get('query', 'credit score analysis')
        
        # Mock demonstration of LLM concepts
        results = {
            'message': 'LLM Concepts Demo - Educational Purposes Only',
            'query': query,
            'concepts_demonstrated': {
                'langchain_openai': {
                    'status': '✅ Simulated',
                    'description': 'LangChain with OpenAI integration for credit analysis',
                    'sample_result': 'Educational credit analysis completed using AI models'
                },
                'ragas_evaluation': {
                    'status': '✅ Simulated',
                    'description': 'RAGAS evaluation for response quality assessment',
                    'sample_result': 'Response quality: High, Relevance: 0.95, Faithfulness: 0.92'
                },
                'multi_agent_system': {
                    'status': '✅ Simulated',
                    'description': 'Multi-agent system for specialized credit analysis',
                    'sample_result': 'Credit analysis agent processed request successfully'
                },
                'arxiv_integration': {
                    'status': '✅ Simulated',
                    'description': 'ArXiv research paper integration',
                    'sample_result': 'Found 3 research papers related to credit scoring models'
                },
                'tavily_search': {
                    'status': '✅ Simulated',
                    'description': 'Tavily web search integration',
                    'sample_result': 'Retrieved latest credit industry news and trends'
                },
                'synthetic_data_generation': {
                    'status': '✅ Simulated',
                    'description': 'Synthetic credit data generation',
                    'sample_result': 'Generated 3 synthetic credit application records'
                },
                'mcp_tool_integration': {
                    'status': '✅ Simulated',
                    'description': 'MCP-like tool integration',
                    'sample_result': 'Financial calculator and credit score simulator tools available'
                },
                'langsmith_tracing': {
                    'status': '✅ Simulated',
                    'description': 'LangSmith experiment tracking',
                    'sample_result': 'Experiment tracked in LangSmith project: AIE7-CREDIT-RISK-ANALYZER'
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"LLM concepts demo error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Credit Assistant Backend...")
    print("📍 Backend will be available at: http://localhost:5001")
    print("🔗 Frontend should connect to: http://localhost:3000")
    print("📚 This is a simplified demo version for educational purposes")
    app.run(debug=True, host='0.0.0.0', port=5001)
