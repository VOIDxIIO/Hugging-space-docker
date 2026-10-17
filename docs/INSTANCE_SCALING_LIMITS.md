# 📊 How Many Chromium Docker Spaces Can You Run on Hugging Face?

This guide covers the **exact limits, resource allocations, auto-sleep policies, and multi-node scaling strategies** for running Dockerized Chromium instances on Hugging Face Spaces.

---

## 1. Hugging Face Free Tier Resource Specifications

Every free Hugging Face Space provides dedicated container resources:

| Resource | Free Tier Allocation | Notes |
| :--- | :--- | :--- |
| **vCPU** | **2 vCPUs** | Dedicated virtual cores |
| **RAM** | **16 GB RAM** | Extremely generous for Chromium |
| **Disk Space** | **50 GB** | Ephemeral container storage |
| **Exposed Port** | **Port 7860** | Routed over public HTTPS (`https://*.hf.space`) |
| **Bandwidth** | **Unlimited** | Standard fair-use cloud traffic |
| **Cost** | **$0.00 / Free** | Completely free forever |

> **Memory Consumption Reality:**  
> A standard Chromium browser running Xvfb, Openbox, x11vnc, noVNC, and Nginx consumes **between 450 MB and 900 MB of RAM**. Because Hugging Face gives you **16,000 MB (16 GB)**, a single container can easily handle heavy multitasking, multiple tabs, long videos, and automation without ever running out of memory.

---

## 2. How Many Dockers Can You Make?

### A. Total Spaces Created per Account: **UNLIMITED**
- There is **no limit** to the number of Space repositories you can create under your Hugging Face profile. You can create 50, 100, or 500 Space repositories.

### B. Simultaneously Running Free Spaces: **5 to 10 per Account**
- Hugging Face automatically schedules and spins up free compute clusters for your active Spaces.
- On a single free account, you can typically run **5 to 10 Spaces concurrently** in active running state without any throttling.
- If you start too many simultaneously on a single account, subsequent spaces may enter a `Queued` or `Building` state until compute slots rotate.

### C. Scaling to 20, 50, or 100+ Free Instances (Multi-Account Fleet)
If you require a massive fleet of 20, 50, or 100+ separate browser nodes for automated tasks, testing, or scraping:
1. Register multiple free Hugging Face accounts (using different email addresses).
2. On each account, fork or duplicate this repository (`Hugging-space-docker`).
3. Deploy 5 to 8 instances per account.
4. Each instance gets its own independent public IP, isolated browser session, and 16GB of dedicated RAM.

---

## 3. Hugging Face Inactivity Sleep & 24/7 Keep-Alive

### The 48-Hour Inactivity Rule
On the free tier, Hugging Face automatically puts Spaces into **Sleep Mode after 48 hours of inactivity** (i.e., when no incoming HTTP web requests hit the Space).

### How to Keep It Running 24/7 (Never Sleep)
Because the sleep mechanism is triggered by a lack of HTTP traffic, you can keep your space awake permanently by sending an automated HTTP GET ping every 10–15 minutes:

#### Option 1: UptimeRobot (Recommended - Free & Easiest)
1. Go to [UptimeRobot.com](https://uptimerobot.com) and create a free account.
2. Click **Add New Monitor**:
   - **Monitor Type:** `HTTP(s)`
   - **Friendly Name:** `Chromium HF Node 1`
   - **URL (or IP):** `https://<your-username>-<space-name>.hf.space/api/status`
   - **Monitoring Interval:** `Every 10 minutes`
3. Click **Create Monitor**.
4. UptimeRobot will ping `/api/status` every 10 minutes. Because this endpoint returns `200 OK`, Hugging Face records active web traffic and **will never put the container to sleep**!

#### Option 2: Cron-Job.org (Free)
1. Register at [cron-job.org](https://cron-job.org).
2. Create a cron job pointing to `https://<your-space>.hf.space/api/status` running every 15 minutes.

#### Option 3: GitHub Actions Keep-Alive Workflow
This repository includes a pre-built GitHub Actions workflow in `.github/workflows/keepalive.yml` that pings your Space URLs on an hourly schedule automatically.

---

## 4. Hardware Scaling Comparison

If you ever need dedicated GPUs or more CPU power, Hugging Face offers paid upgrades per Space:

| Tier | vCPU / GPU | RAM | Disk | Pricing |
| :--- | :--- | :--- | :--- | :--- |
| **CPU Basic (Free)** | 2 vCPU | 16 GB | 50 GB | **FREE** |
| **CPU Upgrade** | 8 vCPU | 32 GB | 50 GB | $0.03 / hour |
| **T4 GPU Small** | 4 vCPU + 16GB T4 | 16 GB | 50 GB | $0.60 / hour |
| **A10G GPU** | 12 vCPU + 24GB A10G | 46 GB | 150 GB | $1.05 / hour |

*For running Chromium, automation, and remote desktop, the **Free CPU Basic tier** is more than sufficient.*
