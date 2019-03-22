#!/usr/bin/python3
from pathlib import Path
import venv
import os
import sys
import subprocess

def home_path():
    return Path(__file__).parent.parent

def pyenv_path():
    return home_path()/"build"/"pyenv"

def run_python(*args, quiet=False):
    kwargs = {}
    if quiet:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    return subprocess.run([str(pyenv_path()/"bin/python")] + list(args), **kwargs).returncode == 0

def cmd():
    if not pyenv_path().exists():
        print("Creating venv...")
        envb = venv.EnvBuilder(with_pip=True)
        envb.create(str(pyenv_path()))

    if not run_python("-c", "import pymake", quiet=True):
        print("Installing py-make...")
        run_python("-m", "pip", "install", "py-make")
    #run_python("-c", "import sys; import pymake3; import os; print(os.getcwd()); del sys.argv[0]; pymake3.pymake3()", *sys.argv)
    run_python("-m", "pymake", *sys.argv[1:])

if __name__ == "__main__":
    cmd()
