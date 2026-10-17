---
title: Cloud Chromium VNC Space
emoji: 🌐
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# 🌐 Cloud Chromium VNC Space

> **Run a full, dedicated desktop Chromium instance inside Hugging Face Spaces with built-in noVNC remote access, real-time public IP & port telemetry, auto-restart supervisor, and multi-node fleet scalability.**

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces)
[![Docker SDK](https://img.shields.io/badge/Docker-SDK%20Port%207860-blue?logo=docker)](https://huggingface.co/docs/hub/spaces-sdks-docker)
[![VNC](https://img.shields.io/badge/VNC-noVNC%20%2B%20x11vnc-orange)](https://novnc.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Project Overview

This project provides an out-of-the-box, containerized desktop environment running **Chromium Browser** on **Hugging Face Spaces (Docker SDK)**. 

### 🌟 Key Highlights
- **🖥️ Remote Desktop from Any Browser:** Uses **noVNC** over WebSockets to let you view and control the full Chromium desktop directly from your phone (Kiwi, Chrome, Safari) or PC without installing any software.
- **📊 Real-Time Control & Telemetry UI:** Integrated dark-mode dashboard on port 7860 displaying the container's **Public IP, Cloud Region, Port 5900/7860 Status, RAM usage, and Uptime**.
- **🔄 Auto-Recovery Supervisor:** If Chromium is closed by mistake, killed, or crashes from memory load, the supervisor **automatically relaunches a fresh Chromium instance in under 2 seconds**.
- **📱 Mobile Touch Friendly:** Full touch support (single-tap click, two-finger scroll/right-click, virtual mobile keyboard).
- **📐 Dynamic Resolution Switcher:** Switch between 720p HD, 1080p FHD, and Mobile Portrait mode on the fly with 1 click.
- **🚇 Zero-Config Tunneling:** Built-in Cloudflare Quick Tunnel and Ngrok support for direct external connections.

---

## 🚀 Quick Deployment Options

### ⚡ Option A: 1-Click Free GitHub Codespaces (No Credit Card, 60 Hrs/Mo Free)
1. At the top of this repository, click **`< > Code`** ➔ **`Codespaces`** ➔ **`Create codespace on main`**.
2. GitHub boots your Docker Chromium instance and forwards port `7860`.
3. Click **"Open in Browser"** when the notification appears. Done!

### 🌐 Option B: Hugging Face Spaces
1. Go to **[huggingface.co/new-space](https://huggingface.co/new-space)**.
2. Select **Space SDK: Docker** (Blank) and choose **CPU Basic Tier**.
   > ⚠️ *Note:* If Hugging Face asks for a credit card or PRO subscription ($9/mo) for Docker, see [Free Deployment Alternatives (Zero Card)](docs/FREE_DEPLOYMENT_ALTERNATIVES.md).
3. Push or upload the files from this repository to your Space:
   ```bash
   git remote add hf https://huggingface.co/spaces/<YOUR_HF_USERNAME>/<YOUR_SPACE_NAME>
   git push hf main --force
   ```
4. Hugging Face builds the container and serves your live Chromium desktop on:
   ```text
   https://<YOUR_HF_USERNAME>-<YOUR_SPACE_NAME>.hf.space
   ```

*Detailed visual walkthrough:* 👉 **[Read the Full Deployment Guide](docs/HUGGINGFACE_DEPLOY_GUIDE.md)** | **[Free Alternatives Guide](docs/FREE_DEPLOYMENT_ALTERNATIVES.md)**

---

## 📊 How Many Dockers Can We Make? (Capacity & Scaling)

| Metric | Free Tier Quota | Scaled Multi-Account Fleet |
| :--- | :--- | :--- |
| **Total Spaces Created** | **Unlimited** | **Unlimited** |
| **Concurrent Active Spaces** | **5 to 10 per account** | **50 - 100+ instances** |
| **Dedicated RAM per Space** | **16 GB RAM** | 16 GB per node |
| **vCPU per Space** | **2 vCPUs** | 2 vCPUs per node |
| **Monthly Cost** | **$0.00 / Free** | **$0.00 / Free** |

### Keeping Free Spaces Running 24/7 (Preventing Sleep)
Free Hugging Face spaces go to sleep after 48 hours if no web traffic is received.  
To keep your container running 24/7 forever without sleeping:
1. Register a free account at [UptimeRobot.com](https://uptimerobot.com) or [cron-job.org](https://cron-job.org).
2. Set an HTTP GET monitor pinging `https://<your-space>.hf.space/api/status` **every 10–15 minutes**.
3. Because the ping receives a `200 OK`, Hugging Face records active web traffic and **the Space will never sleep**!

*Full details on quotas, multi-account fleets, and sleep policies:* 👉 **[Read the Instance Scaling Guide](docs/INSTANCE_SCALING_LIMITS.md)**

---

## 🎮 How to Control with VNC from Anywhere

```
 [ Your Device ] (Phone / PC / Tablet)
        │
        ▼ (HTTPS / WSS over Port 7860)
 ┌────────────────────────────────────────────────────────────┐
 │  Hugging Face Space Gateway (https://*.hf.space:7860)       │
 │                                                            │
 │   ┌───────────┐     ┌──────────────┐     ┌─────────────┐   │
 │   │   Nginx   │────▶│ Dashboard UI │     │  websockify │   │
 │   │ (Port 7860)     │ (Port 8000)  │     │ (Port 6080) │   │
 │   └─────┬─────┘     └──────────────┘     └──────┬──────┘   │
 │         │                                       │          │
 │         ▼                                       ▼          │
 │    noVNC Web App ◀───────────────────────▶ x11vnc Server   │
 │                                             (Port 5900)    │
 │                                                 │          │
 │                                                 ▼          │
 │                                            Xvfb Display :1 │
 │                                                 │          │
 │                                                 ▼          │
 │                                           Chromium Browser │
 └────────────────────────────────────────────────────────────┘
```

You have multiple options to connect:

### 1. Web Browser (Direct noVNC — Recommended)
Open your Space URL in any mobile or desktop browser:
```text
https://<your-username>-<space-name>.hf.space
```
Click the **"Remote Desktop (noVNC)"** tab, or open directly in fullscreen:
```text
https://<your-username>-<space-name>.hf.space/novnc/vnc.html?autoconnect=true&resize=scale
```

### 2. Native VNC Mobile & Desktop Apps
- **Android:** AVNC (Open Source) or bVNC
- **iOS:** Mocha VNC or RealVNC Viewer
- **PC / Mac:** TigerVNC or TightVNC
- **Connection Host:** `<your-space-name>.hf.space` (Port `443` over WSS path `/websockify`)

### 3. Direct Cloudflare Tunnel (Optional)
Add `ENABLE_TUNNEL=true` in your Space settings to automatically generate a global `https://*.trycloudflare.com` URL shown on your dashboard.

*Detailed connection instructions and mobile gestures:* 👉 **[Read the VNC Remote Control Guide](docs/VNC_REMOTE_CONTROL_GUIDE.md)**

---

## 🖥️ Web Management Dashboard

The web management dashboard on port `7860` provides:
1. **Public IP & Location:** Live external IP address of the Hugging Face runner (Iowa, Frankfurt, Paris, etc.).
2. **Port Telemetry:** Shows raw VNC (5900), noVNC WebSocket (6080), and Web Gateway (7860).
3. **Hardware Gauges:** Real-time memory consumption (MB used / 16GB total) and CPU load.
4. **Embedded noVNC Stream:** Clean iframe integration with one-click fullscreen.
5. **Quick Actions:** Force-restart Chromium button, dynamic resolution switcher, and live reconnection controls.

---

## ⚙️ Environment Variables & Secrets

Configure these in your Hugging Face Space under **Settings $\rightarrow$ Variables and secrets**:

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `VNC_PASSWORD` | *(None)* | Sets a password required to access the VNC session. |
| `RESOLUTION` | `1280x720` | Virtual screen resolution (e.g. `1920x1080`, `1280x720`, `720x1280`). |
| `START_URL` | `https://www.google.com` | Webpage Chromium automatically opens on startup. |
| `CHROME_FLAGS` | *(Standard flags)* | Extra command-line parameters passed to Chromium. |
| `ENABLE_TUNNEL` | `false` | Set to `true` to launch Cloudflare Quick Tunnel. |
| `CLOUDFLARE_TUNNEL_TOKEN` | *(None)* | Connects to a persistent Cloudflare Named Tunnel. |
| `NGROK_AUTHTOKEN` | *(None)* | Exposes raw port 5900 via Ngrok. |

---

## 📁 Repository Structure

```
Hugging-space-docker/
├── Dockerfile                         # Production-grade HF Space container configuration
├── README.md                          # Hugging Face metadata & documentation overview
├── nginx.conf                         # Reverse proxy for port 7860 multiplexing
├── supervisord.conf                   # Process manager (Xvfb, Openbox, x11vnc, noVNC, Nginx, Chrome)
├── entrypoint.sh                      # Runtime initializer (passwords, tunnels, permissions)
├── start-browser.sh                   # Chromium auto-recovery supervisor
├── dashboard/
│   ├── app.py                         # Python dashboard API & telemetry server
│   └── static/
│       ├── index.html                 # Modern glassmorphic dashboard UI
│       ├── style.css                  # Responsive styles
│       └── app.js                     # Live telemetry & action controllers
├── docs/
│   ├── INSTANCE_SCALING_LIMITS.md    # Guide on instance limits, quotas & scaling
│   ├── VNC_REMOTE_CONTROL_GUIDE.md    # Guide on controlling VNC from anywhere
│   └── HUGGINGFACE_DEPLOY_GUIDE.md    # Visual step-by-step deploy instructions
└── .github/
    └── workflows/
        └── keepalive.yml              # Automated 24/7 keepalive workflow
```

---

## 📜 License

Released under the [MIT License](LICENSE). Built for developers, scrapers, and remote desktop users on Hugging Face Spaces.
