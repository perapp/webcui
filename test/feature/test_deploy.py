import webcui
from pathlib import Path

def test_deploy(deploy_server):
    import pprint
    pprint.pprint(deploy_server.attrs)
    host = deploy_server.attrs['NetworkSettings']['IPAddress']
    print("TEST DEPLOY on", host)
    src_file = Path(__file__).parent.parent/"example"/"basic"/"cmd.py"
    app_code = compile(src_file.read_bytes(), src_file, "exec")
    app_vars = {}
    exec(app_code, app_vars)
    webcui.run(app_vars["cmd"],
               ["deploy"],
               env={"HOST": host,
                    "USER": "webcui",
                    "PASSWORD": "webcui"},
               standalone_mode=False)

