#!/bin/bash

# Tesla Investment Tracker - Startup Script

echo "🚀 Starting Tesla Investment Tracker..."

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Start Jupyter notebook
echo "📊 Starting Jupyter notebook..."
echo "🌐 Open your browser to the URL shown below"
echo "📝 Make sure to select the 'Tesla Investment Tracker' kernel"
echo ""

jupyter notebook 