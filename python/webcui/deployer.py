import paramiko
from paramiko.rsakey import RSAKey
from paramiko.client import AutoAddPolicy
import pathlib
from subprocess import CalledProcessError
import tempfile
import selectors
import sys
import os
from pathlib import Path, PosixPath

class Deployer(object):

    def __init__(self, app, env_name):
        self.app = app
        self.env_name = env_name
        self.build_dir = tempfile.TemporaryDirectory()

    def deploy(self):
        build = self.app.build()
        self.validate_docker()
        remote_build = self.upload_build(build)
        image = self.build_docker_image(remote_build)
        self.restart_env(image)

    def restart_env(self, image):
        with self.connect() as ssh:
            # TODO: stop running env
            ssh.run(f'docker run --rm -d "{image}"')

    def upload_build(self, build_path):
        with self.connect() as ssh:
            sftp = ssh.open_sftp()
            remote_build_path = PosixPath(f"/var/tmp/{build_path.name}")
            print(f"put {build_path} {remote_build_path}")
            sftp.put(str(build_path), str(remote_build_path))
            return remote_build_path

    def build_docker_image(self, remote_build_path):
        with self.connect() as ssh:
            tarx_dir = remote_build_path.with_suffix(".d")
            ssh.run(f'mkdir -p "{tarx_dir}"')
            ssh.run(f'tar -C "{tarx_dir}" -xaf "{remote_build_path}"')
            tag = self.app.name
            ssh.run(f'docker build -t "{tag}" -f "{tarx_dir}/Dockerfile" "{tarx_dir}"')  # TODO: Tag with version
            return tag

    def validate_docker(self):
        with self.connect() as ssh:
            try:
                ssh.run("docker version")
            except CalledProcessError:
                self.install_docker()
            ssh.run("docker run hello-world")

    def install_docker(self):
        with self.connect() as ssh:
            try:
                ssh.run('echo $USER')
                ssh.run('sudo true')
            except CalledProcessError as e:
                raise Exception("No sudo access. Deploying requires sudo access. Add sudo access to user") from e

            ssh.run('sudo apt-get update')
            ssh.run('sudo apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common')
            ssh.run('curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -')
            ssh.run('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"')
            ssh.run('sudo apt-get update')
            ssh.run('sudo apt-get -y install docker-ce docker-ce-cli containerd.io')

    def connect(self):
        ssh = MySSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy)
        ssh.connect(self.env_conf["host"],
                    port=int(self.env_conf.get("ssh_port", "22")),
                    username=self.env_conf.get("username"),
                    password=self.env_conf.get("password"))
        return ssh

    @property
    def env_conf(self):
        try:
            return self.app.conf["environments"][self.env_name]
        except KeyError:
            raise Exception(f"No environment called '{self.env_name}' defined in {self.app.conf.__file__}")

class MySSHClient(paramiko.SSHClient):
    def run(self, cmd):
        print(f"$ {cmd}")
        stdin, stdout, stderr = self.exec_command(cmd) 
        ch = stdout.channel
        sel = selectors.DefaultSelector()

        def read_stdout(fileobj, mask):
            if ch.recv_stderr_ready():
                sys.stderr.write(ch.recv_stderr(1).decode("utf-8"))
            elif ch.recv_ready():
                sys.stdout.write(ch.recv(1).decode("utf-8"))
        
        sel.register(stdout.channel.fileno(), selectors.EVENT_READ, read_stdout)

        while not ch.closed:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
        exit_status = ch.recv_exit_status()
        if exit_status != 0:
            raise CalledProcessError(exit_status, cmd)
