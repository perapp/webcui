#!/usr/bin/python3
from subprocess import CalledProcessError, check_call, PIPE
import sys

if __name__ == "__main__":
    try:
        try:
            check_call(["pipenv", "--venv"], stdout=PIPE, stderr=PIPE)
        except CalledProcessError:
            check_call(["pipenv", "install", "--dev"])

        check_call(["pipenv", "run", "pyb"] + sys.argv[1:])
    except CalledProcessError as err:
        sys.exit(err.returncode)
