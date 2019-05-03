from pathlib import Path
import docker
from docker import APIClient
import json

def build_docker_images():
    projdir = Path(__file__).parent.parent
    build_docker_image(projdir, projdir/"docker"/"debian.docker")
    build_docker_image(projdir, projdir/"docker"/"deployenv.docker")

def build_docker_image(projdir, dockerfile):
    name = f"perapp/webcui_{dockerfile.stem}"
    docker_api = docker.from_env().api
    print(f"Building image {name} from {dockerfile}")
    for line in docker_api.build(path=str(projdir),
                                 dockerfile=str(dockerfile),
                                 tag=name):
        entry = json.loads(line)
        try:
            print(entry["stream"].rstrip())
        except KeyError:
            pass

if __name__ == "__main__":
    build_docker_images()
