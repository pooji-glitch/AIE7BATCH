#!/bin/bash

echo "🚀 Starting AI Credit Risk Analyzer Frontend..."

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating environment file..."
    cat > .env << EOF
# Frontend Environment Variables
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0

# Optional: Analytics and monitoring
REACT_APP_ANALYTICS_ID=
REACT_APP_SENTRY_DSN=

# Feature flags
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_MONITORING=false
EOF
fi

echo "✅ Frontend is ready!"
echo "🌐 Opening http://localhost:3000 in your browser..."
echo "📱 The application is fully responsive and works on all devices"
echo ""
echo "🎯 Available features:"
echo "   • Dashboard with real-time analytics"
echo "   • Credit Analysis with AI-powered assessment"
echo "   • Data Viewer with advanced filtering"
echo "   • Comprehensive Reports with export options"
echo ""
echo "🛑 To stop the server, press Ctrl+C"

# Start the development server
npm start
