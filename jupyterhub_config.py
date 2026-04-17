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

ADMIN = os.environ.get('JUPYTERHUB_ADMIN', 'aifintech')
c.Authenticator.admin_users = {ADMIN}
c.Authenticator.allowed_users = {ADMIN}
c.NativeAuthenticator.open_signup = False

# ── Network ───────────────────────────────────────────────────────
# PUBLIC_URL: the URL users type in the browser (host machine IP/hostname).
# Must match exactly — cookies are scoped to this origin.
# Set via environment variable so it's easy to change without editing this file.
PUBLIC_HOST = os.environ.get('JUPYTERHUB_PUBLIC_HOST', '192.168.21.3')
PUBLIC_PORT = os.environ.get('JUPYTERHUB_PUBLIC_PORT', '8000')
c.JupyterHub.bind_url = f'http://{PUBLIC_HOST}:{PUBLIC_PORT}'

# Hub API: bind to all interfaces; spawned containers reach hub by container name
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081

c.JupyterHub.cookie_secret_file = '/data/jupyterhub_cookie_secret'
c.JupyterHub.db_url = 'sqlite:////data/jupyterhub.sqlite'
