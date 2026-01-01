#!/bin/bash

echo "=== Final Access Check ==="
echo ""

echo "1. Checking nginx access logs (to see if requests are reaching server):"
echo "----------------------------------------"
sudo tail -20 /var/log/nginx/access.log
echo ""

echo "2. Checking nginx error logs:"
echo "----------------------------------------"
sudo tail -20 /var/log/nginx/error.log
echo ""

echo "3. Testing nginx configuration:"
nginx -t
echo ""

echo "4. Verifying nginx is serving the correct site:"
curl -s -I http://localhost | head -10
echo ""

echo "5. Testing backend through nginx:"
curl -s http://localhost/api/health
echo ""
echo ""

echo "6. Checking if SELinux or AppArmor might be blocking:"
if command -v getenforce &> /dev/null; then
    echo "SELinux: $(getenforce)"
else
    echo "SELinux: Not installed"
fi

if [ -f /sys/kernel/security/apparmor/profiles ]; then
    echo "AppArmor: Active"
    aa-status 2>/dev/null | grep nginx || echo "No nginx AppArmor profile"
else
    echo "AppArmor: Not active"
fi
echo ""

echo "7. Testing from VPS to external IP:"
curl -s --connect-timeout 5 -H "Host: 93.127.195.74" http://93.127.195.74/api/health && echo " ✓" || echo " ✗"
echo ""

echo "=== If logs are empty, requests aren't reaching your server ==="
echo "This could mean:"
echo "1. Your ISP/network is blocking the connection"
echo "2. There's a routing issue"
echo "3. Try accessing from a different network (mobile data)"
echo ""

