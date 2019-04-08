import paramiko
from paramiko.pkey import PKey
import pathlib
import toml

class Deployer(object):

    def __init__(self, env_name):
        self.env_name = env_name
        self._conf = None

    def deploy(self):
        self.build()
        ssh = paramiko.SSHClient()
        ssh.connect(self.env_conf["host"],
                    pkey=self.pkey)

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

    def set_conf_data(self, data: str):
        self._conf = toml.loads(data)

    def set_pkey_data(self, data: str):
        self.pkey = PKey(data=data)
