#!/bin/bash

echo "=== Testing Login Endpoint Directly ==="
echo ""

echo "1. Testing from VPS localhost:"
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"Shresth","password":"hackur"}' \
  -v 2>&1 | grep -E "(< HTTP|token|detail|error)"
echo ""

echo "2. Testing through nginx:"
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"Shresth","password":"hackur"}' \
  -v 2>&1 | grep -E "(< HTTP|token|detail|error)"
echo ""

echo "3. Testing with OPTIONS (CORS preflight):"
curl -X OPTIONS http://localhost/api/auth/login \
  -H "Origin: http://93.127.195.74" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  -v 2>&1 | grep -E "(< HTTP|Access-Control)"
echo ""

echo "4. Checking backend logs for login attempts:"
sudo journalctl -u hackingpanel-backend -n 30 | grep -i login
echo ""

echo "5. Checking nginx access logs:"
sudo tail -10 /var/log/nginx/access.log | grep auth
echo ""

