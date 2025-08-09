#!/bin/bash
# Project Setup Script for PROG8850 Final Assignment
# This script sets up the complete database automation environment

echo "========================================"
echo "PROG8850 Database Automation Setup"
echo "========================================"

# Check prerequisites
echo "Checking prerequisites..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ All prerequisites are installed."

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install mysql-connector-python

# Set up directories
echo "Setting up directory structure..."
mkdir -p monitoring/signoz-data
mkdir -p monitoring/mysql-data
mkdir -p logs

# Set permissions
chmod +x scripts/multi_thread_queries.py

echo "✅ Project setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Start the monitoring stack: docker-compose -f monitoring/docker-compose-signoz.yml up -d"
echo "2. Wait for services to start (2-3 minutes)"
echo "3. Run the CI/CD pipeline: .github/workflows/ci_cd_pipeline.yml"
echo "4. Access SigNoz dashboard: http://localhost:3301"
echo "5. Connect to MySQL: mysql -h 127.0.0.1 -u root -p (password: Secret5555)"
echo ""
echo "For GitHub Actions testing locally, use 'act' tool:"
echo "- Install act: https://github.com/nektos/act"
echo "- Run: act -j database-deployment"
echo ""
echo "========================================"
