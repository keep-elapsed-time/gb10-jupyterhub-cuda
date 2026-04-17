#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# migrate.sh — Copy data from old jupyter-notebook container to
#              a JupyterHub user volume.
#
# Usage:
#   bash scripts/migrate.sh <target_username>
#
# Example:
#   bash scripts/migrate.sh admin
#
# What it does:
#   1. Copies /home/jovyan/* from the old container (jupyter-notebook)
#      to a local ./backup/ directory.
#   2. Creates (or reuses) the Docker volume jupyterhub-user-<username>.
#   3. Loads the backup into that volume via a temporary busybox container.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

OLD_CONTAINER="${OLD_CONTAINER:-jupyter-notebook}"
TARGET_USER="${1:-admin}"
VOLUME_NAME="jupyterhub-user-${TARGET_USER}"
BACKUP_DIR="$(pwd)/backup/${TARGET_USER}"

echo "==> Source container : ${OLD_CONTAINER}"
echo "==> Target user      : ${TARGET_USER}"
echo "==> Target volume    : ${VOLUME_NAME}"
echo "==> Local backup dir : ${BACKUP_DIR}"
echo ""

# ── Step 1: Copy from old container to local backup ───────────────
echo "[1/3] Copying from container ${OLD_CONTAINER}:/home/jovyan/ ..."
mkdir -p "${BACKUP_DIR}"
docker cp "${OLD_CONTAINER}:/home/jovyan/." "${BACKUP_DIR}/"
echo "      Done. Files:"
ls -lh "${BACKUP_DIR}"
echo ""

# ── Step 2: Create target volume if it doesn't exist ──────────────
echo "[2/3] Ensuring volume ${VOLUME_NAME} exists ..."
docker volume create "${VOLUME_NAME}" || true
echo ""

# ── Step 3: Load backup into volume ───────────────────────────────
echo "[3/3] Loading data into volume ${VOLUME_NAME} ..."
docker run --rm \
    -v "${BACKUP_DIR}:/source:ro" \
    -v "${VOLUME_NAME}:/dest" \
    busybox sh -c "cp -a /source/. /dest/ && chown -R 1000:100 /dest"
echo ""

echo "==> Migration complete!"
echo "    Start JupyterHub, log in as '${TARGET_USER}', and your files"
echo "    will be in /home/jovyan/work/"
