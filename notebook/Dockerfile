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

# ── Step 1: System packages ───────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-dev python3-pip python3-venv \
        git curl wget build-essential ca-certificates \
        libssl-dev libffi-dev \
    && ln -sf python3 /usr/bin/python \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Step 2: Remove PEP 668 guard (MUST come before any pip call) ─
# Ubuntu 24.04 marks Python as "externally managed" to protect the OS.
# Inside a Docker container this restriction serves no purpose.
# Removing the marker lets pip install packages without flags or venvs.
RUN rm -f /usr/lib/python3*/EXTERNALLY-MANAGED
# NOTE: do NOT run `pip install --upgrade pip` — the Debian-installed
# pip has no RECORD file and cannot uninstall itself. pip 24.0 is
# sufficient for everything below.

# ── Step 3: Verify nvcc is present ───────────────────────────────
RUN nvcc --version

# ── Step 4: JupyterHub + JupyterLab ──────────────────────────────
RUN pip install --no-cache-dir \
        "jupyterhub==4.*" \
        "jupyterlab==4.*" \
        notebook \
        ipywidgets \
        ipykernel

# ── Step 5: PyTorch ───────────────────────────────────────────────
# cu128 wheels are ABI-compatible with CUDA 13.x runtime.
# Switch to cu132 index-url once PyTorch releases those wheels.
RUN pip install --no-cache-dir \
        torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu128

# ── Step 6: flash-attention (compiled by nvcc at build time) ──────
RUN pip install --no-cache-dir packaging ninja && \
    pip install --no-cache-dir flash-attn --no-build-isolation

# ── Step 7: Common ML libraries ───────────────────────────────────
RUN pip install --no-cache-dir \
        transformers accelerate datasets peft \
        bitsandbytes sentencepiece \
        pandas numpy matplotlib seaborn scikit-learn \
        tqdm rich

# ── Step 8: Non-root user (JupyterHub convention) ─────────────────
ARG NB_USER=jovyan
ARG NB_UID=1000
RUN useradd -m -s /bin/bash -N -u ${NB_UID} ${NB_USER}

USER ${NB_USER}
WORKDIR /home/${NB_USER}

CMD ["jupyterhub-singleuser"]
