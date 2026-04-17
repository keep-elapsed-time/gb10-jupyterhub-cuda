# ─────────────────────────────────────────────────────────────────
# Custom JupyterHub single-user notebook image
# CUDA Toolkit devel (includes nvcc) for GB10 Blackwell
#
# CUDA >= 12.8 required for Blackwell (GB10).
# Update CUDA_VER below when CUDA 13.x is publicly available.
# ─────────────────────────────────────────────────────────────────
ARG CUDA_VER=12.8.1
ARG UBUNTU_VER=22.04

FROM nvidia/cuda:${CUDA_VER}-devel-ubuntu${UBUNTU_VER}

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/cuda/bin:${PATH}" \
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# ── System dependencies ───────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.11 python3.11-dev python3-pip python3.11-venv \
        git curl wget build-essential ca-certificates \
        libssl-dev libffi-dev \
    && ln -sf python3.11 /usr/bin/python3 \
    && ln -sf python3 /usr/bin/python \
    && pip install --upgrade pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Confirm nvcc is available ─────────────────────────────────────
RUN nvcc --version

# ── JupyterHub single-user + JupyterLab ──────────────────────────
RUN pip install --no-cache-dir \
        jupyterhub==4.* \
        jupyterlab==4.* \
        notebook \
        ipywidgets \
        ipykernel

# ── PyTorch (CUDA 12.8) ───────────────────────────────────────────
# Update index-url when PyTorch releases cu130 builds
RUN pip install --no-cache-dir \
        torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu128

# ── flash-attention (compiled with nvcc in image) ─────────────────
RUN pip install --no-cache-dir packaging ninja && \
    pip install --no-cache-dir flash-attn --no-build-isolation

# ── Common ML libraries ───────────────────────────────────────────
RUN pip install --no-cache-dir \
        transformers accelerate datasets peft \
        bitsandbytes sentencepiece \
        pandas numpy matplotlib seaborn scikit-learn \
        tqdm rich

# ── Non-root user (matches JupyterHub convention) ─────────────────
ARG NB_USER=jovyan
ARG NB_UID=1000
RUN useradd -m -s /bin/bash -N -u ${NB_UID} ${NB_USER}

USER ${NB_USER}
WORKDIR /home/${NB_USER}

# ── Default start command (jupyterhub-singleuser) ─────────────────
CMD ["jupyterhub-singleuser"]
