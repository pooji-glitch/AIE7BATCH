import axios from 'axios';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Credit Analysis API functions
export const creditAnalysisAPI = {
  // Analyze credit risk
  analyzeCredit: async (data) => {
    try {
      const response = await api.post('/credit-analysis', data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to analyze credit');
    }
  },

  // Get analysis history
  getAnalysisHistory: async (params = {}) => {
    try {
      const response = await api.get('/credit-analysis/history', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch analysis history');
    }
  },

  // Get analysis by ID
  getAnalysisById: async (id) => {
    try {
      const response = await api.get(`/credit-analysis/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch analysis');
    }
  },
};

// Dashboard API functions
export const dashboardAPI = {
  // Get dashboard statistics
  getStats: async () => {
    try {
      const response = await api.get('/dashboard/stats');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch dashboard stats');
    }
  },

  // Get recent activity
  getRecentActivity: async (limit = 10) => {
    try {
      const response = await api.get('/dashboard/activity', { params: { limit } });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch recent activity');
    }
  },

  // Get chart data
  getChartData: async (chartType, dateRange) => {
    try {
      const response = await api.get('/dashboard/charts', { 
        params: { type: chartType, range: dateRange } 
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch chart data');
    }
  },
};

// Data Management API functions
export const dataAPI = {
  // Get applications data
  getApplications: async (params = {}) => {
    try {
      const response = await api.get('/applications', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch applications');
    }
  },

  // Get application by ID
  getApplicationById: async (id) => {
    try {
      const response = await api.get(`/applications/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch application');
    }
  },

  // Update application
  updateApplication: async (id, data) => {
    try {
      const response = await api.put(`/applications/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update application');
    }
  },

  // Delete application
  deleteApplication: async (id) => {
    try {
      const response = await api.delete(`/applications/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to delete application');
    }
  },

  // Export data
  exportData: async (format, filters = {}) => {
    try {
      const response = await api.get('/applications/export', { 
        params: { format, ...filters },
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to export data');
    }
  },
};

// Reports API functions
export const reportsAPI = {
  // Generate report
  generateReport: async (reportType, params = {}) => {
    try {
      const response = await api.post('/reports/generate', { 
        type: reportType, 
        params 
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to generate report');
    }
  },

  // Get report by ID
  getReportById: async (id) => {
    try {
      const response = await api.get(`/reports/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch report');
    }
  },

  // Get available report types
  getReportTypes: async () => {
    try {
      const response = await api.get('/reports/types');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch report types');
    }
  },

  // Export report
  exportReport: async (id, format) => {
    try {
      const response = await api.get(`/reports/${id}/export`, { 
        params: { format },
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to export report');
    }
  },
};

// Market Data API functions
export const marketDataAPI = {
  // Get market data
  getMarketData: async (params = {}) => {
    try {
      const response = await api.get('/market-data', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch market data');
    }
  },

  // Get financial news
  getFinancialNews: async (limit = 10) => {
    try {
      const response = await api.get('/market-data/news', { params: { limit } });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch financial news');
    }
  },
};

// AI Model API functions
export const aiModelAPI = {
  // Get model performance metrics
  getModelMetrics: async () => {
    try {
      const response = await api.get('/ai-model/metrics');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch model metrics');
    }
  },

  // Retrain model
  retrainModel: async () => {
    try {
      const response = await api.post('/ai-model/retrain');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to retrain model');
    }
  },

  // Get model status
  getModelStatus: async () => {
    try {
      const response = await api.get('/ai-model/status');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch model status');
    }
  },
};

// Utility functions
export const apiUtils = {
  // Download file from blob
  downloadFile: (blob, filename) => {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },

  // Handle API errors
  handleError: (error) => {
    console.error('API Error:', error);
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
    return error.message || 'An unexpected error occurred';
  },

  // Format date for API
  formatDate: (date) => {
    return new Date(date).toISOString().split('T')[0];
  },

  // Build query string
  buildQueryString: (params) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        searchParams.append(key, value);
      }
    });
    return searchParams.toString();
  },
};

export default api;
