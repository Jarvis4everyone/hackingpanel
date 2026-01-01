# Quick Fix for External Access

## Problem
Servers work locally but can't be accessed from the internet. This is because ports 5000 and 3000 are blocked by your VPS provider's firewall.

## Solution Options

### Option 1: Open Ports in VPS Provider Firewall (Recommended if possible)

**For Hostinger:**
1. Go to https://hpanel.hostinger.com/
2. Navigate to **VPS** → Your VPS
3. Go to **Firewall** section
4. Add rules:
   - Port **5000** (TCP) - Allow
   - Port **3000** (TCP) - Allow
5. Save and wait 1-2 minutes

Then access:
- Frontend: http://93.127.195.74:3000
- Backend: http://93.127.195.74:5000

### Option 2: Use Nginx Reverse Proxy (Use Standard Port 80)

If you can't open custom ports, use nginx to route traffic through port 80 (usually already open):

```bash
cd ~/h1x1/hackingpanel
git pull
chmod +x setup_nginx.sh
sudo ./setup_nginx.sh
```

Then access:
- Frontend: http://93.127.195.74
- Backend API: http://93.127.195.74/api

**Note:** You may need to open port 80 in your VPS provider's firewall if it's not already open.

### Option 3: Check if Ports are Actually Blocked

Test from your local computer:
```bash
# Test if ports are reachable
telnet 93.127.195.74 5000
telnet 93.127.195.74 3000

# Or use curl with timeout
curl -v --connect-timeout 5 http://93.127.195.74:5000/api/health
curl -v --connect-timeout 5 http://93.127.195.74:3000
```

If these fail, the ports are definitely blocked by your provider.

## Current Status

✅ Servers are running correctly
✅ Listening on 0.0.0.0 (all interfaces)
✅ Working locally on VPS
❌ External access blocked (provider firewall)

## Next Steps

1. **Try Option 1 first** - Open ports in your VPS provider's control panel
2. **If that doesn't work**, use **Option 2** - Nginx reverse proxy on port 80
3. **Verify** by accessing from your browser after setup

