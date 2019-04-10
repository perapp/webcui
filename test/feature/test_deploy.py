from webcui.deployer import Deployer
import tarfile
import io

def test_deploy(deploy_server):
    host = deploy_server.attrs['NetworkSettings']['IPAddress']
    deployer = Deployer("prod")
    deployer.load_conf(data=f"""
        [environments]

          [environments.prod]
          host  = "{host}"
          port  = 80
          username = "webcui"
          password = "webcui"
        """)
    deployer.deploy()

def read_file(container, path):
  tar_data = next(container.get_archive(path)[0])
  with tarfile.open(fileobj=io.BytesIO(tar_data)) as tarobj:
      return tarobj.extractfile(tarobj.next()).read()

if __name__ == "__main__":
  import pytest
  pytest.main(["--pdb", __file__])
