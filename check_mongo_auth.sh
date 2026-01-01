#!/bin/bash

echo "=== Checking MongoDB Connection and Authentication ==="
echo ""

echo "1. Backend logs (MongoDB connection):"
sudo journalctl -u hackingpanel-backend -n 50 | grep -i -E "(mongo|database|connected|auth)" | tail -10
echo ""

echo "2. Testing authentication endpoint:"
echo "Testing login with credentials..."
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"Shresth","password":"hackur"}' \
  2>/dev/null | jq . 2>/dev/null || curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"Shresth","password":"hackur"}'
echo ""
echo ""

echo "3. Checking .env file:"
cat ~/h1x1/hackingpanel/.env
echo ""

echo "4. Verifying backend can read .env:"
cd ~/h1x1/hackingpanel
source .venv/bin/activate
python3 -c "
from app.config import settings
print(f'MongoDB URL: {settings.MONGODB_URL[:50]}...')
print(f'MongoDB DB: {settings.MONGODB_DB_NAME}')
print(f'Auth Username: {settings.AUTH_USERNAME}')
print(f'Auth Password: {\"*\" * len(settings.AUTH_PASSWORD) if settings.AUTH_PASSWORD else \"NOT SET\"}')
print(f'Server URL: {settings.SERVER_URL}')
"
echo ""

echo "5. Testing health endpoint:"
curl -s http://localhost:5000/api/health | jq . 2>/dev/null || curl -s http://localhost:5000/api/health
echo ""

