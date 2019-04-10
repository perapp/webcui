import paramiko
from paramiko.rsakey import RSAKey
from paramiko.client import AutoAddPolicy
import pathlib
import toml

class Deployer(object):

    def __init__(self, env_name):
        self.env_name = env_name
        self._conf = None

    def deploy(self):
        self.build()
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy)
        ssh.connect(self.env_conf["host"],
                    username=self.env_conf.get("username"),
                    password=self.env_conf.get("password"))

    def build(self):
        pass
    
    def validate_build(self):
        if not self.build_path.exists():
            self.build()
        return self.build_path
    
    @property
    def build_path(self):
        return pathlib.Path(".")

    @property
    def conf(self):
        if self._conf is None:
            raise Exception("TODO: Conf should be loaded here")
        return self._conf

    @property
    def env_conf(self):
        try:
            return self.conf["environments"][self.env_name]
        except KeyError:
            raise Exception(f"No environment called '{self.env_name}' defined in {self.conf_path}")

    @property
    def conf_path(self):
        return pathlib.Path("./webcui.conf") # TODO:

    def load_conf(self,
                  path: pathlib.Path = None,
                  data: str = None):
        if data is not None:
            self._conf = toml.loads(data)
            return self.conf
        elif path is not None:
            return self.load_conf(data=path.read_text())
        else:
            return self.load_conf(path=self.conf_path)
            