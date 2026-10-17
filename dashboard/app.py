#!/usr/bin/env python3
"""
Chromium VNC Space - Dashboard & API Server
Serves real-time system stats, public IP, VNC connection info, and browser management controls.
Runs on 127.0.0.1:8000 and is reverse-proxied by Nginx on port 7860.
"""

import os
import sys
import json
import time
import socket
import urllib.request
import subprocess
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("DASHBOARD_PORT", 8000))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
START_TIME = time.time()

# Cache for public IP to avoid hitting rate limits
_cached_ip_info = {"data": None, "timestamp": 0}

def get_public_ip_info():
    global _cached_ip_info
    now = time.time()
    if _cached_ip_info["data"] and (now - _cached_ip_info["timestamp"] < 60):
        return _cached_ip_info["data"]

    info = {
        "ip": "Detecting...",
        "city": "Unknown",
        "region": "Unknown",
        "country": "Unknown",
        "org": "Cloud Provider"
    }

    try:
        req = urllib.request.Request(
            "https://ipinfo.io/json",
            headers={"User-Agent": "curl/7.68.0", "Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            info["ip"] = data.get("ip", "Unknown")
            info["city"] = data.get("city", "Unknown")
            info["region"] = data.get("region", "Unknown")
            info["country"] = data.get("country", "Unknown")
            info["org"] = data.get("org", "Unknown")
            _cached_ip_info = {"data": info, "timestamp": now}
            return info
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            "https://api.ipify.org?format=json",
            headers={"User-Agent": "curl/7.68.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            info["ip"] = data.get("ip", "Unknown")
            _cached_ip_info = {"data": info, "timestamp": now}
            return info
    except Exception:
        pass

    info["ip"] = "Unavailable (Check outbound connectivity)"
    return info

def get_system_stats():
    stats = {
        "uptime_seconds": int(time.time() - START_TIME),
        "uptime_formatted": format_uptime(int(time.time() - START_TIME)),
        "cpu_usage": "N/A",
        "memory": {"used_mb": 0, "total_mb": 0, "percent": 0},
        "disk": {"used_gb": 0, "total_gb": 0, "percent": 0},
        "browser_running": False,
        "browser_pid": None
    }

    # Memory info via /proc/meminfo
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        mem = {}
        for line in lines:
            parts = line.split(":")
            if len(parts) == 2:
                mem[parts[0].strip()] = int(parts[1].strip().split()[0])
        total_kb = mem.get("MemTotal", 0)
        avail_kb = mem.get("MemAvailable", mem.get("MemFree", 0))
        used_kb = max(0, total_kb - avail_kb)
        if total_kb > 0:
            stats["memory"]["total_mb"] = round(total_kb / 1024)
            stats["memory"]["used_mb"] = round(used_kb / 1024)
            stats["memory"]["percent"] = round((used_kb / total_kb) * 100, 1)
    except Exception:
        pass

    # Disk usage
    try:
        total, used, free = shutil.disk_usage("/")
        stats["disk"]["total_gb"] = round(total / (1024**3), 1)
        stats["disk"]["used_gb"] = round(used / (1024**3), 1)
        stats["disk"]["percent"] = round((used / total) * 100, 1)
    except Exception:
        pass

    # Browser process check
    try:
        res = subprocess.run(["pgrep", "-f", "chromium|chrome"], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            pids = res.stdout.strip().split("\n")
            stats["browser_running"] = True
            stats["browser_pid"] = pids[0]
    except Exception:
        pass

    # CPU load average
    try:
        load1, load5, load15 = os.getloadavg()
        stats["cpu_usage"] = f"{load1:.2f} (1m), {load5:.2f} (5m)"
    except Exception:
        pass

    return stats

def get_tunnel_info():
    tunnel_file = "/tmp/tunnel_url.txt"
    if os.path.exists(tunnel_file):
        try:
            with open(tunnel_file, "r") as f:
                url = f.read().strip()
                if url:
                    return {"active": True, "url": url}
        except Exception:
            pass
    return {"active": False, "url": None}

def format_uptime(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, sec = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {sec}s"
    elif minutes > 0:
        return f"{minutes}m {sec}s"
    else:
        return f"{sec}s"

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            space_id = os.environ.get("SPACE_ID", "local-dev")
            space_host = os.environ.get("SPACE_HOST", f"{space_id}.hf.space" if space_id != "local-dev" else "localhost:7860")
            vnc_pw_set = bool(os.environ.get("VNC_PASSWORD"))

            data = {
                "status": "online",
                "space_id": space_id,
                "space_url": f"https://{space_host}" if not space_host.startswith("localhost") else f"http://{space_host}",
                "public_ip_info": get_public_ip_info(),
                "system": get_system_stats(),
                "ports": {
                    "vnc_raw": 5900,
                    "novnc_internal": 6080,
                    "web_gateway": 7860
                },
                "tunnel": get_tunnel_info(),
                "vnc_password_enabled": vnc_pw_set,
                "resolution": os.environ.get("RESOLUTION", "1280x720")
            }
            self.wfile.write(json.dumps(data, indent=2).encode())
            return

        elif path == "/api/info":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            info = {
                "name": "Cloud Chromium VNC Space",
                "version": "1.0.0",
                "author": "VOIDxIIO",
                "docs": "https://github.com/VOIDxIIO/Hugging-space-docker"
            }
            self.wfile.write(json.dumps(info).encode())
            return

        # Serve static files from STATIC_DIR
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/restart-browser":
            try:
                # Signal the supervisor to restart the browser or kill current chromium instances
                subprocess.run(["pkill", "-9", "-f", "chromium|chrome"], capture_output=True)
                # start-browser.sh loop will automatically relaunch it
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "message": "Chromium killed. Auto-supervisor is launching a fresh instance."
                }).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
            return

        elif path == "/api/set-resolution":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode()
                payload = json.loads(body) if body else {}
                res = payload.get("resolution", "1280x720")
                if "x" in res:
                    w, h = res.split("x")
                    os.environ["RESOLUTION"] = res
                    # Try xrandr if available
                    subprocess.run(["xrandr", "-s", res], env={**os.environ, "DISPLAY": ":1"}, capture_output=True)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True, "resolution": res}).encode())
                    return
                raise ValueError("Invalid format. Use WxH (e.g. 1920x1080)")
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
            return

        self.send_response(404)
        self.end_headers()

def run():
    print(f"[Dashboard] Starting Dashboard Server on 127.0.0.1:{PORT}...")
    server = HTTPServer(("127.0.0.1", PORT), DashboardHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
