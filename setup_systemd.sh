#!/bin/bash

# Setup systemd services for Hacking Panel
# This script will install and start both backend and frontend as systemd services

echo "=== Setting up Hacking Panel systemd services ==="

# Get the project directory
PROJECT_DIR="/root/h1x1/hackingpanel"
FRONTEND_DIR="/root/h1x1/hackingpanel/frontend"

# Check if directories exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory not found at $PROJECT_DIR"
    exit 1
fi

# Create frontend .env if it doesn't exist
if [ ! -f "$FRONTEND_DIR/.env" ]; then
    echo "Creating frontend .env file..."
    cat > "$FRONTEND_DIR/.env" <<'EOF'
VITE_API_URL=http://93.127.195.74:5000
EOF
fi

# Copy service files to systemd directory
echo "Installing systemd service files..."
cp "$PROJECT_DIR/hackingpanel-backend.service" /etc/systemd/system/
cp "$PROJECT_DIR/hackingpanel-frontend.service" /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable services to start on boot
echo "Enabling services to start on boot..."
systemctl enable hackingpanel-backend.service
systemctl enable hackingpanel-frontend.service

# Stop any existing instances
echo "Stopping any existing instances..."
systemctl stop hackingpanel-backend.service 2>/dev/null
systemctl stop hackingpanel-frontend.service 2>/dev/null

# Kill any existing processes
pkill -f "python.*run.py" 2>/dev/null
pkill -f "vite.*--host.*0.0.0.0" 2>/dev/null
sleep 2

# Start services
echo "Starting services..."
systemctl start hackingpanel-backend.service
systemctl start hackingpanel-frontend.service

# Wait a moment for services to start
sleep 3

# Check status
echo ""
echo "=== Service Status ==="
systemctl status hackingpanel-backend.service --no-pager -l
echo ""
systemctl status hackingpanel-frontend.service --no-pager -l

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Services are now running and will start automatically on boot."
echo ""
echo "Useful commands:"
echo "  Check backend status:  systemctl status hackingpanel-backend"
echo "  Check frontend status: systemctl status hackingpanel-frontend"
echo "  View backend logs:     journalctl -u hackingpanel-backend -f"
echo "  View frontend logs:    journalctl -u hackingpanel-frontend -f"
echo "  Restart backend:       systemctl restart hackingpanel-backend"
echo "  Restart frontend:      systemctl restart hackingpanel-frontend"
echo "  Stop backend:          systemctl stop hackingpanel-backend"
echo "  Stop frontend:         systemctl stop hackingpanel-frontend"
echo ""
echo "Backend:  http://93.127.195.74:5000"
echo "Frontend: http://93.127.195.74:3000"

