from pybuilder.core import use_plugin, init, task, depends
from pathlib import Path
import json
import functools

use_plugin("python.core")
use_plugin("pypi:pybuilder_pytest")

# use_plugin("python.distutils")

default_task = "package"

@init
def initialize(project):
    project.basepath = Path(project.basedir)
    project.set_property('dir_source_main_python', 'python')

    project.get_property("pytest_extra_args").append("-x")
    project.set_property("dir_source_pytest_python", "test")

@task
@depends("docker")
def compile_sources():
    pass


@task("docker", description="Build Docker images used during testing")
def build_docker_images(project, logger):
    build = functools.partial(build_docker_image, project, logger)
    build(project.basepath/"docker"/"debian.docker")
    build(project.basepath/"docker"/"deployenv.docker")
    
def build_docker_image(project, logger, dockerfile):
    import docker
    from docker import APIClient

    name = f"perapp/webcui_{dockerfile.stem}"
    docker_api = docker.from_env().api
    logger.info(f"Building image {name} from {dockerfile}")
    for line in docker_api.build(path=str(project.basepath),
                                 dockerfile=str(dockerfile),
                                 tag=name):
        entry = json.loads(line)
        try:
            logger.debug(entry["stream"].rstrip())
        except KeyError:
            pass

