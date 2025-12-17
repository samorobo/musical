#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Music Playlist Generator Server${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python3 found${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Start the server
echo ""
echo -e "${GREEN}Starting Flask server...${NC}"
echo -e "${BLUE}Server will be available at: http://localhost:5000${NC}"
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Server Logs:${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Run Flask app and display logs
python app.py