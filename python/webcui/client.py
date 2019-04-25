import click
from click.testing import CliRunner
from .server import Server
from .deployer import Deployer
from .app import App
import os

class Client(object):

    def __init__(self, cmd, env):
        self.app = App(cmd, env)

    def run(self):
        Server(app=self.app).run()

    def build(self):
        """
        Build Webcui app as a tar archive ready to be uploaded to a remote site and deployed.
        Used for testing and debugging.
        """
        return self.app.build()

    def deploy(self):
        return Deployer(self.app, "prod").deploy()
        
def run(cmd, args=None, env=os.environ, standalone_mode=True):
    client = Client(cmd, env)

    @click.group()
    def cli():
        pass

    @cli.command()
    def run():
        """
        Run app on the local computer.
        """
        client.run()

    @cli.command()
    def build():
        """
        Build app as a tar archive.
        """
        print(client.build())

    @cli.command()
    def deploy():
        """
        Build, upload and deploy app to remote server.
        """
        print(client.deploy())

    return cli(args, standalone_mode=standalone_mode)
