import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Download, 
  Calendar, 
  TrendingUp, 
  TrendingDown,
  BarChart3,
  PieChart,
  Filter,
  RefreshCw,
  Eye,
  Printer
} from 'lucide-react';
import { Line, Bar, Doughnut, Pie } from 'react-chartjs-2';
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

const Reports = () => {
  const [selectedReport, setSelectedReport] = useState('credit-analysis');
  const [dateRange, setDateRange] = useState('month');
  const [isLoading, setIsLoading] = useState(false);
  const [reportData, setReportData] = useState(null);

  const reportTypes = [
    {
      id: 'credit-analysis',
      name: 'Credit Analysis Summary',
      description: 'Overview of credit scores and risk distribution',
      icon: BarChart3,
      color: 'bg-blue-500'
    },
    {
      id: 'approval-rates',
      name: 'Approval Rates Report',
      description: 'Monthly approval rates and trends',
      icon: TrendingUp,
      color: 'bg-green-500'
    },
    {
      id: 'risk-assessment',
      name: 'Risk Assessment Report',
      description: 'Detailed risk analysis by category',
      icon: PieChart,
      color: 'bg-yellow-500'
    },
    {
      id: 'performance-metrics',
      name: 'Performance Metrics',
      description: 'AI model performance and accuracy',
      icon: FileText,
      color: 'bg-purple-500'
    }
  ];

  const generateReport = async () => {
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      const mockData = {
        'credit-analysis': {
          title: 'Credit Analysis Summary Report',
          period: 'January 2024',
          summary: {
            totalApplications: 1247,
            averageCreditScore: 724,
            approvalRate: 78.3,
            averageProcessingTime: '2.4 hours'
          },
          charts: {
            creditScoreDistribution: {
              labels: ['300-500', '501-600', '601-700', '701-800', '801-850'],
              datasets: [{
                data: [5, 15, 30, 35, 15],
                backgroundColor: [
                  'rgba(239, 68, 68, 0.8)',
                  'rgba(251, 191, 36, 0.8)',
                  'rgba(59, 130, 246, 0.8)',
                  'rgba(34, 197, 94, 0.8)',
                  'rgba(139, 92, 246, 0.8)'
                ]
              }]
            },
            monthlyTrends: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
              datasets: [{
                label: 'Applications',
                data: [120, 135, 150, 140, 160, 180],
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4
              }]
            }
          }
        },
        'approval-rates': {
          title: 'Approval Rates Report',
          period: 'January 2024',
          summary: {
            overallApprovalRate: 78.3,
            lowRiskApprovalRate: 95.2,
            mediumRiskApprovalRate: 72.1,
            highRiskApprovalRate: 45.8
          },
          charts: {
            approvalTrends: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
              datasets: [{
                label: 'Approval Rate (%)',
                data: [75, 78, 82, 79, 81, 78.3],
                borderColor: 'rgb(34, 197, 94)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                tension: 0.4
              }]
            },
            approvalByRisk: {
              labels: ['Low Risk', 'Medium Risk', 'High Risk'],
              datasets: [{
                data: [95.2, 72.1, 45.8],
                backgroundColor: [
                  'rgba(34, 197, 94, 0.8)',
                  'rgba(251, 191, 36, 0.8)',
                  'rgba(239, 68, 68, 0.8)'
                ]
              }]
            }
          }
        },
        'risk-assessment': {
          title: 'Risk Assessment Report',
          period: 'January 2024',
          summary: {
            lowRiskApplications: 561,
            mediumRiskApplications: 436,
            highRiskApplications: 250,
            totalRiskScore: 6.2
          },
          charts: {
            riskDistribution: {
              labels: ['Low Risk', 'Medium Risk', 'High Risk'],
              datasets: [{
                data: [45, 35, 20],
                backgroundColor: [
                  'rgba(34, 197, 94, 0.8)',
                  'rgba(251, 191, 36, 0.8)',
                  'rgba(239, 68, 68, 0.8)'
                ]
              }]
            },
            riskFactors: {
              labels: ['Payment History', 'Credit Utilization', 'Length of Credit', 'Credit Mix', 'New Credit'],
              datasets: [{
                label: 'Risk Impact Score',
                data: [85, 65, 78, 72, 60],
                backgroundColor: 'rgba(59, 130, 246, 0.8)'
              }]
            }
          }
        },
        'performance-metrics': {
          title: 'AI Performance Metrics Report',
          period: 'January 2024',
          summary: {
            modelAccuracy: 94.2,
            averageConfidence: 87.5,
            falsePositiveRate: 3.2,
            falseNegativeRate: 2.6
          },
          charts: {
            accuracyTrends: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
              datasets: [{
                label: 'Model Accuracy (%)',
                data: [92, 93, 94, 93.5, 94.2, 94.2],
                borderColor: 'rgb(139, 92, 246)',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                tension: 0.4
              }]
            },
            confidenceDistribution: {
              labels: ['60-70%', '71-80%', '81-90%', '91-100%'],
              datasets: [{
                data: [8, 25, 45, 22],
                backgroundColor: [
                  'rgba(239, 68, 68, 0.8)',
                  'rgba(251, 191, 36, 0.8)',
                  'rgba(59, 130, 246, 0.8)',
                  'rgba(34, 197, 94, 0.8)'
                ]
              }]
            }
          }
        }
      };

      setReportData(mockData[selectedReport]);
      setIsLoading(false);
    }, 2000);
  };

  useEffect(() => {
    if (selectedReport) {
      generateReport();
    }
  }, [selectedReport, dateRange]);

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

  const exportReport = (format) => {
    // Simulate export functionality
    console.log(`Exporting ${selectedReport} report in ${format} format`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
          <p className="mt-2 text-gray-600">
            Generate and view comprehensive credit analysis reports
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={() => generateReport()}
            disabled={isLoading}
            className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {isLoading ? (
              <RefreshCw className="h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="h-4 w-4" />
            )}
            <span>{isLoading ? 'Generating...' : 'Refresh'}</span>
          </button>
          {reportData && (
            <div className="flex space-x-2">
              <button
                onClick={() => exportReport('pdf')}
                className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="h-4 w-4" />
                <span>Export PDF</span>
              </button>
              <button
                onClick={() => exportReport('excel')}
                className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="h-4 w-4" />
                <span>Export Excel</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Report Type Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {reportTypes.map((report) => {
          const Icon = report.icon;
          return (
            <button
              key={report.id}
              onClick={() => setSelectedReport(report.id)}
              className={`p-6 rounded-lg border-2 transition-all ${
                selectedReport === report.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-3">
                <div className={`${report.color} p-2 rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <div className="text-left">
                  <h3 className="font-semibold text-gray-900">{report.name}</h3>
                  <p className="text-sm text-gray-600">{report.description}</p>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Date Range Filter */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">Date Range:</label>
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="week">Last Week</option>
            <option value="month">Last Month</option>
            <option value="quarter">Last Quarter</option>
            <option value="year">Last Year</option>
          </select>
        </div>
      </div>

      {/* Report Content */}
      {isLoading ? (
        <div className="bg-white rounded-lg shadow-md p-12 border border-gray-200">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mr-4"></div>
            <span className="text-lg text-gray-600">Generating report...</span>
          </div>
        </div>
      ) : reportData ? (
        <div className="space-y-6">
          {/* Report Header */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{reportData.title}</h2>
                <p className="text-gray-600">Period: {reportData.period}</p>
              </div>
              <div className="flex space-x-2">
                <button className="flex items-center space-x-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors">
                  <Eye className="h-4 w-4" />
                  <span>Preview</span>
                </button>
                <button className="flex items-center space-x-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors">
                  <Printer className="h-4 w-4" />
                  <span>Print</span>
                </button>
              </div>
            </div>
          </div>

          {/* Summary Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(reportData.summary).map(([key, value]) => (
              <div key={key} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-sm font-medium text-gray-600 capitalize">
                  {key.replace(/([A-Z])/g, ' $1').trim()}
                </h3>
                <p className="text-2xl font-bold text-gray-900 mt-2">
                  {typeof value === 'number' && key.includes('Rate') ? `${value}%` : 
                   typeof value === 'number' && key.includes('Time') ? `${value} hours` :
                   typeof value === 'number' ? value.toLocaleString() : value}
                </p>
              </div>
            ))}
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(reportData.charts).map(([chartKey, chartData]) => (
              <div key={chartKey} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 capitalize">
                  {chartKey.replace(/([A-Z])/g, ' $1').trim()}
                </h3>
                <div className="h-64">
                  {chartKey.includes('Distribution') || chartKey.includes('ByRisk') || chartKey.includes('Distribution') ? (
                    <Doughnut data={chartData} options={chartOptions} />
                  ) : chartKey.includes('Factors') ? (
                    <Bar data={chartData} options={chartOptions} />
                  ) : (
                    <Line data={chartData} options={chartOptions} />
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Key Insights */}
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Insights</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                <p className="text-sm text-gray-700">
                  Overall performance shows positive trends with improving approval rates
                </p>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <p className="text-sm text-gray-700">
                  AI model accuracy remains consistently high at 94.2%
                </p>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                <p className="text-sm text-gray-700">
                  Medium-risk applications require additional review processes
                </p>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                <p className="text-sm text-gray-700">
                  Processing time has improved by 15% compared to last month
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 border border-gray-200">
          <div className="text-center">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Report Selected</h3>
            <p className="text-gray-600">
              Select a report type above to generate and view detailed analytics
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;
