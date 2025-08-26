import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  DollarSign, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Activity,
  MessageCircle,
  Lightbulb,
  Target,
  BookOpen,
  Shield,
  Zap
} from 'lucide-react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setIsLoading(false), 1000);
  }, []);

  // Mock data - replace with actual API calls
  const stats = [
    {
      title: 'Users Helped',
      value: '2,847',
      change: '+18.5%',
      changeType: 'positive',
      icon: Users,
      color: 'bg-blue-500',
      description: 'People who got credit insights'
    },
    {
      title: 'Questions Answered',
      value: '15,392',
      change: '+32.1%',
      changeType: 'positive',
      icon: MessageCircle,
      color: 'bg-green-500',
      description: 'AI credit questions resolved'
    },
    {
      title: 'Average Score Improvement',
      value: '+45 pts',
      change: '+12.3%',
      changeType: 'positive',
      icon: TrendingUp,
      color: 'bg-purple-500',
      description: 'After following AI advice'
    },
    {
      title: 'User Satisfaction',
      value: '94.2%',
      change: '+5.7%',
      changeType: 'positive',
      icon: CheckCircle,
      color: 'bg-yellow-500',
      description: 'Happy with AI assistance'
    },
  ];

  const recentActivity = [
    {
      id: 1,
      type: 'question',
      message: 'User asked: "Why did my score drop?"',
      time: '2 minutes ago',
      status: 'answered',
      aiResponse: 'Explained credit utilization impact'
    },
    {
      id: 2,
      type: 'scenario',
      message: 'User ran "what-if" scenario: Paying off credit card',
      time: '15 minutes ago',
      status: 'completed',
      aiResponse: 'Showed +25 point improvement'
    },
    {
      id: 3,
      type: 'analysis',
      message: 'New credit profile analyzed for Sarah Wilson',
      time: '1 hour ago',
      status: 'completed',
      aiResponse: 'Provided personalized recommendations'
    },
    {
      id: 4,
      type: 'education',
      message: 'User learned about credit utilization ratios',
      time: '2 hours ago',
      status: 'completed',
      aiResponse: 'Educational tip delivered'
    },
  ];

  const aiFeatures = [
    {
      title: 'Smart Credit Analysis',
      description: 'AI analyzes your credit profile and explains each factor in simple terms',
      icon: Shield,
      color: 'bg-blue-100 text-blue-600'
    },
    {
      title: 'Interactive Q&A',
      description: 'Ask any credit question and get personalized, easy-to-understand answers',
      icon: MessageCircle,
      color: 'bg-green-100 text-green-600'
    },
    {
      title: 'What-If Scenarios',
      description: 'See how different actions would affect your credit score in real-time',
      icon: Target,
      color: 'bg-purple-100 text-purple-600'
    },
    {
      title: 'Educational Tips',
      description: 'Learn about credit scores with bite-sized, actionable advice',
      icon: BookOpen,
      color: 'bg-yellow-100 text-yellow-600'
    }
  ];

  const chartData = {
    creditScores: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [
        {
          label: 'Average Credit Score',
          data: [680, 695, 710, 705, 720, 724],
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
        },
      ],
    },
    questionsAnswered: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [
        {
          label: 'Questions Answered',
          data: [1200, 1350, 1500, 1400, 1600, 1800],
          backgroundColor: 'rgba(34, 197, 94, 0.8)',
        },
        {
          label: 'User Satisfaction',
          data: [85, 88, 90, 89, 92, 94],
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
        },
      ],
    },
    scoreImprovements: {
      labels: ['0-10 pts', '11-25 pts', '26-50 pts', '51-75 pts', '76+ pts'],
      datasets: [
        {
          data: [15, 25, 35, 20, 5],
          backgroundColor: [
            'rgba(239, 68, 68, 0.8)',
            'rgba(251, 191, 36, 0.8)',
            'rgba(59, 130, 246, 0.8)',
            'rgba(34, 197, 94, 0.8)',
            'rgba(139, 92, 246, 0.8)',
          ],
        },
      ],
    },
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Credit Assistant Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Making credit scores understandable and actionable with AI
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Try AI Assistant
          </button>
        </div>
      </div>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-white">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center space-x-3 mb-4">
            <Zap className="h-8 w-8" />
            <h2 className="text-2xl font-bold">Your AI Credit Assistant</h2>
          </div>
          <p className="text-xl mb-6 opacity-90">
            Get personalized credit insights, ask questions, and see how different actions affect your score. 
            No more confusing numbers - just clear, actionable advice.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white bg-opacity-10 rounded-lg p-4">
              <h3 className="font-semibold mb-2">Ask Questions</h3>
              <p className="text-sm opacity-90">"Why did my score drop?" or "How can I improve it?"</p>
            </div>
            <div className="bg-white bg-opacity-10 rounded-lg p-4">
              <h3 className="font-semibold mb-2">Try Scenarios</h3>
              <p className="text-sm opacity-90">See what happens if you pay off debt or open new accounts</p>
            </div>
            <div className="bg-white bg-opacity-10 rounded-lg p-4">
              <h3 className="font-semibold mb-2">Get Educated</h3>
              <p className="text-sm opacity-90">Learn about credit factors and best practices</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                  <p className="text-xs text-gray-500 mt-1">{stat.description}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
              <div className="mt-4 flex items-center">
                {stat.changeType === 'positive' ? (
                  <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                ) : (
                  <TrendingDown className="h-4 w-4 text-red-500 mr-1" />
                )}
                <span
                  className={`text-sm font-medium ${
                    stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {stat.change}
                </span>
                <span className="text-sm text-gray-500 ml-1">from last month</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* AI Features */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">How Our AI Helps You</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {aiFeatures.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="text-center">
                <div className={`${feature.color} p-4 rounded-lg inline-block mb-4`}>
                  <Icon className="h-8 w-8" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Credit Score Trend */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Credit Score Improvements</h3>
          <Line data={chartData.creditScores} options={chartOptions} />
        </div>

        {/* Questions and Satisfaction */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Assistant Activity</h3>
          <Bar data={chartData.questionsAnswered} options={chartOptions} />
        </div>
      </div>

      {/* Score Improvements and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Score Improvement Distribution */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Score Improvement Distribution</h3>
          <div className="h-64">
            <Doughnut data={chartData.scoreImprovements} options={chartOptions} />
          </div>
        </div>

        {/* Recent AI Activity */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent AI Interactions</h3>
          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  {activity.type === 'question' && (
                    <MessageCircle className="h-5 w-5 text-blue-500" />
                  )}
                  {activity.type === 'scenario' && (
                    <Target className="h-5 w-5 text-green-500" />
                  )}
                  {activity.type === 'analysis' && (
                    <Shield className="h-5 w-5 text-purple-500" />
                  )}
                  {activity.type === 'education' && (
                    <BookOpen className="h-5 w-5 text-yellow-500" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">{activity.message}</p>
                  <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                  <p className="text-xs text-blue-600 mt-1">{activity.aiResponse}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Demo Call-to-Action */}
      <div className="bg-gradient-to-r from-green-500 to-blue-500 rounded-lg p-8 text-white text-center">
        <Lightbulb className="h-12 w-12 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-4">Ready to Understand Your Credit?</h2>
        <p className="text-lg mb-6 opacity-90">
          Our AI assistant makes credit scores simple and actionable. 
          Get personalized insights, ask questions, and see real-time scenarios.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
            Start Credit Analysis
          </button>
          <button className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
            Learn More
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
