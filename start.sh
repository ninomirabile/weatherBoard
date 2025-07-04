#!/bin/bash

# WeatherBoard - Start Script
# Usage: ./start.sh [mock|mqtt]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default mode
MODE=${1:-mock}

echo -e "${BLUE}🌤️  WeatherBoard - Starting in $MODE mode${NC}"
echo "=================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"

# Check if ports are available
echo -e "${YELLOW}🔌 Checking ports...${NC}"

if port_in_use 8000; then
    echo -e "${RED}❌ Port 8000 is already in use${NC}"
    exit 1
fi

if port_in_use 5173; then
    echo -e "${RED}❌ Port 5173 is already in use${NC}"
    exit 1
fi

if [ "$MODE" = "mqtt" ] && port_in_use 1883; then
    echo -e "${RED}❌ Port 1883 is already in use${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Ports available${NC}"

# Install dependencies if needed
echo -e "${YELLOW}📦 Installing dependencies...${NC}"

# Backend dependencies
if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "Python virtual environment exists"
fi

# Frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "Node.js dependencies exist"
fi

echo -e "${GREEN}✅ Dependencies OK${NC}"

# Start services based on mode
if [ "$MODE" = "mqtt" ]; then
    echo -e "${YELLOW}🚀 Starting in MQTT mode...${NC}"
    
    # Start MQTT broker
    echo "Starting MQTT broker..."
    docker run -d --name weatherboard-mqtt -p 1883:1883 eclipse-mosquitto:2.0
    
    # Start backend in MQTT mode
    echo "Starting backend (MQTT mode)..."
    cd backend
    source venv/bin/activate
    DATA_SOURCE=mqtt MQTT_BROKER_HOST=localhost MQTT_BROKER_PORT=1883 uvicorn app.main:app --reload --port 8000 --host 0.0.0.0 &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend
    echo "Starting frontend..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo -e "${GREEN}✅ WeatherBoard started in MQTT mode!${NC}"
    echo ""
    echo -e "${BLUE}📊 Services:${NC}"
    echo "  • Backend: http://localhost:8000"
    echo "  • Frontend: http://localhost:5173"
    echo "  • MQTT Broker: localhost:1883"
    echo ""
    echo -e "${YELLOW}💡 To publish MQTT data, use:${NC}"
    echo "  mosquitto_pub -h localhost -p 1883 -t /weather/milano -m '{\"city\":\"Milano\",\"temperature\":18.3,\"humidity\":65.5,\"wind_speed\":10.4,\"description\":\"Heavy Rain\",\"timestamp\":\"2024-07-03T11:34:00Z\"}'"
    echo ""
    echo -e "${YELLOW}🛑 To stop: Ctrl+C${NC}"
    
    # Wait for interrupt
    trap "echo -e '\n${YELLOW}🛑 Stopping services...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker stop weatherboard-mqtt 2>/dev/null; docker rm weatherboard-mqtt 2>/dev/null; echo -e '${GREEN}✅ Services stopped${NC}'; exit 0" INT
    
    wait
    
else
    echo -e "${YELLOW}🚀 Starting in MOCK mode...${NC}"
    
    # Start backend in mock mode
    echo "Starting backend (mock mode)..."
    cd backend
    source venv/bin/activate
    uvicorn app.main:app --reload --port 8000 --host 0.0.0.0 &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend
    echo "Starting frontend..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo -e "${GREEN}✅ WeatherBoard started in MOCK mode!${NC}"
    echo ""
    echo -e "${BLUE}📊 Services:${NC}"
    echo "  • Backend: http://localhost:8000"
    echo "  • Frontend: http://localhost:5173"
    echo ""
    echo -e "${YELLOW}🛑 To stop: Ctrl+C${NC}"
    
    # Wait for interrupt
    trap "echo -e '\n${YELLOW}🛑 Stopping services...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo -e '${GREEN}✅ Services stopped${NC}'; exit 0" INT
    
    wait
fi 