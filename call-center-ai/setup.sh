#!/bin/bash
# Quick Setup Script for AI Call Center Army

set -e

echo "🚀 AI Call Center Army - Quick Setup"
echo "====================================="
echo ""

# Check Python version
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11+ required. Please install it first."
    exit 1
fi

echo "✅ Python 3.11+ found"

# Create virtual environment
if [ ! -d "venv_linux" ]; then
    echo "📦 Creating virtual environment..."
    python3.11 -m venv venv_linux
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv_linux/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo "   Required: ANTHROPIC_API_KEY, OPENAI_API_KEY"
    echo ""
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p /tmp/call-recordings
mkdir -p data/recordings

# Check Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker found"

    # Check if Docker is running
    if docker info &> /dev/null; then
        echo "✅ Docker is running"

        # Start infrastructure services
        read -p "🐳 Start Docker services (PostgreSQL, Redis, ChromaDB, LiveKit)? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🚀 Starting Docker services..."
            cd deployment
            docker-compose up -d postgres redis chromadb
            cd ..
            echo "✅ Infrastructure services started"
        fi
    else
        echo "⚠️  Docker is installed but not running. Start Docker and run this script again."
    fi
else
    echo "⚠️  Docker not found. Install Docker to run infrastructure services."
    echo "   Or use external/cloud services for PostgreSQL, Redis, and ChromaDB."
fi

echo ""
echo "=============================================="
echo "✅ Setup Complete!"
echo "=============================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Edit .env with your API keys:"
echo "   nano .env"
echo ""
echo "2. Start the dashboard:"
echo "   source venv_linux/bin/activate"
echo "   python -m web_interface.dashboard"
echo ""
echo "3. In another terminal, start voice agents:"
echo "   source venv_linux/bin/activate"
echo "   python -m livekit_integration.voice_agent"
echo ""
echo "4. Access dashboard:"
echo "   http://localhost:8080"
echo ""
echo "5. Deploy to Hostinger (optional):"
echo "   ./deployment/deploy_hostinger.sh"
echo ""
echo "📚 Read README.md for complete documentation"
echo ""
