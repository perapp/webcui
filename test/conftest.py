import pytest
import docker

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
                                      labels=["pytest"],
                                      publish_all_ports=True,
                                      remove=True,
                                      privileged=True)
    container.reload()
    
    yield container
    container.kill()
