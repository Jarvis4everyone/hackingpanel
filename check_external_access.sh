#!/bin/bash

echo "=== Checking External Access Issues ==="
echo ""

echo "1. Checking if servers are listening on all interfaces:"
netstat -tulpn | grep -E "(5000|3000)" || ss -tulpn | grep -E "(5000|3000)"
echo ""

echo "2. Testing local connections:"
echo "Backend:"
curl -s http://localhost:5000/api/health && echo " ✓ Backend working locally" || echo " ✗ Backend not responding"
echo "Frontend:"
curl -s http://localhost:3000 > /dev/null && echo " ✓ Frontend working locally" || echo " ✗ Frontend not responding"
echo ""

echo "3. Checking local firewall (UFW):"
ufw status verbose
echo ""

echo "4. Checking iptables rules:"
iptables -L -n | grep -E "(5000|3000)" || echo "No iptables rules found for ports 5000/3000"
echo ""

echo "5. Testing from external IP (if possible):"
echo "Trying to connect from VPS to itself via external IP..."
curl -s --connect-timeout 5 http://93.127.195.74:5000/api/health && echo " ✓ External IP accessible from VPS" || echo " ✗ External IP not accessible (likely provider firewall)"
echo ""

echo "=== IMPORTANT ==="
echo "If servers work locally but not externally, you need to:"
echo "1. Check your VPS provider's firewall/security group settings"
echo "2. Open ports 5000 and 3000 in the provider's control panel"
echo "3. Common providers:"
echo "   - Hostinger: Check Firewall settings in hPanel"
echo "   - DigitalOcean: Check Networking > Firewalls"
echo "   - AWS: Check Security Groups"
echo "   - Azure: Check Network Security Groups"
echo "   - Google Cloud: Check Firewall Rules"
echo ""

