import pytest
import docker
from docker.types import Mount

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
    
    yield container
    container.kill()
