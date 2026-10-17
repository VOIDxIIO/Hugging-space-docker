#!/usr/bin/env bash
# Chromium Auto-Restart & Crash-Recovery Supervisor
# Ensures Chromium is always running on display :1 and restarts instantly if closed or killed.

export DISPLAY="${DISPLAY:-:1}"
START_URL="${START_URL:-https://www.google.com}"
CHROME_USER_DATA="${CHROME_USER_DATA:-/home/user/.config/chromium}"

# Wait for X server (:1) to be ready
echo "[Browser Supervisor] Waiting for X display ${DISPLAY} to be ready..."
while ! xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; do
    sleep 0.5
done
echo "[Browser Supervisor] Display ${DISPLAY} detected! Starting Chromium loop..."

# Clean up any stale lock files from previous runs
rm -f "${CHROME_USER_DATA}/SingletonLock" 2>/dev/null || true

# Supervisor Loop
while true; do
    echo "[Browser Supervisor] Launching Chromium with URL: ${START_URL}..."
    
    # Locate chromium or chrome binary
    CHROMIUM_BIN=$(which chromium || which chromium-browser || which google-chrome || which google-chrome-stable)
    
    if [ -z "${CHROMIUM_BIN}" ]; then
        echo "[Browser Supervisor] ERROR: Chromium binary not found in PATH!"
        sleep 5
        continue
    fi

    ${CHROMIUM_BIN} \
        --no-sandbox \
        --disable-dev-shm-usage \
        --disable-gpu \
        --disable-software-rasterizer \
        --remote-debugging-port=9222 \
        --remote-debugging-address=127.0.0.1 \
        --start-maximized \
        --no-first-run \
        --no-default-browser-check \
        --disable-background-networking \
        --disable-features=Translate \
        --user-data-dir="${CHROME_USER_DATA}" \
        ${CHROME_FLAGS} \
        "${START_URL}"

    EXIT_CODE=$?
    echo "[Browser Supervisor] Chromium exited with code ${EXIT_CODE}. Relaunching in 2 seconds..."
    sleep 2
done
