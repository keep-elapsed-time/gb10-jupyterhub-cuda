# ─────────────────────────────────────────────────────────────────
# Custom JupyterHub single-user notebook image
# CUDA 13.2.0 devel (nvcc) + Ubuntu 24.04 (Python 3.12)
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

# ── Step 2: Remove PEP 668 guard (safe in Docker) ────────────────
RUN rm -f /usr/lib/python3*/EXTERNALLY-MANAGED

# ── Step 3: Verify nvcc ───────────────────────────────────────────
RUN nvcc --version

# ── Step 4: JupyterHub + JupyterLab ──────────────────────────────
RUN pip install --no-cache-dir \
        "jupyterhub==4.*" \
        "jupyterlab==4.*" \
        notebook \
        ipywidgets \
        ipykernel

# ── Step 5: PyTorch cu132 (matches CUDA 13.2 nvcc) ───────────────
RUN pip install --no-cache-dir \
        torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu132 \
    || pip install --no-cache-dir \
        torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/nightly/cu130

RUN python3 -c "import torch; print('torch:', torch.__version__, '| cuda:', torch.version.cuda)"

# ── Step 6: flash-attention ───────────────────────────────────────
ENV MAX_JOBS=4
RUN pip install --no-cache-dir packaging ninja && \
    pip install --no-cache-dir flash-attn --no-build-isolation

# ── Step 7: Common ML libraries ───────────────────────────────────
RUN pip install --no-cache-dir \
        transformers accelerate datasets peft \
        bitsandbytes sentencepiece \
        pandas numpy matplotlib seaborn scikit-learn \
        tqdm rich

# ── Step 8: Non-root user ─────────────────────────────────────────
# nvidia/cuda Ubuntu images already occupy UID 1000 (ubuntu user).
# Rename it to jovyan so JupyterHub's volume mapping works correctly.
ARG NB_USER=jovyan
RUN existing=$(getent passwd 1000 | cut -d: -f1); \
    if [ -n "$existing" ]; then \
        usermod -l ${NB_USER} "$existing" && \
        usermod -d /home/${NB_USER} -m ${NB_USER} && \
        groupmod -n ${NB_USER} "$existing" 2>/dev/null || true; \
    else \
        useradd -m -s /bin/bash -N -u 1000 ${NB_USER}; \
    fi

USER ${NB_USER}
WORKDIR /home/${NB_USER}

CMD ["jupyterhub-singleuser"]
