#!/usr/bin/python3
"""
Create venv and bootstrap with:
 * .pth file to python dirs (not for deploy test env)
 * bin directory for Windows env (in order to use the same Makefile on Windows)
"""
import sys
assert sys.version_info >= (3,6)

from pathlib import Path
import venv
import os
import subprocess

def home_path():
    return Path(__file__).parent.parent.parent

def pyvenv_path(stage):
    return home_path()/"build"/"env"/stage

def run_python(stage, *args, quiet=False):
    kwargs = {}
    if quiet:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    exe = Path("Scripts")/"python.exe" if sys.platform == 'win32' else Path("bin")/"python"
    return subprocess.run([str(pyvenv_path(stage)/exe)] + list(args), **kwargs).returncode == 0

def cmd(argv):
    if len(argv) > 1:
        stage = argv[1]
    else:
        stage = "build"

    envpath = pyvenv_path(stage)
    if not envpath.exists():
        print(f"Creating {stage} venv...")
        envb = venv.EnvBuilder(with_pip=True)
        envb.create(str(envpath))

        if "pypi" not in stage:
            if sys.platform == 'win32':
                libpath = envpath/"Lib"/"site-packages"
                (libpath/"webcui.pth").write_text("..\\..\\..\\..\\..\\python\n")
            else:
                libpath = envpath/"lib"/("python%d.%d" % sys.version_info[:2])/"site-packages"
                (libpath/"webcui.pth").write_text("../../../../../../python\n")

        run_python(stage,
                   "-m", "pip", "install", "--upgrade", "pip")
        run_python(stage,
                   "-m", "pip", "install", "--upgrade",
                   "-r", str(home_path()/"python"/"requirements-dev.txt"),
                   "-r", str(home_path()/"python"/"requirements.txt"))

if __name__ == "__main__":
    cmd(sys.argv)
