import os
import docker

c = get_config()  # noqa: F821

# ── Spawner ───────────────────────────────────────────────────────
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = 'jupyterhub-notebook-cuda:latest'
c.DockerSpawner.network_name = os.environ.get('DOCKER_NETWORK_NAME', 'jupyterhub-net')
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

# ── Per-user resource limits ──────────────────────────────────────
c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            driver="nvidia",
            count=1,
            capabilities=[["gpu"]]
        )
    ],
    "mem_limit": "24g",
    "memswap_limit": "24g",
    "shm_size": "4g",
}

# ── Persistent storage per user ───────────────────────────────────
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {
    'jupyterhub-user-{username}': notebook_dir
}

# ── Auth ──────────────────────────────────────────────────────────
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

ADMIN = os.environ.get('JUPYTERHUB_ADMIN', 'admin')
c.Authenticator.admin_users = {ADMIN}
# allowed_users must include admin — otherwise NativeAuthenticator
# blocks even admin after signup ("not authorized yet")
c.Authenticator.allowed_users = {ADMIN}

c.NativeAuthenticator.open_signup = False   # Admin approves new users at /hub/authorize

# ── Network ───────────────────────────────────────────────────────
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081
c.JupyterHub.cookie_secret_file = '/data/jupyterhub_cookie_secret'

# ── DB ────────────────────────────────────────────────────────────
c.JupyterHub.db_url = 'sqlite:////data/jupyterhub.sqlite'
