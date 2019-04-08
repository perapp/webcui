from webcui.deployer import Deployer
import tarfile
import io

def test_deploy(deploy_server):
    host = deploy_server.attrs['NetworkSettings']['IPAddress']
    deployer = Deployer("prod")
    deployer.set_conf_data(f"""
        [environments]

          [environments.prod]
          host  = "{host}"
          port  = 80
        """)
    deployer.set_pkey_data(read_file(deploy_server, "/root/.ssh/id_rsa"))
    deployer.deploy()

def read_file(container, path):
  tar_data = next(container.get_archive(path)[0])
  with tarfile.open(fileobj=io.BytesIO(tar_data)) as tarobj:
      return tarobj.next().tobuf()

if __name__ == "__main__":
  import pytest
  pytest.main(["test/feature/test_deploy.py"])
