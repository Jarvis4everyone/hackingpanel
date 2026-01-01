# Firewall Setup Guide

## Problem
Servers are running locally but not accessible from the internet. This is because your VPS provider's firewall is blocking the ports.

## Solution

### Step 1: Check Local Firewall (Already Done)
The script already configured UFW. Verify:
```bash
sudo ufw status
```

### Step 2: Configure VPS Provider Firewall

You need to open ports **5000** and **3000** in your VPS provider's control panel.

#### For Hostinger (Most Likely):
1. Log into **hPanel** (https://hpanel.hostinger.com/)
2. Go to **VPS** → Select your VPS
3. Go to **Firewall** section
4. Add rules:
   - **Port 5000** (TCP) - Allow
   - **Port 3000** (TCP) - Allow
5. Save and apply

#### For Other Providers:

**DigitalOcean:**
- Go to Networking → Firewalls
- Create/Edit firewall rules
- Add inbound rules for ports 5000 and 3000 (TCP)

**AWS EC2:**
- Go to EC2 → Security Groups
- Edit inbound rules
- Add rules for ports 5000 and 3000 (TCP) from 0.0.0.0/0

**Azure:**
- Go to Network Security Groups
- Add inbound security rules for ports 5000 and 3000

**Google Cloud:**
- Go to VPC Network → Firewall rules
- Create rules allowing TCP ports 5000 and 3000

### Step 3: Alternative - Use Standard Ports

If you can't open custom ports, we can configure the servers to use standard ports:
- Backend: Port 80 (HTTP) or 443 (HTTPS)
- Frontend: Port 80 (HTTP) or 443 (HTTPS)

This requires setting up a reverse proxy (nginx) which is more complex but uses standard ports that are usually already open.

### Step 4: Verify After Opening Ports

After opening ports in your provider's firewall, test:
```bash
# From your local computer, test:
curl http://93.127.195.74:5000/api/health
curl http://93.127.195.74:3000
```

Or open in browser:
- http://93.127.195.74:5000/api/health
- http://93.127.195.74:3000

## Quick Test Script

Run this on your VPS to check if ports are accessible:
```bash
./check_external_access.sh
```

