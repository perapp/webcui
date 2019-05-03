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

    project.get_property("pytest_extra_args").extend(["-x", "-s", "--tb=native"])
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


#####################

import click
from pathlib import Path
from shutil import rmtree
import docker

home = Path(__file__).parent

@click.group()
def cli():
    pass

@cli.command()
@click.option("--all", is_flag=True, default=False)
def clean(all):
    rmtree(home/"dist")
    for docker.from_env().images.list("webcui"):
        
    if all:
        if os.get("VIRTUAL_ENV"):
            rmtree(os.get("VIRTUAL_ENV"))

logger = logging.getLogger(__name__)

@click.group()
def cli():
    logging.basicConfig()
    logger.setLevel(logging.INFO)

@cli.command()
def build():
    pass

@cli.command()
def test():
    pass

@cli.command()
@click.option("--all", is_flag=True, default=False)
def clean(all):
    clean_dirs(home/"dist")
    clean_docker_images("webcui/*")

    if all:
        clean_dirs(os.get("VIRTUAL_ENV"))

def clean_dirs(pattern):
    if pattern:
        for x in glob.glob(str(pattern)):
            logger.info(f"rm {x}")
            rmtree(dir_to_clean)

def clean_docker_images(pattern):
    for image in docker.from_env().images.list():
        for tag in image.tags:
            if fnmatch.fnmatch(tag, pattern):
                logger.info(f"docker rmi {image}")
                break

if __name__ == "__main__":
    cli()

