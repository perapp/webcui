import pytest
import docker
from docker.types import Mount
import os

@pytest.fixture(scope='session')
def deploy_server():
    """
    A fixture setting up a server to test deployment on.
    The value of the fixture is a docker container object.
    """
    image = "perapp/webcui_deployenv"
    client = docker.from_env()
    container = client.containers.run(image, 
                                      detach=True,
                                      remove=True,
                                      publish_all_ports=True,
                                      labels=["pytest"],
                                      mounts=[Mount("/var/run/docker.sock",
                                                    "/var/run/docker.sock",
                                                    type="bind")],
                                      privileged=True)
    container.reload()

    ports = container.attrs['NetworkSettings']['Ports']
    host_port_map = ports["22/tcp"][0]

    # translate HostIp to $DOCKER_HOST for when running in dind mode (e.g. in Gitlab CI)
    if host_port_map.get("HostIp") == "0.0.0.0" and os.environ.get("DOCKER_HOST"):
        host_port_map["HostIp"] = os.environ.get("DOCKER_HOST")

    print(f"Started {image} on {client.api.base_url} with port mapping: {container.attrs['NetworkSettings']['Ports']}")

    yield container
    container.kill()
