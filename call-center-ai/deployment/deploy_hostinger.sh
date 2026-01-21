#!/bin/bash
set -e

# Hostinger VPS Deployment Script for AI Call Center Army
# Usage: ./deploy_hostinger.sh

echo "🚀 AI Call Center Army - Hostinger Deployment"
echo "=============================================="

# Load environment variables
if [ -f ../.env ]; then
    source ../.env
else
    echo "❌ Error: .env file not found!"
    exit 1
fi

# Check required variables
if [ -z "$HOSTINGER_SSH_HOST" ] || [ -z "$HOSTINGER_SSH_USER" ]; then
    echo "❌ Error: HOSTINGER_SSH_HOST and HOSTINGER_SSH_USER must be set in .env"
    exit 1
fi

SSH_HOST=$HOSTINGER_SSH_HOST
SSH_USER=$HOSTINGER_SSH_USER
APP_DIR="/var/www/callcenter"

echo "📡 Deploying to: $SSH_USER@$SSH_HOST"
echo ""

# 1. Create remote directory
echo "📁 Setting up remote directory..."
ssh $SSH_USER@$SSH_HOST "mkdir -p $APP_DIR"

# 2. Copy project files
echo "📤 Uploading project files..."
rsync -avz --exclude='venv_linux' \
           --exclude='.git' \
           --exclude='__pycache__' \
           --exclude='*.pyc' \
           --exclude='.env' \
           ../ $SSH_USER@$SSH_HOST:$APP_DIR/

# 3. Copy .env file
echo "🔐 Uploading environment configuration..."
scp ../.env $SSH_USER@$SSH_HOST:$APP_DIR/.env

# 4. Install dependencies on remote
echo "📦 Installing dependencies on remote server..."
ssh $SSH_USER@$SSH_HOST << 'ENDSSH'
cd /var/www/callcenter

# Install Python 3.11 if needed
if ! command -v python3.11 &> /dev/null; then
    echo "Installing Python 3.11..."
    apt update
    apt install -y python3.11 python3.11-venv python3.11-dev
fi

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi
ENDSSH

# 5. Start services
echo "🐳 Starting Docker containers..."
ssh $SSH_USER@$SSH_HOST << 'ENDSSH'
cd /var/www/callcenter/deployment
docker-compose down
docker-compose up -d --build
docker-compose ps
ENDSSH

# 6. Configure Nginx (if not already configured)
echo "⚙️  Configuring Nginx..."
ssh $SSH_USER@$SSH_HOST << 'ENDSSH'
if [ ! -f /etc/nginx/sites-available/callcenter ]; then
    cat > /etc/nginx/sites-available/callcenter << 'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /livekit {
        proxy_pass http://localhost:7880;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
NGINX

    ln -s /etc/nginx/sites-available/callcenter /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
fi
ENDSSH

# 7. Health check
echo ""
echo "🏥 Performing health check..."
sleep 10

HEALTH_CHECK=$(ssh $SSH_USER@$SSH_HOST "curl -f http://localhost:8080/health 2>/dev/null || echo 'FAILED'")

if [ "$HEALTH_CHECK" == "FAILED" ]; then
    echo "⚠️  Warning: Health check failed. Check logs with:"
    echo "   ssh $SSH_USER@$SSH_HOST 'cd $APP_DIR/deployment && docker-compose logs'"
else
    echo "✅ Health check passed!"
fi

# 8. Show status
echo ""
echo "=============================================="
echo "✅ Deployment Complete!"
echo "=============================================="
echo ""
echo "📊 Dashboard: http://$SSH_HOST"
echo "📞 LiveKit: ws://$SSH_HOST:7880"
echo ""
echo "Useful commands:"
echo "  View logs:    ssh $SSH_USER@$SSH_HOST 'cd $APP_DIR/deployment && docker-compose logs -f'"
echo "  Restart:      ssh $SSH_USER@$SSH_HOST 'cd $APP_DIR/deployment && docker-compose restart'"
echo "  Stop:         ssh $SSH_USER@$SSH_HOST 'cd $APP_DIR/deployment && docker-compose down'"
echo ""
