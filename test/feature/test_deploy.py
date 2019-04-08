from webcui.deployer import Deployer

def test_deploy(deploy_server):
    host = deploy_server.attrs['NetworkSettings']['IPAddress']
    deployer = Deployer("prod")
    deployer.load_confs(f"""
        [environments]

          [environments.prod]
          host  = "{host}"
          port  = 80
        """)
    deployer.deploy()

if __name__ == "__main__":
  import pytest
  pytest.main(["test/feature/test_deploy.py"])
