# 🚀 Step-by-Step: Deploying to Hugging Face Spaces in 3 Minutes

Follow these quick steps to launch your cloud Chromium instance on Hugging Face Spaces.

---

## Step 1: Create a New Space on Hugging Face

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Fill in the Space settings:
   - **Space Name:** Choose any name (e.g., `cloud-chromium` or `vnc-browser`).
   - **License:** `mit` (or `apache-2.0`).
   - **Select the Space SDK:** Click on **Docker** (Blank).
   - **Space Hardware:** Select **CPU Basic (Free - 2 vCPU, 16GB RAM, 50GB Disk)**.
   - **Visibility:** `Public` (accessible via public URL) or `Private` (requires HF login).
3. Click **Create Space**.

---

## Step 2: Upload Files to Your Space

You have two easy ways to upload this repository:

### Option A: Push via Git (Fastest)
In your terminal, clone your Hugging Face Space repo and push these files, or push directly from this repository:
```bash
# Add your Hugging Face space as a remote
git remote add hf https://huggingface.co/spaces/<your-hf-username>/<your-space-name>

# Push the main branch
git push hf main --force
```

### Option B: Upload via Web UI
1. In your newly created Space, click on the **Files and versions** tab.
2. Click **Add file** $\rightarrow$ **Upload files**.
3. Drag and drop all the files from this repository:
   - `Dockerfile`
   - `README.md`
   - `nginx.conf`
   - `supervisord.conf`
   - `entrypoint.sh`
   - `start-browser.sh`
   - `dashboard/` directory (with `app.py` and `static/`)
   - `docs/` directory
4. Click **Commit changes to main**.

---

## Step 3: (Optional) Configure Space Secrets

If you want to protect your VNC session with a password or specify a custom default URL:

1. In your Space, click on the **Settings** tab.
2. Scroll down to **Variables and secrets**.
3. Click **New secret** or **New variable**:
   - `VNC_PASSWORD`: Set a password to protect the desktop session.
   - `RESOLUTION`: Set initial screen resolution (default: `1280x720`).
   - `START_URL`: Set initial webpage Chromium opens (e.g. `https://google.com`).
   - `ENABLE_TUNNEL`: Set to `true` to enable Cloudflare Quick Tunnel.

---

## Step 4: Access Your Desktop

1. Hugging Face will automatically build the Docker image (takes about 1-2 minutes).
2. Once the build completes, the status changes to **Running** 🟢.
3. Open the **App** tab in your Space:
   - You will see the **Chromium VNC Dashboard** showing your runner's Public IP, Ports, and Memory.
   - Click on the **Remote Desktop (noVNC)** tab to view and control Chromium immediately in your browser!
