import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  Download, 
  Eye, 
  Edit, 
  Trash2,
  ChevronDown,
  ChevronUp,
  SortAsc,
  SortDesc
} from 'lucide-react';

const DataViewer = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilters, setSelectedFilters] = useState({
    riskLevel: 'all',
    status: 'all',
    dateRange: 'all'
  });
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [expandedRows, setExpandedRows] = useState(new Set());
  const [isLoading, setIsLoading] = useState(true);

  // Mock data - replace with actual API calls
  const mockData = [
    {
      id: 1,
      applicantName: 'John Doe',
      email: 'john.doe@email.com',
      phone: '(555) 123-4567',
      creditScore: 745,
      riskLevel: 'Low',
      status: 'Approved',
      applicationDate: '2024-01-15',
      annualIncome: 75000,
      employmentLength: 5,
      creditUtilization: 25,
      latePayments: 0,
      aiConfidence: 92,
      details: {
        address: '123 Main St, City, State 12345',
        employer: 'Tech Corp Inc.',
        loanAmount: 25000,
        loanPurpose: 'Home Improvement',
        coApplicant: 'Jane Doe',
        documents: ['W2 Form', 'Bank Statements', 'Credit Report']
      }
    },
    {
      id: 2,
      applicantName: 'Jane Smith',
      email: 'jane.smith@email.com',
      phone: '(555) 987-6543',
      creditScore: 680,
      riskLevel: 'Medium',
      status: 'Under Review',
      applicationDate: '2024-01-14',
      annualIncome: 55000,
      employmentLength: 3,
      creditUtilization: 45,
      latePayments: 2,
      aiConfidence: 78,
      details: {
        address: '456 Oak Ave, City, State 12345',
        employer: 'Retail Solutions LLC',
        loanAmount: 15000,
        loanPurpose: 'Debt Consolidation',
        coApplicant: null,
        documents: ['Pay Stubs', 'Credit Report']
      }
    },
    {
      id: 3,
      applicantName: 'Mike Johnson',
      email: 'mike.johnson@email.com',
      phone: '(555) 456-7890',
      creditScore: 620,
      riskLevel: 'High',
      status: 'Rejected',
      applicationDate: '2024-01-13',
      annualIncome: 45000,
      employmentLength: 1,
      creditUtilization: 75,
      latePayments: 5,
      aiConfidence: 85,
      details: {
        address: '789 Pine Rd, City, State 12345',
        employer: 'Startup Ventures',
        loanAmount: 30000,
        loanPurpose: 'Business Expansion',
        coApplicant: null,
        documents: ['Business Plan', 'Financial Statements']
      }
    },
    {
      id: 4,
      applicantName: 'Sarah Wilson',
      email: 'sarah.wilson@email.com',
      phone: '(555) 321-0987',
      creditScore: 780,
      riskLevel: 'Low',
      status: 'Approved',
      applicationDate: '2024-01-12',
      annualIncome: 85000,
      employmentLength: 8,
      creditUtilization: 15,
      latePayments: 0,
      aiConfidence: 95,
      details: {
        address: '321 Elm St, City, State 12345',
        employer: 'Healthcare Systems',
        loanAmount: 40000,
        loanPurpose: 'Medical Equipment',
        coApplicant: 'Dr. Robert Wilson',
        documents: ['Medical License', 'Practice Financials']
      }
    },
    {
      id: 5,
      applicantName: 'David Brown',
      email: 'david.brown@email.com',
      phone: '(555) 654-3210',
      creditScore: 710,
      riskLevel: 'Medium',
      status: 'Pending',
      applicationDate: '2024-01-11',
      annualIncome: 65000,
      employmentLength: 4,
      creditUtilization: 35,
      latePayments: 1,
      aiConfidence: 82,
      details: {
        address: '654 Maple Dr, City, State 12345',
        employer: 'Construction Co.',
        loanAmount: 20000,
        loanPurpose: 'Vehicle Purchase',
        coApplicant: null,
        documents: ['Driver License', 'Vehicle Quote']
      }
    }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setData(mockData);
      setFilteredData(mockData);
      setIsLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    let filtered = data;

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.applicantName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.phone.includes(searchTerm)
      );
    }

    // Apply dropdown filters
    if (selectedFilters.riskLevel !== 'all') {
      filtered = filtered.filter(item => item.riskLevel === selectedFilters.riskLevel);
    }
    if (selectedFilters.status !== 'all') {
      filtered = filtered.filter(item => item.status === selectedFilters.status);
    }

    setFilteredData(filtered);
  }, [data, searchTerm, selectedFilters]);

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });

    const sorted = [...filteredData].sort((a, b) => {
      if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
      if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
      return 0;
    });
    setFilteredData(sorted);
  };

  const toggleRowExpansion = (id) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedRows(newExpanded);
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'Low': return 'text-green-600 bg-green-100';
      case 'Medium': return 'text-yellow-600 bg-yellow-100';
      case 'High': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Approved': return 'text-green-600 bg-green-100';
      case 'Rejected': return 'text-red-600 bg-red-100';
      case 'Under Review': return 'text-yellow-600 bg-yellow-100';
      case 'Pending': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const SortIcon = ({ columnKey }) => {
    if (sortConfig.key !== columnKey) {
      return <SortAsc className="h-4 w-4 text-gray-400" />;
    }
    return sortConfig.direction === 'asc' ? 
      <SortAsc className="h-4 w-4 text-blue-600" /> : 
      <SortDesc className="h-4 w-4 text-blue-600" />;
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
          <h1 className="text-3xl font-bold text-gray-900">Data Viewer</h1>
          <p className="mt-2 text-gray-600">
            View and manage credit application data
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
            <Download className="h-4 w-4" />
            <span>Export Data</span>
          </button>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search applications..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Risk Level Filter */}
          <select
            value={selectedFilters.riskLevel}
            onChange={(e) => setSelectedFilters({...selectedFilters, riskLevel: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Risk Levels</option>
            <option value="Low">Low Risk</option>
            <option value="Medium">Medium Risk</option>
            <option value="High">High Risk</option>
          </select>

          {/* Status Filter */}
          <select
            value={selectedFilters.status}
            onChange={(e) => setSelectedFilters({...selectedFilters, status: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Statuses</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
            <option value="Under Review">Under Review</option>
            <option value="Pending">Pending</option>
          </select>

          {/* Date Range Filter */}
          <select
            value={selectedFilters.dateRange}
            onChange={(e) => setSelectedFilters({...selectedFilters, dateRange: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Dates</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort('applicantName')}
                    className="flex items-center space-x-1 hover:text-gray-700"
                  >
                    <span>Applicant</span>
                    <SortIcon columnKey="applicantName" />
                  </button>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort('creditScore')}
                    className="flex items-center space-x-1 hover:text-gray-700"
                  >
                    <span>Credit Score</span>
                    <SortIcon columnKey="creditScore" />
                  </button>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk Level
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort('applicationDate')}
                    className="flex items-center space-x-1 hover:text-gray-700"
                  >
                    <span>Application Date</span>
                    <SortIcon columnKey="applicationDate" />
                  </button>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  AI Confidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredData.map((item) => (
                <React.Fragment key={item.id}>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <span className="text-sm font-medium text-blue-600">
                              {item.applicantName.split(' ').map(n => n[0]).join('')}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{item.applicantName}</div>
                          <div className="text-sm text-gray-500">{item.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{item.creditScore}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRiskColor(item.riskLevel)}`}>
                        {item.riskLevel}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(item.status)}`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(item.applicationDate).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${item.aiConfidence}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-900">{item.aiConfidence}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => toggleRowExpansion(item.id)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          {expandedRows.has(item.id) ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                        </button>
                        <button className="text-green-600 hover:text-green-900">
                          <Eye className="h-4 w-4" />
                        </button>
                        <button className="text-blue-600 hover:text-blue-900">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button className="text-red-600 hover:text-red-900">
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                  {expandedRows.has(item.id) && (
                    <tr>
                      <td colSpan="7" className="px-6 py-4 bg-gray-50">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          <div>
                            <h4 className="font-medium text-gray-900 mb-2">Contact Information</h4>
                            <p className="text-sm text-gray-600">Phone: {item.phone}</p>
                            <p className="text-sm text-gray-600">Address: {item.details.address}</p>
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-900 mb-2">Financial Details</h4>
                            <p className="text-sm text-gray-600">Annual Income: ${item.annualIncome.toLocaleString()}</p>
                            <p className="text-sm text-gray-600">Employment: {item.employmentLength} years</p>
                            <p className="text-sm text-gray-600">Credit Utilization: {item.creditUtilization}%</p>
                            <p className="text-sm text-gray-600">Late Payments: {item.latePayments}</p>
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-900 mb-2">Loan Information</h4>
                            <p className="text-sm text-gray-600">Amount: ${item.details.loanAmount.toLocaleString()}</p>
                            <p className="text-sm text-gray-600">Purpose: {item.details.loanPurpose}</p>
                            <p className="text-sm text-gray-600">Employer: {item.details.employer}</p>
                            {item.details.coApplicant && (
                              <p className="text-sm text-gray-600">Co-Applicant: {item.details.coApplicant}</p>
                            )}
                          </div>
                        </div>
                        <div className="mt-4">
                          <h4 className="font-medium text-gray-900 mb-2">Documents</h4>
                          <div className="flex flex-wrap gap-2">
                            {item.details.documents.map((doc, index) => (
                              <span key={index} className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                {doc}
                              </span>
                            ))}
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      <div className="bg-white rounded-lg shadow-md px-6 py-4 border border-gray-200">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing <span className="font-medium">1</span> to <span className="font-medium">{filteredData.length}</span> of{' '}
            <span className="font-medium">{data.length}</span> results
          </div>
          <div className="flex space-x-2">
            <button className="px-3 py-1 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-50">
              Previous
            </button>
            <button className="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">
              1
            </button>
            <button className="px-3 py-1 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-50">
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataViewer;
