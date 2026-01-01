#!/bin/bash

# Update .env file with correct MongoDB credentials

cd ~/h1x1/hackingpanel

cat > .env <<'EOF'
MONGODB_URL=mongodb+srv://KaushikShresth:Shresth123&@cluster0.awof7.mongodb.net/
MONGODB_DB_NAME=HackingPanel
Serverurl = http://93.127.195.74:5000/
Username = Shresth
Password = hackur
EOF

echo "✓ .env file updated successfully!"
echo ""
echo "Current .env contents:"
cat .env
echo ""
echo "Restarting backend service to apply changes..."
sudo systemctl restart hackingpanel-backend
sleep 2
echo ""
echo "Backend status:"
sudo systemctl status hackingpanel-backend --no-pager -l | head -15

