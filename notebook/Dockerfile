# ─────────────────────────────────────────────────────────────────
# Custom JupyterHub single-user notebook image
# Base: Ubuntu 24.04 (Python 3.12 built-in) + CUDA devel (nvcc)
#
# CUDA 12.8.x = minimum for Blackwell (GB10).
# To upgrade to CUDA 13.x when released: change CUDA_VER below.
# ─────────────────────────────────────────────────────────────────
ARG CUDA_VER=12.8.1
ARG UBUNTU_VER=24.04

FROM nvidia/cuda:${CUDA_VER}-devel-ubuntu${UBUNTU_VER}

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/cuda/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# ── System dependencies ───────────────────────────────────────────
# Ubuntu 24.04 ships Python 3.12 natively — no PPA needed
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-dev python3-pip python3-venv \
        git curl wget build-essential ca-certificates \
        libssl-dev libffi-dev \
    && ln -sf python3 /usr/bin/python \
    && pip install --upgrade pip --break-system-packages \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Verify nvcc ───────────────────────────────────────────────────
RUN nvcc --version

# ── JupyterHub single-user + JupyterLab ──────────────────────────
RUN pip install --no-cache-dir --break-system-packages \
        "jupyterhub==4.*" \
        "jupyterlab==4.*" \
        notebook \
        ipywidgets \
        ipykernel

# ── PyTorch with CUDA 12.8 ────────────────────────────────────────
RUN pip install --no-cache-dir --break-system-packages \
        torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu128

# ── flash-attention (compiled with nvcc) ─────────────────────────
RUN pip install --no-cache-dir --break-system-packages \
        packaging ninja && \
    pip install --no-cache-dir --break-system-packages \
        flash-attn --no-build-isolation

# ── Common ML libraries ───────────────────────────────────────────
RUN pip install --no-cache-dir --break-system-packages \
        transformers accelerate datasets peft \
        bitsandbytes sentencepiece \
        pandas numpy matplotlib seaborn scikit-learn \
        tqdm rich

# ── Non-root user matching JupyterHub convention ──────────────────
ARG NB_USER=jovyan
ARG NB_UID=1000
RUN useradd -m -s /bin/bash -N -u ${NB_UID} ${NB_USER}

USER ${NB_USER}
WORKDIR /home/${NB_USER}

CMD ["jupyterhub-singleuser"]
