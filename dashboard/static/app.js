/**
 * Chromium VNC Space - Frontend Dashboard Controller
 */

// Tab Switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

    btn.classList.add('active');
    const target = btn.getAttribute('data-tab');
    const targetContent = document.getElementById(target);
    if (targetContent) targetContent.classList.add('active');
  });
});

// Fullscreen Toggle
const btnFullscreen = document.getElementById('btn-toggle-fullscreen');
if (btnFullscreen) {
  btnFullscreen.addEventListener('click', () => {
    document.body.classList.toggle('fullscreen-mode');
    btnFullscreen.textContent = document.body.classList.contains('fullscreen-mode')
      ? '✕ Exit Fullscreen'
      : '⛶ Fullscreen';
  });
}

// Open VNC in New Window
const btnNewWindow = document.getElementById('btn-open-new-window');
if (btnNewWindow) {
  btnNewWindow.addEventListener('click', () => {
    window.open('/novnc/vnc.html?autoconnect=true&resize=scale&reconnect=true', '_blank');
  });
}

// Reconnect VNC Iframe
const btnReconnect = document.getElementById('btn-reconnect-vnc');
if (btnReconnect) {
  btnReconnect.addEventListener('click', () => {
    const iframe = document.getElementById('vnc-iframe');
    if (iframe) {
      iframe.src = iframe.src;
    }
  });
}

// Copy Helper
function copyText(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(() => {
    const orig = el.innerText;
    el.innerText = 'Copied to clipboard!';
    setTimeout(() => { el.innerText = orig; }, 1800);
  }).catch(() => {
    alert('Copied: ' + text);
  });
}

// Restart Browser API Call
async function restartBrowser() {
  const feedback = document.getElementById('action-feedback');
  if (feedback) {
    feedback.style.color = '#38bdf8';
    feedback.innerText = 'Sending restart signal to Chromium...';
  }

  try {
    const res = await fetch('/api/restart-browser', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      if (feedback) {
        feedback.style.color = '#34d399';
        feedback.innerText = '✅ ' + data.message;
      }
      setTimeout(fetchStatus, 1500);
    } else {
      if (feedback) {
        feedback.style.color = '#f87171';
        feedback.innerText = '❌ Failed: ' + (data.error || 'Unknown error');
      }
    }
  } catch (err) {
    if (feedback) {
      feedback.style.color = '#f87171';
      feedback.innerText = '❌ Network error while restarting browser.';
    }
  }
}

const btnRestart1 = document.getElementById('btn-restart-browser');
const btnRestart2 = document.getElementById('btn-restart-browser-action');
if (btnRestart1) btnRestart1.addEventListener('click', restartBrowser);
if (btnRestart2) btnRestart2.addEventListener('click', restartBrowser);

// Resolution Buttons
document.querySelectorAll('.btn-res').forEach(btn => {
  btn.addEventListener('click', async () => {
    const res = btn.getAttribute('data-res');
    try {
      const resp = await fetch('/api/set-resolution', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resolution: res })
      });
      const data = await resp.json();
      if (data.success) {
        alert('Resolution set to ' + res + '. Reconnecting VNC...');
        const iframe = document.getElementById('vnc-iframe');
        if (iframe) iframe.src = iframe.src;
      }
    } catch (e) {
      console.error(e);
    }
  });
});

const quickRes = document.getElementById('quick-res-select');
if (quickRes) {
  quickRes.addEventListener('change', async (e) => {
    const res = e.target.value;
    try {
      await fetch('/api/set-resolution', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resolution: res })
      });
      const iframe = document.getElementById('vnc-iframe');
      if (iframe) iframe.src = iframe.src;
    } catch (err) {
      console.error(err);
    }
  });
}

// Status Poller
async function fetchStatus() {
  try {
    const res = await fetch('/api/status?t=' + Date.now());
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();

    // Status Indicator
    const statusIndicator = document.getElementById('status-indicator');
    if (statusIndicator) {
      statusIndicator.innerHTML = '<span class="dot pulse"></span> Online';
    }

    // Space Name
    const spaceBadge = document.getElementById('space-name-badge');
    if (spaceBadge && data.space_id) {
      spaceBadge.innerText = data.space_id;
    }

    // Public IP & Geo
    const valIp = document.getElementById('val-ip');
    const valGeo = document.getElementById('val-geo');
    if (valIp && data.public_ip_info) {
      valIp.innerText = data.public_ip_info.ip || 'Unavailable';
      const loc = [data.public_ip_info.city, data.public_ip_info.country, data.public_ip_info.org]
        .filter(x => x && x !== 'Unknown')
        .join(' • ');
      valGeo.innerText = loc || 'Cloud Container';
    }

    // RAM
    const valRam = document.getElementById('val-ram');
    const ramFill = document.getElementById('ram-fill');
    if (valRam && data.system && data.system.memory) {
      const m = data.system.memory;
      valRam.innerText = `${m.used_mb} / ${m.total_mb} MB (${m.percent}%)`;
      if (ramFill) ramFill.style.width = Math.min(100, m.percent) + '%';
    }

    // Uptime & CPU
    const valUptime = document.getElementById('val-uptime');
    const valCpu = document.getElementById('val-cpu');
    if (valUptime && data.system) {
      valUptime.innerText = data.system.uptime_formatted;
      if (valCpu) valCpu.innerText = 'Load: ' + data.system.cpu_usage;
    }

    // Web URL
    const codeWebUrl = document.getElementById('code-web-url');
    if (codeWebUrl) {
      const origin = window.location.origin;
      codeWebUrl.innerText = `${origin}/novnc/vnc.html?autoconnect=true&resize=scale`;
    }

    // Tunnel Info
    const tunnelContainer = document.getElementById('tunnel-status-container');
    if (tunnelContainer) {
      if (data.tunnel && data.tunnel.active && data.tunnel.url) {
        tunnelContainer.innerHTML = `
          <div class="code-box">
            <span class="code-url"><strong>Active Tunnel URL:</strong> <a href="${data.tunnel.url}" target="_blank" style="color:#38bdf8">${data.tunnel.url}</a></span>
          </div>
          <p style="margin-top:8px">This tunnel gives you direct global access to this container bypassing all restrictive firewalls.</p>
        `;
      } else {
        tunnelContainer.innerHTML = `
          <p style="color:var(--text-dim)">No external tunnel active. The Space is operating securely via native Hugging Face HTTPS routing on port 7860.</p>
          <p style="margin-top:6px; font-size:12px; color:var(--text-muted)">To activate a Cloudflare or Ngrok tunnel, add <code>CLOUDFLARE_TUNNEL_TOKEN</code> or <code>NGROK_AUTHTOKEN</code> in your Space Settings &gt; Secrets.</p>
        `;
      }
    }

    // VNC Host Info
    const infoHost = document.getElementById('info-vnc-host');
    if (infoHost) {
      infoHost.innerText = window.location.hostname || data.space_url;
    }

    const infoPw = document.getElementById('info-vnc-pw');
    if (infoPw) {
      infoPw.innerText = data.vnc_password_enabled ? 'Configured (Secret set)' : 'Disabled (Open Access)';
    }

  } catch (err) {
    console.warn('[Status] Poll failed:', err);
    const statusIndicator = document.getElementById('status-indicator');
    if (statusIndicator) {
      statusIndicator.innerHTML = '<span class="dot" style="background:#ef4444"></span> Offline / Reconnecting';
    }
  }
}

// Initial fetch and 5s polling interval
fetchStatus();
setInterval(fetchStatus, 5000);

const btnRefresh = document.getElementById('btn-reload-dashboard');
if (btnRefresh) btnRefresh.addEventListener('click', fetchStatus);
