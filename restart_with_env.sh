#!/bin/bash

echo "=== Stopping All Servers ==="

# Stop systemd services
echo "1. Stopping systemd services..."
sudo systemctl stop hackingpanel-backend 2>/dev/null
sudo systemctl stop hackingpanel-frontend 2>/dev/null
sudo systemctl stop nginx 2>/dev/null
sleep 2

# Kill any remaining processes
echo "2. Killing any remaining processes..."
pkill -f "python.*run.py" 2>/dev/null
pkill -f "vite.*--host.*0.0.0.0" 2>/dev/null
pkill -f "node.*vite" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
sleep 2

# Verify nothing is running on ports 5000, 3000, 80
echo "3. Checking ports..."
PORTS_IN_USE=$(netstat -tulpn 2>/dev/null | grep -E ":(5000|3000|80)" || ss -tulpn 2>/dev/null | grep -E ":(5000|3000|80)")
if [ -n "$PORTS_IN_USE" ]; then
    echo "Warning: Some ports are still in use:"
    echo "$PORTS_IN_USE"
    echo "Force killing processes on these ports..."
    # Get PIDs from ports and kill them
    lsof -ti:5000 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    lsof -ti:80 | xargs kill -9 2>/dev/null
    sleep 2
else
    echo "✓ All ports are free"
fi

echo ""
echo "=== Updating .env File ==="
cd ~/h1x1/hackingpanel

cat > .env <<'EOF'
MONGODB_URL=mongodb+srv://KaushikShresth:Shresth123&@cluster0.awof7.mongodb.net/
MONGODB_DB_NAME=HackingPanel
Serverurl = http://93.127.195.74:5000/
Username = Shresth
Password = hackur
EOF

echo "✓ .env file updated!"
echo ""
echo "Current .env contents:"
cat .env
echo ""

echo "=== Starting All Servers ==="

# Start backend
echo "1. Starting backend service..."
sudo systemctl start hackingpanel-backend
sleep 3

# Start frontend
echo "2. Starting frontend service..."
sudo systemctl start hackingpanel-frontend
sleep 3

# Start nginx
echo "3. Starting nginx..."
sudo systemctl start nginx
sleep 2

echo ""
echo "=== Service Status ==="
echo "Backend:"
sudo systemctl is-active hackingpanel-backend && echo "✓ Active" || echo "✗ Failed"
echo "Frontend:"
sudo systemctl is-active hackingpanel-frontend && echo "✓ Active" || echo "✗ Failed"
echo "Nginx:"
sudo systemctl is-active nginx && echo "✓ Active" || echo "✗ Failed"

echo ""
echo "=== Checking MongoDB Connection ==="
sleep 2
sudo journalctl -u hackingpanel-backend -n 20 | grep -i mongo || echo "Check logs manually: sudo journalctl -u hackingpanel-backend -n 50"

echo ""
echo "=== Testing Connections ==="
sleep 2
echo "Backend health:"
curl -s http://localhost:5000/api/health && echo " ✓" || echo " ✗"
echo "Backend via nginx:"
curl -s http://localhost/api/health && echo " ✓" || echo " ✗"
echo "Frontend via nginx:"
curl -s http://localhost > /dev/null && echo "✓ Frontend responding" || echo "✗ Frontend not responding"

echo ""
echo "=== Done ==="
echo "Access your application at: http://93.127.195.74"
echo ""
echo "Check logs:"
echo "  Backend:  sudo journalctl -u hackingpanel-backend -f"
echo "  Frontend: sudo journalctl -u hackingpanel-frontend -f"

