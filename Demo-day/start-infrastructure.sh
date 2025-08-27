#!/bin/bash

echo "🚀 Starting AI Credit Assistant Infrastructure..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    if [ -f "env.example" ]; then
        cp env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env file with your configuration before continuing.${NC}"
        echo -e "${YELLOW}⚠️  Press Enter when ready to continue...${NC}"
        read
    else
        echo -e "${RED}❌ env.example file not found. Please create .env file manually.${NC}"
        exit 1
    fi
fi

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p nginx/ssl
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p logs

# Build and start services
echo -e "${BLUE}🐳 Building and starting Docker services...${NC}"
docker-compose build

echo -e "${BLUE}🚀 Starting all services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"
sleep 30

# Check service status
echo -e "${BLUE}📊 Checking service status...${NC}"
docker-compose ps

# Health checks
echo -e "${BLUE}🏥 Running health checks...${NC}"

# Check backend health
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API is healthy${NC}"
else
    echo -e "${RED}❌ Backend API health check failed${NC}"
fi

# Check frontend health
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
fi

# Check database health
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PostgreSQL is healthy${NC}"
else
    echo -e "${RED}❌ PostgreSQL health check failed${NC}"
fi

# Check Redis health
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis is healthy${NC}"
else
    echo -e "${RED}❌ Redis health check failed${NC}"
fi

# Display service URLs
echo -e "${BLUE}🌐 Service URLs:${NC}"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}Backend API:${NC} http://localhost:5000"
echo -e "${GREEN}API Documentation:${NC} http://localhost:5000/api/docs"
echo -e "${GREEN}Grafana Dashboard:${NC} http://localhost:3001 (admin/admin)"
echo -e "${GREEN}Prometheus:${NC} http://localhost:9090"
echo -e "${GREEN}Kibana:${NC} http://localhost:5601"

# Display useful commands
echo -e "${BLUE}🔧 Useful Commands:${NC}"
echo -e "${YELLOW}View logs:${NC} docker-compose logs -f"
echo -e "${YELLOW}Stop services:${NC} docker-compose down"
echo -e "${YELLOW}Restart services:${NC} docker-compose restart"
echo -e "${YELLOW}View service status:${NC} docker-compose ps"
echo -e "${YELLOW}Access database:${NC} docker-compose exec postgres psql -U postgres -d credit_assistant"

# Check for any errors
echo -e "${BLUE}🔍 Checking for any startup errors...${NC}"
ERRORS=$(docker-compose logs --tail=50 | grep -i "error\|failed\|exception" || true)

if [ -n "$ERRORS" ]; then
    echo -e "${RED}⚠️  Found potential errors in logs:${NC}"
    echo "$ERRORS"
    echo -e "${YELLOW}Check logs with: docker-compose logs${NC}"
else
    echo -e "${GREEN}✅ No obvious errors found in recent logs${NC}"
fi

echo -e "${GREEN}🎉 Infrastructure startup complete!${NC}"
echo -e "${BLUE}Your AI Credit Assistant is now running at:${NC}"
echo -e "${GREEN}🌐 http://localhost:3000${NC}"

# Optional: Open browser
read -p "Would you like to open the application in your browser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        open http://localhost:3000
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000
    else
        echo -e "${YELLOW}Please manually open: http://localhost:3000${NC}"
    fi
fi

echo -e "${BLUE}📝 Next steps:${NC}"
echo -e "1. Configure your OpenAI API key in the .env file"
echo -e "2. Set up SSL certificates for production"
echo -e "3. Configure monitoring alerts"
echo -e "4. Set up automated backups"
echo -e "5. Review security settings"

echo -e "${GREEN}🚀 Your AI Credit Assistant infrastructure is ready!${NC}"
