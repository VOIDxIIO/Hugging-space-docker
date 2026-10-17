FROM debian:bookworm-slim

LABEL maintainer="VOIDxIIO <https://github.com/VOIDxIIO>"
LABEL description="Cloud Chromium Instance on Hugging Face Spaces with noVNC, Web Dashboard, and Multi-Client Remote Control"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    DISPLAY=:1 \
    RESOLUTION=1280x720 \
    HOME=/home/user \
    USER=user \
    PATH="/home/user/.local/bin:${PATH}"

# Install X11, Openbox, VNC, noVNC, Nginx, Supervisor, Chromium, Fonts, and Utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    openbox \
    novnc \
    websockify \
    chromium \
    chromium-sandbox \
    x11-utils \
    x11-xserver-utils \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-liberation \
    fonts-freefont-ttf \
    supervisor \
    nginx \
    curl \
    wget \
    ca-certificates \
    procps \
    net-tools \
    iproute2 \
    python3 \
    locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Cloudflared (for optional zero-config external tunneling)
RUN ARCH=$(dpkg --print-architecture) && \
    wget -q -O /tmp/cloudflared.deb "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${ARCH}.deb" && \
    dpkg -i /tmp/cloudflared.deb || apt-get install -fy && \
    rm -f /tmp/cloudflared.deb

# Create non-root user matching Hugging Face Spaces requirement (UID 1000)
RUN useradd -m -u 1000 -s /bin/bash user && \
    mkdir -p /home/user/app /home/user/.vnc /home/user/.config/chromium /tmp && \
    chmod -R 777 /tmp /var/log/nginx /var/lib/nginx

# Symlink noVNC standard index to vnc.html so direct root access on 6080 works cleanly
RUN ln -sf /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# Set working directory and copy application files
WORKDIR /home/user/app
COPY --chown=user:user . /home/user/app

# Set executable permissions on scripts
RUN chmod +x /home/user/app/entrypoint.sh /home/user/app/start-browser.sh

# Change ownership of entire app tree to user 1000
RUN chown -R user:user /home/user

# Switch to non-root user as required by Hugging Face Spaces
USER user

# Hugging Face Spaces exposes port 7860
EXPOSE 7860

ENTRYPOINT ["/home/user/app/entrypoint.sh"]
