import pathlib
import inspect
import toml
from pathlib import Path
import uuid
import tarfile
import tempfile
import string
import os
import textwrap

class App(object):
    def __init__(self, cmd, env=os.environ):
        self.cmd = cmd
        self.env = env
        self._conf = None

    @property
    def name(self):
        return self.project_base_dir.name

    @property
    def conf(self):
        if self._conf is None:
            self.load_conf()
        return self._conf

    def load_conf(self,
                  path: pathlib.Path = None,
                  data: str = None):
        if data is not None:
            self._conf = expand_vars(self.env, toml.loads(data))
            self._conf["__file__"] = None
            return self._conf
        elif path is not None:
            self.load_conf(data=path.read_text())
            self._conf["__file__"] = str(path.resolve())
            return self._conf
        else:
            return self.load_conf(path=self.conf_path)

    @property
    def project_base_dir(self):
        base = self.python_base_dir
        if base.name == "python":
            base = base.parent
        return base

    @property
    def app_file_path(self):
        return pathlib.Path(inspect.getfile(self.cmd)).resolve()

    @property
    def python_base_dir(self):
        base = self.app_file_path.parent
        while (base/"__init__.py").exists():
            base = base.parent
        return base

    @property
    def conf_path(self):
        return self.project_base_dir/"webcui.conf"

    @property
    def python_version(self):
        return self.conf.get("python-version", "latest")

    def build(self, build_file=None):
        if build_file is None:
            build_file = Path(tempfile.gettempdir())/f"{self.name}_{uuid.uuid4()}.tar.gz"

        with tempfile.TemporaryDirectory() as tmp:
            work_dir = Path(tmp)

            docker_file = work_dir/"Dockerfile"
            docker_file.write_text(self.docker_file)

            webcui_dir = pathlib.Path(__file__).parent

            root = pathlib.Path(".")
            ar = tarfile.open(build_file, "x:gz")
            ar.add(self.project_base_dir, root/"app"/self.name)
            ar.add(docker_file, root/"Dockerfile")
            ar.add(webcui_dir, root/"lib"/"webcui")
            ar.add(webcui_dir.parent/"requirements.txt", root/"lib"/"webcui"/"requirements.txt")  # TODO: fix path to req.txt
            ar.close()
        return build_file

    @property
    def docker_file(self):
        python_version = "latest"
        rel_app_file = self.app_file_path.relative_to(self.project_base_dir)
        return textwrap.dedent(f"""
        FROM python:{self.python_version}

        LABEL org.pypi.webcui=""

        ADD lib/webcui/requirements.txt /opt/lib/webcui/
        RUN python -m pip install -r /opt/lib/webcui/requirements.txt
        ADD lib /opt/lib

        ADD app /opt/app
        # RUN python -m pip install -r /opt/app/{self.name}/requirements.txt

        ENV PYTHONPATH /opt/app/{self.name}:/opt/lib
        EXPOSE 80
        CMD python /opt/app/{self.name}/{rel_app_file} run
        """)

def expand_vars(env:dict, xs):
    if isinstance(xs, dict):
        return {x:expand_vars(env, y)
                for x,y in xs.items()}
    elif isinstance(xs, str):
        try:
            return string.Template(xs).substitute(env)
        except KeyError as err:
            raise Exception(f"Variable {err} used in webcui.config not defined as environment variable") from err
    else:
        return xs
