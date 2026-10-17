# 📱 Complete Guide: How to Control Your Chromium Container with VNC from Anywhere

This guide details all methods for connecting to and controlling your remote Chromium desktop instance running on Hugging Face Spaces from **any smartphone, tablet, laptop, or desktop computer worldwide**.

---

## Architecture Overview

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

---

## Method 1: Direct Web Access (noVNC) — Zero Installation

The fastest and most universal method. Requires **no apps, no installation, and no port forwarding**.

1. Open your browser on any device (Chrome, Safari, Firefox, Kiwi Browser, etc.).
2. Navigate to your Hugging Face Space URL:
   ```text
   https://<your-username>-<your-space-name>.hf.space
   ```
3. The integrated Dashboard displays real-time runner information:
   - **Public IP & Location** of the runner
   - **RAM / CPU / Uptime**
   - **Live Desktop View** embedded directly on the page!
4. **Standalone Fullscreen View:**  
   If you want to view *only* the desktop without the dashboard UI, append `/novnc/vnc.html?autoconnect=true&resize=scale` to your URL:
   ```text
   https://<your-username>-<your-space-name>.hf.space/novnc/vnc.html?autoconnect=true&resize=scale
   ```

### Touch Gestures on Mobile (Phones & Tablets)
- **Single Tap:** Left Click
- **Two-Finger Tap:** Right Click
- **Two-Finger Drag:** Scroll page up/down
- **Virtual Keyboard:** Tap the slide-out menu bar on the left edge of the screen and tap the keyboard icon.
- **Toggle Scaling:** Tap the gear icon in the slide-out menu and select `Local Scaling` so the entire desktop fits your phone screen.

---

## Method 2: Native VNC Clients on Mobile & Desktop

Native VNC apps give you specialized trackball navigation, lower input latency, and full native clipboard synchronization.

### Recommended Apps:
- **Android:** [AVNC](https://github.com/gujjwal00/avnc) (Free & Open Source) or **bVNC Secure VNC**
- **iOS (iPhone/iPad):** **Mocha VNC** or **RealVNC Viewer**
- **Windows / Mac / Linux:** **TigerVNC**, **TightVNC**, or **RealVNC Viewer**

### Connection Parameters:
- **Protocol:** `VNC over WebSocket (WSS)`
- **Host:** `<your-username>-<your-space-name>.hf.space`
- **Port:** `443` (Standard HTTPS)
- **Path:** `/websockify`
- **Password:** If you configured `VNC_PASSWORD` in your Space Secrets, enter it here. Otherwise leave empty.

---

## Method 3: Cloudflare Quick Tunnel (Free Global Access)

If your network blocks Hugging Face or you want a dedicated global domain:

1. In your Hugging Face Space, navigate to **Settings** $\rightarrow$ **Variables and secrets**.
2. Add a new secret or environment variable:
   - **Name:** `ENABLE_TUNNEL`
   - **Value:** `true`
3. Restart the Space.
4. The container automatically launches a Cloudflare Quick Tunnel.
5. In your Space Dashboard, the active `https://*.trycloudflare.com` URL will be automatically detected and displayed!

---

## Method 4: Raw TCP Port 5900 Forwarding (via Ngrok)

Hugging Face Spaces only exposes HTTP/HTTPS traffic on port 7860. If you have an older VNC client that requires a standard TCP socket on port 5900:

1. Sign up for a free account at [ngrok.com](https://ngrok.com) and copy your Auth Token.
2. In your Space **Settings** $\rightarrow$ **Variables and secrets**:
   - **Name:** `NGROK_AUTHTOKEN`
   - **Value:** `<your-ngrok-token>`
3. The container establishes an encrypted tunnel and logs the endpoint.
4. Connect using any standard VNC client to the generated Ngrok address.

---

## Method 5: Useful Controls & Troubleshooting

### What if I accidentally close Chromium?
- The container runs an **Auto-Recovery Supervisor** (`start-browser.sh`). If Chromium is closed, crashed, or terminated, the supervisor automatically relaunches it within 2 seconds.
- You can also click the **"Restart Browser"** button directly on the Web Dashboard at any time.

### How to change screen resolution on the fly?
- Open the Dashboard tab $\rightarrow$ select your desired resolution from the dropdown:
  - `1280x720` (Default 720p HD)
  - `1920x1080` (Full HD 1080p)
  - `720x1280` (Vertical Mobile Orientation)
