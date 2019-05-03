import pytest
import docker
from docker.types import Mount
import os
from urllib.parse import urlparse

@pytest.fixture(scope='session')
def deploy_server():
    """
    A fixture setting up a server to test deployment on.
    The value of the fixture is a docker container object.
    """
    prefix = os.environ.get("DOCKER_PREFIX", "")
    image = f"{prefix}deployenv
    print(image)
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

    #ports = container.attrs['NetworkSettings']['Ports']
    #host_port_map = ports["22/tcp"][0]

    # translate HostIp to $DOCKER_HOST for when running in dind mode (e.g. in Gitlab CI)
    #docker_host = urlparse(os.environ.get("DOCKER_HOST")).hostname
    #if docker_host and host_port_map.get("HostIp") == "0.0.0.0":
    #    host_port_map["HostIp"] = docker_host

    print(f"Started {image} on {client.api.base_url} with port mapping: {container.attrs['NetworkSettings']['Ports']}")
    yield container
    container.kill()
