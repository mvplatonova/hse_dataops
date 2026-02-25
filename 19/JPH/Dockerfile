FROM python:3.14-slim

LABEL description="JupyterHub server with configurable-http-proxy"
LABEL version="1.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Node.js и npm для configurable-http-proxy
    nodejs \
    npm \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash -u 1000 jupyterhub

WORKDIR /srv/jupyterhub

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN npm install -g configurable-http-proxy

RUN mkdir -p /srv/jupyterhub/data && \
    chown -R jupyterhub:jupyterhub /srv/jupyterhub

COPY jupyterhub_config.py /srv/jupyterhub/

RUN chown jupyterhub:jupyterhub /srv/jupyterhub/jupyterhub_config.py

# 8000 - JupyterHub web interface
# 8081 - JupyterHub API
EXPOSE 8000 8081

USER jupyterhub

CMD ["jupyterhub", "--config", "/srv/jupyterhub/jupyterhub_config.py"]
