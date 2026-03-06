#!/bin/bash

# Test script for N8N Personality AI MVP Setup
echo "🧪 Testing N8N Personality AI MVP Setup"
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from env.example..."
    cp env.example .env
    echo "📝 Please edit .env file and add your OpenAI API key"
fi

# Check required environment variables
source .env 2>/dev/null || echo "⚠️  Could not load .env file"

if [ -z "$JUGUANG_API_KEY" ] || [ "$JUGUANG_API_KEY" = "your_juguang_api_key_here" ]; then
    echo "⚠️  JUGUANG_API_KEY not set in .env file"
    echo "   Please add your Juguang API key to continue"
fi

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check service health
echo ""
echo "🏥 Checking service health..."

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U n8n_user -d n8n_personality_ai > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "❌ PostgreSQL is not ready yet (may take up to 60 seconds)"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis is not ready"
fi

# Check N8N
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5678 | grep -q "200\|401"; then
    echo "✅ N8N is ready at http://localhost:5678"
    echo "   Login: admin / admin123"
else
    echo "❌ N8N is not ready yet (may take up to 2 minutes)"
fi

# Check Frontend
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ Frontend is ready at http://localhost:3000"
else
    echo "❌ Frontend is not ready yet"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Test Juguang API: python3 test_juguang_api.py"  
echo "2. Open N8N at http://localhost:5678 (admin/admin123)"
echo "3. Import workflows/personality-chat-workflow.json"
echo "4. Configure PostgreSQL credentials in N8N"
echo "5. Activate the workflow"
echo "6. Open chat interface at http://localhost:3000"
echo ""
echo "📚 For detailed setup instructions, see README.md"

# Show service status
echo ""
echo "📊 Service Status:"
docker-compose ps
