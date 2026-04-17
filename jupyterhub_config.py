import os
import docker

c = get_config()  # noqa: F821

# ── Spawner ───────────────────────────────────────────────────────
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Custom notebook image with CUDA Toolkit (nvcc) + flash-attn
c.DockerSpawner.image = 'jupyterhub-notebook-cuda:latest'
c.DockerSpawner.network_name = os.environ.get('DOCKER_NETWORK_NAME', 'jupyterhub-net')
c.DockerSpawner.remove = True          # Remove container when server stops
c.DockerSpawner.debug = True

# ── Per-user resource limits ─────────────────────────────────────
c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            driver="nvidia",
            count=1,                       # 1 GPU per session
            capabilities=[["gpu"]]
        )
    ],
    "mem_limit": "24g",                    # 24 GB RAM per user
    "memswap_limit": "24g",               # Disable swap on top of RAM
    "shm_size": "4g",                     # Shared memory for DataLoader
}

# ── Persistent storage per user ───────────────────────────────────
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {
    'jupyterhub-user-{username}': notebook_dir
}

# ── Auth ──────────────────────────────────────────────────────────
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.Authenticator.admin_users = {os.environ.get('JUPYTERHUB_ADMIN', 'admin')}
c.NativeAuthenticator.open_signup = False   # Admin must approve new users

# ── Network ───────────────────────────────────────────────────────
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081

# ── DB ────────────────────────────────────────────────────────────
c.JupyterHub.db_url = 'sqlite:////data/jupyterhub.sqlite'
