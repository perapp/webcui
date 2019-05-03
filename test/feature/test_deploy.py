import webcui
from pathlib import Path
import tempfile
import shutil
import toml
import pprint

def test_deploy(deploy_server):
    app_name = "basic"
    app_dir = Path(__file__).parent.parent/"example"/"basic"

    # make a temp copy of the app to modify the config file
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        shutil.copytree(app_dir, tmp_dir/app_name)
        app_dir = tmp_dir/app_name

        #ssh_port_map = deploy_server.attrs['NetworkSettings']['Ports']["22/tcp"][0]
        #ssh_host = ssh_port_map["HostIp"]
        #ssh_port = ssh_port_map["HostPort"]

        ssh_host = deploy_server.attrs['NetworkSettings']["IPAddress"]
        ssh_port = 22
        print(f"Test deploy on Docker container {ssh_host}:{ssh_port}")

        conf = toml.load(app_dir/"webcui.conf")
        conf["environments"]["prod"]["host"] = ssh_host
        conf["environments"]["prod"]["ssh_port"] = ssh_port
        with (app_dir/"webcui.conf").open(mode="w") as fileobj:
            toml.dump(conf, fileobj)
        print("Updated test webcui conf:")
        pprint.pprint(conf)

        cmd = get_cmd_from_file(app_dir/"cmd.py", "cmd")
        webcui.run(cmd,
               ["deploy"],
               env={"HOST": ssh_host,
                    "USER": "webcui",
                    "PASSWORD": "webcui"},
               standalone_mode=False)

def get_cmd_from_file(src_file, func_name):
        app_code = compile(src_file.read_bytes(), src_file, "exec")
        app_vars = {}
        exec(app_code, app_vars)
        return app_vars[func_name]
