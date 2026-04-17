# ─────────────────────────────────────────────────────────────────
# Custom JupyterHub single-user notebook image
# CUDA 13.2.0 devel (nvcc included) + Ubuntu 24.04 (Python 3.12)
# ─────────────────────────────────────────────────────────────────
ARG CUDA_VER=13.2.0
ARG UBUNTU_VER=24.04

FROM nvidia/cuda:${CUDA_VER}-devel-ubuntu${UBUNTU_VER}

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/cuda/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# ── System dependencies ───────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-dev python3-pip python3-venv \
        git curl wget build-essential ca-certificates \
        libssl-dev libffi-dev \
    && ln -sf python3 /usr/bin/python \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Upgrade pip via get-pip.py (avoids Debian RECORD conflict) ────
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# ── Verify nvcc ───────────────────────────────────────────────────
RUN nvcc --version

# ── JupyterHub single-user + JupyterLab ──────────────────────────
RUN pip install --no-cache-dir \
        "jupyterhub==4.*" \
        "jupyterlab==4.*" \
        notebook \
        ipywidgets \
        ipykernel

# ── PyTorch ───────────────────────────────────────────────────────
RUN pip install --no-cache-dir \
        torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu128

# ── flash-attention (compiled with nvcc from CUDA 13.2) ───────────
RUN pip install --no-cache-dir packaging ninja && \
    pip install --no-cache-dir flash-attn --no-build-isolation

# ── Common ML libraries ───────────────────────────────────────────
RUN pip install --no-cache-dir \
        transformers accelerate datasets peft \
        bitsandbytes sentencepiece \
        pandas numpy matplotlib seaborn scikit-learn \
        tqdm rich

# ── Non-root user ─────────────────────────────────────────────────
ARG NB_USER=jovyan
ARG NB_UID=1000
RUN useradd -m -s /bin/bash -N -u ${NB_UID} ${NB_USER}

USER ${NB_USER}
WORKDIR /home/${NB_USER}

CMD ["jupyterhub-singleuser"]
