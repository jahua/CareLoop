#!/bin/bash

# NextChat-Enhanced Development Setup Script

echo "🚀 NextChat-Enhanced Development Setup"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Make sure you're in the nextchat-personality-enhanced directory."
    exit 1
fi

echo "📦 Installing dependencies..."
if command -v yarn &> /dev/null; then
    echo "Using Yarn..."
    yarn install
elif command -v npm &> /dev/null; then
    echo "Using NPM..."
    npm install
else
    echo "❌ Error: Neither yarn nor npm found. Please install Node.js and npm/yarn."
    exit 1
fi

# Check if Phase 1 API is running
echo "🔍 Checking Phase 1 API connection..."
if curl -s -f "http://localhost:3001/api/health" > /dev/null; then
    echo "✅ Phase 1 API is running on port 3001"
else
    echo "⚠️  Warning: Phase 1 API not detected on port 3001"
    echo "   Make sure to start the Phase 1 backend first:"
    echo "   cd ../Phase-1 && docker-compose up -d"
fi

# Check if N8N is running
echo "🔍 Checking N8N connection..."
if curl -s -f "http://localhost:5678" > /dev/null; then
    echo "✅ N8N is running on port 5678"
else
    echo "⚠️  Warning: N8N not detected on port 5678"
fi

echo ""
echo "🎯 Setup Complete!"
echo "==================="
echo ""
echo "To start development:"
echo "  yarn dev         # Start development server"
echo "  yarn build       # Build for production"
echo "  yarn start       # Start production server"
echo ""
echo "URLs:"
echo "  Frontend:        http://localhost:3000"
echo "  Phase 1 API:     http://localhost:3001"
echo "  N8N:             http://localhost:5678"
echo ""
echo "Features enabled:"
echo "  🧠 Personality Detection with EMA Smoothing"
echo "  🤖 Multi-Agent System Monitoring"
echo "  ✅ Quality Verification Pipeline"
echo "  📊 Real-time Analytics Dashboard"
echo ""

















































