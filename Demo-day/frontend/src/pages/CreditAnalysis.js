import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { 
  Calculator, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Download,
  RefreshCw,
  Eye,
  EyeOff,
  MessageCircle,
  Lightbulb,
  Target,
  HelpCircle,
  Play,
  RotateCcw
} from 'lucide-react';
import toast from 'react-hot-toast';

const CreditAnalysis = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showWhatIf, setShowWhatIf] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [whatIfScenario, setWhatIfScenario] = useState('');
  const [whatIfResult, setWhatIfResult] = useState(null);
  const [isRunningScenario, setIsRunningScenario] = useState(false);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm();

  // Pre-defined questions for demo
  const demoQuestions = [
    "Why did my credit score drop?",
    "What can I do to increase my score?",
    "How does credit utilization affect my score?",
    "What's the impact of opening a new credit card?",
    "How long do late payments stay on my report?",
    "What's a good credit utilization ratio?"
  ];

  const onSubmit = async (data) => {
    setIsAnalyzing(true);
    
    // Get the credit score from the form data
    const enteredCreditScore = parseInt(data.currentCreditScore) || 700;
    
    // Calculate a realistic range based on the entered score
    const scoreRange = `${Math.max(300, enteredCreditScore - 50)}-${Math.min(850, enteredCreditScore + 50)}`;
    
    // Educational analysis - using the entered credit score
    setTimeout(() => {
      const educationalResult = {
        analysisType: 'Educational Credit Analysis',
        disclaimer: 'This is an educational tool. For your actual credit score, please check with official credit bureaus.',
        creditScoreRange: `Based on your inputs, your score would likely be in the ${scoreRange} range`,
        enteredCreditScore: enteredCreditScore, // Store the actual entered score
        riskLevel: 'Educational Assessment',
        confidence: 'Educational purposes only',
        approvalRecommendation: 'Educational guidance only',
        factors: [
          { 
            factor: 'Payment History', 
            impact: 'Educational', 
            score: 'N/A', 
            explanation: 'Payment history accounts for 35% of your FICO score. Always pay bills on time to maintain good credit.' 
          },
          { 
            factor: 'Credit Utilization', 
            impact: 'Educational', 
            score: 'N/A', 
            explanation: 'Credit utilization should stay below 30%. This means if you have $10,000 in credit, keep balances under $3,000.' 
          },
          { 
            factor: 'Length of Credit History', 
            impact: 'Educational', 
            score: 'N/A', 
            explanation: 'Longer credit history generally means better scores. Keep old accounts open when possible.' 
          },
          { 
            factor: 'Credit Mix', 
            impact: 'Educational', 
            score: 'N/A', 
            explanation: 'Having different types of credit (credit cards, loans, mortgages) can improve your score.' 
          },
          { 
            factor: 'New Credit', 
            impact: 'Educational', 
            score: 'N/A', 
            explanation: 'Opening too many new accounts quickly can temporarily lower your score. Space out applications.' 
          },
        ],
        aiInsights: [
          'This is an educational analysis to help you understand credit factors',
          'Your actual credit score may vary based on many factors',
          'Always check with official credit bureaus for your real score',
          'Focus on building good credit habits rather than obsessing over numbers',
        ],
        recommendations: [
          'Pay all bills on time - this is the most important factor',
          'Keep credit card balances below 30% of your limit',
          'Don\'t close old credit accounts unless necessary',
          'Only apply for new credit when you really need it',
          'Monitor your credit report regularly for errors',
        ],
        educationalTips: [
          'Credit scores range from 300-850, with 670+ considered good',
          'Payment history accounts for 35% of your FICO score',
          'Credit utilization should ideally stay below 30%',
          'Hard inquiries stay on your report for 2 years but only affect scores for 1 year',
          'Length of credit history accounts for 15% of your score',
          'You can get free credit reports from annualcreditreport.com'
        ]
      };
      
      setAnalysisResult(educationalResult);
      setIsAnalyzing(false);
      toast.success('Credit analysis completed! Ask me anything about your score!');
    }, 3000);
  };

  const handleChatMessage = async (message) => {
    if (!message.trim()) return;

    const userMessage = { type: 'user', content: message, timestamp: new Date() };
    setChatMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');

    // Simulate AI response
    setTimeout(() => {
      // Get the user's credit score for personalized responses
      const userScore = analysisResult?.enteredCreditScore || 700;
      
      const aiResponses = {
        "Why did my credit score drop?": `With your credit score of ${userScore}, the most likely reasons for a drop are: 1) Increased credit utilization above 30%, 2) Recent credit inquiries, 3) Late payments, or 4) Reduced credit limits. To improve: focus on paying down balances and making all payments on time.`,
        "What can I do to increase my score?": `To improve your ${userScore} score: 1) Pay down credit card balances to reduce utilization below 30%, 2) Continue making all payments on time, 3) Avoid opening new accounts for 6 months, 4) Consider becoming an authorized user on someone's account with good credit, 5) Check for errors on your credit report.`,
        "How does credit utilization affect my score?": `Credit utilization accounts for 30% of your FICO score. With your current score of ${userScore}, keeping utilization below 30% is crucial. If your utilization is high, paying down balances could significantly improve your score.`,
        "What's the impact of opening a new credit card?": `For someone with a ${userScore} score, opening a new credit card could temporarily lower your score by 5-10 points due to the hard inquiry. However, if managed well, it could help long-term by increasing your total credit limit and improving your credit mix.`,
        "How long do late payments stay on my report?": `Late payments can stay on your credit report for up to 7 years, but their impact decreases over time. With your ${userScore} score, avoiding late payments is especially important as they can cause significant drops. Always pay on time!`,
        "What's a good credit utilization ratio?": `A good credit utilization ratio is 30% or less. With your ${userScore} score, keeping utilization low is key. Aim for under 10% for optimal results. Lower utilization = higher score potential.`
      };

      const aiResponse = aiResponses[message] || "I can help explain your credit score factors, provide improvement tips, or answer questions about credit utilization, payment history, and more. What would you like to know?";
      
      const aiMessage = { type: 'ai', content: aiResponse, timestamp: new Date() };
      setChatMessages(prev => [...prev, aiMessage]);
    }, 1000);
  };

  const runWhatIfScenario = async () => {
    if (!whatIfScenario.trim()) return;

    setWhatIfResult(null);
    setIsRunningScenario(true);
    
    // Get base score from the entered credit score
    let baseScore = 700; // default
    if (analysisResult && analysisResult.enteredCreditScore) {
      // Use the actual credit score entered by the user
      baseScore = analysisResult.enteredCreditScore;
    } else if (analysisResult && analysisResult.creditScoreRange) {
      // Fallback to extracting from range if entered score not available
      const rangeMatch = analysisResult.creditScoreRange.match(/(\d+)-(\d+)/);
      if (rangeMatch) {
        const min = parseInt(rangeMatch[1]);
        const max = parseInt(rangeMatch[2]);
        baseScore = Math.floor((min + max) / 2);
      }
    } else {
      // If no analysis has been run, use a default score for educational purposes
      baseScore = 720;
    }
    
    // Simulate what-if analysis
    setTimeout(() => {
      const scenarios = {
        "pay off credit card": {
          title: "Paying Off Credit Card Balance",
          currentScore: baseScore,
          newScore: baseScore + 25,
          impact: "+25 points",
          explanation: "Paying off your credit card would reduce your utilization from 45% to 15%, significantly improving your score.",
          timeline: "Impact would be seen within 1-2 billing cycles"
        },
        "open new credit card": {
          title: "Opening New Credit Card",
          currentScore: baseScore,
          newScore: baseScore - 8,
          impact: "-8 points",
          explanation: "Opening a new card would add a hard inquiry and reduce average account age, but increase total credit limit.",
          timeline: "Temporary dip, but could improve score long-term"
        },
        "miss payment": {
          title: "Missing a Payment",
          currentScore: baseScore,
          newScore: baseScore - 60,
          impact: "-60 points",
          explanation: "Missing a payment would significantly damage your excellent payment history, the most important credit factor.",
          timeline: "Impact would be immediate and long-lasting"
        },
        "reduce credit utilization": {
          title: "Reducing Credit Utilization",
          currentScore: baseScore,
          newScore: baseScore + 15,
          impact: "+15 points",
          explanation: "Reducing your credit utilization from 45% to 30% would improve your score by showing better credit management.",
          timeline: "Impact would be seen within 1-2 billing cycles"
        },
        "pay off student loan": {
          title: "Paying Off Student Loan",
          currentScore: baseScore,
          newScore: baseScore + 10,
          impact: "+10 points",
          explanation: "Paying off a student loan would improve your debt-to-income ratio and show responsible debt management.",
          timeline: "Impact would be seen within 1-2 months"
        }
      };

      const scenario = scenarios[whatIfScenario.toLowerCase()] || {
        title: "Custom Scenario",
        currentScore: baseScore,
        newScore: baseScore + Math.floor(Math.random() * 20) - 10,
        impact: "Variable impact",
        explanation: "This scenario would have a moderate impact on your credit score.",
        timeline: "Impact timeline varies"
      };

      setWhatIfResult(scenario);
      setIsRunningScenario(false);
    }, 2000);
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'Low': return 'text-green-600 bg-green-100';
      case 'Medium': return 'text-yellow-600 bg-yellow-100';
      case 'High': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 750) return 'text-green-600';
    if (score >= 650) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Credit Education Assistant</h1>
          <p className="mt-2 text-gray-600">
            Learn about credit factors and get educational insights - not actual credit scores
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={() => setShowChat(!showChat)}
            className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <MessageCircle className="h-4 w-4" />
            <span>{showChat ? 'Hide' : 'Show'} AI Chat</span>
          </button>
          <button
            onClick={() => setShowWhatIf(!showWhatIf)}
            className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            <Target className="h-4 w-4" />
            <span>{showWhatIf ? 'Hide' : 'Show'} What-If Scenarios</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Analysis Form */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Educational Credit Profile Analysis</h2>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Personal Information */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Personal Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    {...register('firstName', { required: 'First name is required' })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.firstName && (
                    <p className="text-red-500 text-sm mt-1">{errors.firstName.message}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    {...register('lastName', { required: 'Last name is required' })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.lastName && (
                    <p className="text-red-500 text-sm mt-1">{errors.lastName.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Financial Information */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Financial Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Annual Income ($)
                  </label>
                  <input
                    type="number"
                    {...register('annualIncome', { 
                      required: 'Annual income is required',
                      min: { value: 0, message: 'Income must be positive' }
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.annualIncome && (
                    <p className="text-red-500 text-sm mt-1">{errors.annualIncome.message}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Employment Length (years)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    {...register('employmentLength', { 
                      required: 'Employment length is required',
                      min: { value: 0, message: 'Employment length must be positive' }
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.employmentLength && (
                    <p className="text-red-500 text-sm mt-1">{errors.employmentLength.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Credit Information */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Credit Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Current Credit Score
                  </label>
                  <input
                    type="number"
                    {...register('currentCreditScore', { 
                      required: 'Current credit score is required',
                      min: { value: 300, message: 'Credit score must be at least 300' },
                      max: { value: 850, message: 'Credit score cannot exceed 850' }
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.currentCreditScore && (
                    <p className="text-red-500 text-sm mt-1">{errors.currentCreditScore.message}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Credit Utilization (%)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    {...register('creditUtilization', { 
                      required: 'Credit utilization is required',
                      min: { value: 0, message: 'Utilization must be positive' },
                      max: { value: 100, message: 'Utilization cannot exceed 100%' }
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {errors.creditUtilization && (
                    <p className="text-red-500 text-sm mt-1">{errors.creditUtilization.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={isAnalyzing}
                className="flex-1 flex items-center justify-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isAnalyzing ? (
                  <>
                    <RefreshCw className="h-5 w-5 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Calculator className="h-5 w-5" />
                    <span>Analyze My Credit</span>
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={() => reset()}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Analysis Results */}
        <div className="space-y-6">
          {analysisResult ? (
            <>
              {/* Summary Card */}
              <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">{analysisResult.analysisType}</h2>
                
                {/* Educational Disclaimer */}
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                  <div className="flex items-start">
                    <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" />
                    <div>
                      <h4 className="text-sm font-medium text-yellow-800">Educational Tool Disclaimer</h4>
                      <p className="text-sm text-yellow-700 mt-1">{analysisResult.disclaimer}</p>
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">Your Entered Score</p>
                    <p className="text-xl font-bold text-blue-600">
                      {analysisResult.enteredCreditScore}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Based on your input
                    </p>
                  </div>
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">Estimated Range</p>
                    <p className="text-lg font-bold text-green-600">
                      {analysisResult.creditScoreRange}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Educational estimate
                    </p>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">AI Confidence</span>
                    <span className="text-sm font-medium text-gray-900">{analysisResult.confidence}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full" 
                      style={{ width: `${analysisResult.confidence}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Credit Factors */}
              <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Credit Score Breakdown</h3>
                <div className="space-y-4">
                  {analysisResult.factors.map((factor, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900">{factor.factor}</h4>
                        <span className="inline-block px-2 py-1 rounded text-xs font-medium text-blue-600 bg-blue-100">
                          {factor.impact}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{factor.explanation}</p>
                      <div className="flex items-center space-x-2">
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div 
                            className="h-2 rounded-full bg-blue-500"
                            style={{ width: '100%' }}
                          ></div>
                        </div>
                        <span className="text-xs text-gray-500">Educational</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* AI Chat */}
              {showChat && (
                <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Ask Your AI Credit Assistant</h3>
                  
                  {/* Quick Questions */}
                  <div className="mb-4">
                    <p className="text-sm text-gray-600 mb-2">Quick questions:</p>
                    <div className="flex flex-wrap gap-2">
                      {demoQuestions.map((question, index) => (
                        <button
                          key={index}
                          onClick={() => handleChatMessage(question)}
                          className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full hover:bg-blue-200 transition-colors"
                        >
                          {question}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Chat Messages */}
                  <div className="h-64 overflow-y-auto border border-gray-200 rounded-lg p-4 mb-4">
                    {chatMessages.length === 0 ? (
                      <p className="text-gray-500 text-center">Ask me anything about your credit score!</p>
                    ) : (
                      chatMessages.map((message, index) => (
                        <div key={index} className={`mb-4 ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
                          <div className={`inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                            message.type === 'user' 
                              ? 'bg-blue-600 text-white' 
                              : 'bg-gray-100 text-gray-900'
                          }`}>
                            <p className="text-sm">{message.content}</p>
                          </div>
                        </div>
                      ))
                    )}
                  </div>

                  {/* Chat Input */}
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={currentMessage}
                      onChange={(e) => setCurrentMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleChatMessage(currentMessage)}
                      placeholder="Ask about your credit score..."
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      onClick={() => handleChatMessage(currentMessage)}
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                    >
                      <MessageCircle className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              )}

              {/* What-If Scenarios */}
              {showWhatIf && (
                <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">What-If Scenarios</h3>
                  <p className="text-sm text-gray-600 mb-4">See how different actions would affect your credit score (educational estimates only)</p>
                  
                  {/* Educational Disclaimer */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                    <div className="flex items-start">
                      <AlertTriangle className="h-4 w-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
                      <div>
                        <p className="text-sm text-blue-800">
                          <strong>Educational Tool:</strong> These scenarios show estimated impacts for learning purposes. 
                          Actual results may vary based on your specific credit profile.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Scenario
                      </label>
                      <select
                        value={whatIfScenario}
                        onChange={(e) => setWhatIfScenario(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">Select a scenario...</option>
                        <option value="pay off credit card">Pay off credit card balance</option>
                        <option value="open new credit card">Open new credit card</option>
                        <option value="miss payment">Miss a payment</option>
                        <option value="reduce credit utilization">Reduce credit utilization</option>
                        <option value="pay off student loan">Pay off student loan</option>
                      </select>
                    </div>
                    
                    <button
                      onClick={runWhatIfScenario}
                      disabled={!whatIfScenario || isRunningScenario}
                      className="w-full flex items-center justify-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
                    >
                      {isRunningScenario ? (
                        <>
                          <RotateCcw className="h-4 w-4 animate-spin" />
                          <span>Running Scenario...</span>
                        </>
                      ) : (
                        <>
                          <Play className="h-4 w-4" />
                          <span>Run Scenario</span>
                        </>
                      )}
                    </button>

                    {whatIfResult && (
                      <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                        <h4 className="font-medium text-gray-900 mb-2">{whatIfResult.title}</h4>
                        <div className="grid grid-cols-2 gap-4 mb-3">
                          <div className="text-center">
                            <p className="text-sm text-gray-600">Current Score</p>
                            <p className="text-lg font-bold text-gray-900">{whatIfResult.currentScore}</p>
                          </div>
                          <div className="text-center">
                            <p className="text-sm text-gray-600">New Score</p>
                            <p className={`text-lg font-bold ${whatIfResult.newScore > whatIfResult.currentScore ? 'text-green-600' : 'text-red-600'}`}>
                              {whatIfResult.newScore}
                            </p>
                          </div>
                        </div>
                        <div className="text-center mb-3">
                          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                            whatIfResult.newScore > whatIfResult.currentScore ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'
                          }`}>
                            {whatIfResult.impact}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">{whatIfResult.explanation}</p>
                        <p className="text-xs text-gray-500">{whatIfResult.timeline}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Educational Tips */}
              <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Lightbulb className="h-5 w-5 text-yellow-500 mr-2" />
                  Credit Education Tips
                </h3>
                <div className="space-y-3">
                  {analysisResult.educationalTips.map((tip, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                      <p className="text-sm text-gray-700">{tip}</p>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
              <div className="text-center py-12">
                <HelpCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Analyze Your Credit</h3>
                <p className="text-gray-600 mb-4">
                  Fill out the form to get personalized credit insights and ask questions about your score
                </p>
                <div className="space-y-2 text-sm text-gray-500">
                  <p>• Understand what affects your credit score</p>
                  <p>• Get personalized improvement tips</p>
                  <p>• Ask questions about your credit</p>
                  <p>• Try "what-if" scenarios</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CreditAnalysis;
