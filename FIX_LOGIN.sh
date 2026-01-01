#!/bin/bash

echo "=== Fixing Login Issue Completely ==="

# Stash any git changes
cd ~/h1x1/hackingpanel
git stash
git pull

# Fix frontend .env
echo "1. Updating frontend .env..."
cd frontend
cat > .env <<'EOF'
VITE_API_URL=http://93.127.195.74
EOF
echo "✓ Frontend .env updated:"
cat .env
cd ..

# Verify nginx config
echo ""
echo "2. Checking nginx configuration..."
if grep -q "location /api" /etc/nginx/sites-available/hackingpanel; then
    echo "✓ Nginx /api proxy configured"
else
    echo "✗ Nginx /api proxy missing - fixing..."
    sudo ./setup_nginx.sh
fi

# Restart everything
echo ""
echo "3. Restarting all services..."
sudo systemctl restart hackingpanel-backend
sleep 2
sudo systemctl restart hackingpanel-frontend
sleep 3
sudo systemctl restart nginx
sleep 2

# Test API endpoint
echo ""
echo "4. Testing API endpoint..."
API_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/health)
if [ "$API_TEST" = "200" ]; then
    echo "✓ API accessible via nginx: http://localhost/api/health"
else
    echo "✗ API not accessible via nginx (HTTP $API_TEST)"
fi

# Test login endpoint
echo ""
echo "5. Testing login endpoint..."
LOGIN_TEST=$(curl -s -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"Shresth","password":"hackur"}' | grep -o '"token"' | head -1)
if [ "$LOGIN_TEST" = '"token"' ]; then
    echo "✓ Login endpoint working!"
else
    echo "✗ Login endpoint not working"
    echo "Response:"
    curl -s -X POST http://localhost/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"username":"Shresth","password":"hackur"}'
fi

echo ""
echo "=== Status ==="
echo "Backend: $(systemctl is-active hackingpanel-backend)"
echo "Frontend: $(systemctl is-active hackingpanel-frontend)"
echo "Nginx: $(systemctl is-active nginx)"
echo ""
echo "Frontend .env:"
cat frontend/.env
echo ""
echo "=== Next Steps ==="
echo "1. Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)"
echo "2. Open browser console (F12) and check Network tab"
echo "3. Try logging in and check what URL is being called"
echo ""
echo "Expected API call: POST http://93.127.195.74/api/auth/login"

