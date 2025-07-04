#!/bin/bash

# WeatherBoard - Stop Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 WeatherBoard - Stopping all services${NC}"
echo "=================================="

# Stop backend processes
echo -e "${YELLOW}🔄 Stopping backend...${NC}"
pkill -f "uvicorn app.main:app" 2>/dev/null || echo "No backend process found"

# Stop frontend processes
echo -e "${YELLOW}🔄 Stopping frontend...${NC}"
pkill -f "vite" 2>/dev/null || echo "No frontend process found"

# Stop MQTT broker container
echo -e "${YELLOW}🔄 Stopping MQTT broker...${NC}"
docker stop weatherboard-mqtt 2>/dev/null || echo "No MQTT container found"
docker rm weatherboard-mqtt 2>/dev/null || echo "No MQTT container to remove"

# Stop any other related processes
echo -e "${YELLOW}🔄 Cleaning up...${NC}"
pkill -f "weatherboard" 2>/dev/null || echo "No weatherboard processes found"

echo -e "${GREEN}✅ All WeatherBoard services stopped${NC}"
echo ""
echo -e "${BLUE}📊 Services stopped:${NC}"
echo "  • Backend (port 8000)"
echo "  • Frontend (port 5173)"
echo "  • MQTT Broker (port 1883)" 