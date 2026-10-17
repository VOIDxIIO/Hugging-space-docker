#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "      🚀 Starting Cloud Chromium VNC Hugging Face Space   "
echo "      👤 User: $(whoami) (UID: $(id -u))                  "
echo "      🖥️ Resolution: ${RESOLUTION:-1280x720}              "
echo "      🌐 Exposed Port: 7860                               "
echo "=========================================================="

export RESOLUTION="${RESOLUTION:-1280x720}"
export DISPLAY="${DISPLAY:-:1}"
export HOME="${HOME:-/home/user}"

# Ensure temporary directories exist and are writable
mkdir -p /tmp/client_temp /tmp/proxy_temp /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp
mkdir -p "${HOME}/.vnc" "${HOME}/.config/chromium" "${HOME}/.config/openbox"

# Configure Openbox minimal default config
cat << 'EOF' > "${HOME}/.config/openbox/rc.xml"
<?xml version="1.0" encoding="UTF-8"?>
<openbox_config xmlns="http://openbox.org/3.4/rc">
  <theme>
    <name>Clearlooks</name>
    <titleLayout>NLIMC</titleLayout>
  </theme>
  <desktops>
    <number>1</number>
  </desktops>
</openbox_config>
EOF

# Setup VNC Password
if [ -n "${VNC_PASSWORD}" ]; then
    echo "[VNC Security] Setting up VNC password authentication..."
    x11vnc -storepasswd "${VNC_PASSWORD}" "${HOME}/.vnc/passwd"
    export X11VNC_AUTH_FLAG="-rfbauth ${HOME}/.vnc/passwd"
else
    echo "[VNC Security] No VNC_PASSWORD specified. Running with open access."
    export X11VNC_AUTH_FLAG="-nopw"
fi

# Optional Cloudflare Quick Tunnel Support
if [ "${ENABLE_TUNNEL}" = "true" ] || [ -n "${CLOUDFLARE_TUNNEL_TOKEN}" ]; then
    if [ -n "${CLOUDFLARE_TUNNEL_TOKEN}" ]; then
        echo "[Tunnel] Starting Cloudflare Named Tunnel..."
        cloudflared tunnel run --token "${CLOUDFLARE_TUNNEL_TOKEN}" > /tmp/tunnel.log 2>&1 &
    else
        echo "[Tunnel] Launching Cloudflare Quick Tunnel on port 7860..."
        cloudflared tunnel --url http://127.0.0.1:7860 > /tmp/tunnel.log 2>&1 &
        # Extract the public URL in background
        (
            for i in $(seq 1 30); do
                sleep 2
                URL=$(grep -oE 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' /tmp/tunnel.log | head -n 1 || true)
                if [ -n "${URL}" ]; then
                    echo "${URL}" > /tmp/tunnel_url.txt
                    echo "[Tunnel] Global Tunnel Ready: ${URL}"
                    break
                fi
            done
        ) &
    fi
fi

# Optional Ngrok Tunnel Support
if [ -n "${NGROK_AUTHTOKEN}" ]; then
    echo "[Tunnel] Starting Ngrok tunnel..."
    ngrok config add-authtoken "${NGROK_AUTHTOKEN}" || true
    ngrok http 7860 --log=stdout > /tmp/ngrok.log 2>&1 &
    (
        sleep 4
        URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -oE 'https://[a-zA-Z0-9-]+\.ngrok-free\.app' | head -n 1 || true)
        if [ -n "${URL}" ]; then
            echo "${URL}" > /tmp/tunnel_url.txt
            echo "[Tunnel] Ngrok Tunnel Ready: ${URL}"
        fi
    ) &
fi

# Execute Supervisor
exec /usr/bin/supervisord -c /home/user/app/supervisord.conf
