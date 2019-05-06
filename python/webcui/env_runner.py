import docker
from docker.types import Mount
from pathlib import Path

client = docker.from_env()
image = "nginx"

build = Path("c:\\work")
env = "prod"
port = 80

try:
    client.images.get(image)
except docker.errors.ImageNotFound:
    print(f"Pulling image {image}")
    client.images.pull(image)

if client.containers.list():
    print("Currently running containers:")
    print("Image Name Labels")
    for c in client.containers.list():
        envs = ", ".join([x[7:] for x in c.labels
                          if x.startswith("webcui_")])
        print(f"{c.image.tags[0]} {c.short_id} {envs}")
 
for c in client.containers.list(filters={"label": f"webcui_{env}"}):
    print(f"Stopping {env} container {c.name}, {c.short_id}")
    c.stop()
print(f"Starting {env} container...")
client.containers.run(image, 
                      detach=True,
                      labels=["webcui", f"webcui_{env}"],
                      ports={80: port}, # TODO: Change to 8080
                      mounts=[Mount(target="/app",
                                    source=str(build),
                                    type="bind")],
                      remove=True)
print("done")
