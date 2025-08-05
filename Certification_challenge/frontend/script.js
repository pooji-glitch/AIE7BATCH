// Tesla Investment Analysis AI Frontend JavaScript

class TeslaInvestmentAI {
    constructor() {
        this.apiUrl = 'http://localhost:8000';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Submit button
        const submitBtn = document.getElementById('submit-btn');
        submitBtn.addEventListener('click', () => this.handleSubmit());

        // Quick query buttons
        const quickQueryBtns = document.querySelectorAll('.quick-query');
        quickQueryBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleQuickQuery(e));
        });

        // Enter key in textarea
        const queryTextarea = document.getElementById('query');
        queryTextarea.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit();
            }
        });
    }

    handleQuickQuery(event) {
        const queries = {
            'Revenue Analysis': 'What was Tesla\'s revenue performance in Q4 2023 and how does it compare to previous quarters?',
            'Delivery Performance': 'How many vehicles did Tesla deliver in Q4 2023 and what are the delivery trends?',
            'Market Sentiment': 'What is the current market sentiment for Tesla and how has it changed recently?',
            'Competitor Analysis': 'Who are Tesla\'s main competitors and how do they compare in terms of market position?'
        };

        const queryText = event.target.textContent;
        const query = queries[queryText];
        
        if (query) {
            document.getElementById('query').value = query;
            this.handleSubmit();
        }
    }

    async handleSubmit() {
        const query = document.getElementById('query').value.trim();
        
        if (!query) {
            this.showError('Please enter a question to analyze.');
            return;
        }

        this.showLoading();
        this.showResults();

        try {
            const response = await this.callAPI(query);
            this.displayResults(response);
        } catch (error) {
            console.error('API Error:', error);
            this.showError('Failed to get analysis. Please try again.');
        }
    }

    async callAPI(query) {
        const response = await fetch(`${this.apiUrl}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: query
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('analysis-result').style.display = 'none';
        document.getElementById('context-sources').style.display = 'none';
        document.getElementById('metrics').style.display = 'none';
    }

    showResults() {
        document.getElementById('results').style.display = 'block';
        document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
    }

    displayResults(data) {
        // Hide loading
        document.getElementById('loading').style.display = 'none';

        // Display analysis result
        const responseContent = document.getElementById('response-content');
        responseContent.innerHTML = this.formatResponse(data.response || data.answer || 'No response available');

        // Display timestamp
        document.getElementById('timestamp').textContent = new Date().toLocaleString();

        // Display sources
        this.displaySources(data.context_sources || data.sources || []);

        // Display metrics
        this.displayMetrics(data.retrieval_evaluation || {});

        // Show all result sections
        document.getElementById('analysis-result').style.display = 'block';
        document.getElementById('context-sources').style.display = 'block';
        document.getElementById('metrics').style.display = 'block';
    }

    formatResponse(response) {
        if (typeof response === 'string') {
            // Convert markdown-like formatting to HTML
            return response
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n/g, '<br>')
                .replace(/^# (.*$)/gim, '<h3 class="text-lg font-semibold text-gray-800 mb-2">$1</h3>')
                .replace(/^## (.*$)/gim, '<h4 class="text-md font-semibold text-gray-700 mb-1">$1</h4>')
                .replace(/^- (.*$)/gim, '<li class="ml-4">$1</li>')
                .replace(/(\d+\. .*$)/gim, '<li class="ml-4">$1</li>');
        }
        return response;
    }

    displaySources(sources) {
        const sourcesContent = document.getElementById('sources-content');
        
        if (!sources || sources.length === 0) {
            sourcesContent.innerHTML = '<p class="text-gray-500 italic">No specific sources available</p>';
            return;
        }

        const sourcesHTML = sources.map((source, index) => `
            <div class="bg-gray-50 rounded-lg p-3">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h4 class="font-medium text-gray-800">Source ${index + 1}</h4>
                        <p class="text-sm text-gray-600 mt-1">${source.content || source.page_content || 'No content available'}</p>
                        <div class="flex items-center mt-2 space-x-4 text-xs text-gray-500">
                            <span><i class="fas fa-tag mr-1"></i>${source.metadata?.source || 'Unknown'}</span>
                            <span><i class="fas fa-calendar mr-1"></i>${source.metadata?.date || source.metadata?.quarter || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="ml-3">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            ${source.metadata?.type || 'Data'}
                        </span>
                    </div>
                </div>
            </div>
        `).join('');

        sourcesContent.innerHTML = sourcesHTML;
    }

    displayMetrics(metrics) {
        const metricsContent = document.getElementById('metrics-content');
        
        if (!metrics || Object.keys(metrics).length === 0) {
            metricsContent.innerHTML = '<p class="text-gray-500 italic col-span-3">No metrics available</p>';
            return;
        }

        const metricsHTML = Object.entries(metrics).map(([key, value]) => `
            <div class="bg-gray-50 rounded-lg p-4 text-center">
                <div class="text-2xl font-bold text-blue-600 mb-1">
                    ${typeof value === 'number' ? (value * 100).toFixed(1) + '%' : value}
                </div>
                <div class="text-sm font-medium text-gray-700 capitalize">
                    ${key.replace(/_/g, ' ')}
                </div>
            </div>
        `).join('');

        metricsContent.innerHTML = metricsHTML;
    }

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        errorDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                <span>${message}</span>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.teslaAI = new TeslaInvestmentAI();
    
    // Add some sample data for demo purposes
    console.log('Tesla Investment Analysis AI Frontend Loaded');
    
    // Check if backend is available
    fetch('http://localhost:8000/health')
        .then(response => {
            if (response.ok) {
                console.log('Backend is running');
            }
        })
        .catch(error => {
            console.warn('Backend not available:', error);
        });
}); 