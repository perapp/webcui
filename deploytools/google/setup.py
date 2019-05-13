#!/usr/bin/python3
import subprocess

PROJ_NAME = "webcuiproj2"
NODE_NAME = "webcui"

def run():
    if not test_gcloud("projects", "describe", PROJ_NAME):
        gcloud("projects", "create", PROJ_NAME)
    gcloud("config", "set", "project", PROJ_NAME)
    gcloud("config", "set", "compute/zone", "us-east1-c")

    try:
        gcloud("services", "enable", "compute.googleapis.com")
    except:
        print("Could not enable compute.googleapis.com service for your project. Usually you need to enable billing to continue.")
        print(f"Please do so by following this link: https://console.developers.google.com/billing?project={PROJ_NAME}")
        return

    if not test_gcloud("compute", "instances", "describe", NODE_NAME):
        gcloud("compute", "instances", "create", NODE_NAME,
               "--machine-type=f1-micro",
               "--tags=http-server,https-server"
               "--metadata=ssh-keys=per:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6HL/Q198U+qO9io8AWPzggD5o9PjgZD5bV3OOXLW+vBR3PQL8OmQabjpMkbeE0CV8xACMfa8ARYzNBAtaUaPs01LqTpcJdI/EztALqS0bNq+l1Fvo7VVE83f2vp6df2CCS6Ixds3G61UIsJki7TVa1pnK389d6sFJwGSksvzGZrs5IhXwpXnRm4Iogb9YW1UJsp4Fbd7cMCz3ln3LvsIB3pBGdbTvuLwBdxu2Kvck2YhfybZcmHpNN8PnIApdcgAZ+se9Bv77EYx35Kz5aQJEnfBA4XHjc7kXLjRhK8z+rOaJPi4Gij3l6MhvaNSckmw1Cj3iG51Xvnh/eygvAtR5 per@dev-small")

        
def gcloud(*args):
    p = subprocess.run(["gcloud"] + list(args), check=True)
    return p.stdout


def test_gcloud(*args):
    return subprocess.run(["gcloud"] + list(args),
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).returncode == 0

if __name__ == "__main__":
    run()

"""

def run():
    
    gcloud projects create webcuiproj
    gcloud config set project webcuiproj
    https://console.developers.google.com/billing/linkedaccount?project=webcuiproj
    gcloud services enable compute.googleapis.com

gcloud compute instances create webcui --machine-type=f1-micro \
   --image-project=coreos-cloud --image-family=coreos-stable \
   --zone=us-east1-c \
   --tags=http-server,https-server \
   --metadata=ssh-keys="per:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6HL/Q198U+qO9io8AWPzggD5o9PjgZD5bV3OOXLW+vBR3PQL8OmQabjpMkbeE0CV8xACMfa8ARYzNBAtaUaPs01LqTpcJdI/EztALqS0bNq+l1Fvo7VVE83f2vp6df2CCS6Ixds3G61UIsJki7TVa1pnK389d6sFJwGSksvzGZrs5IhXwpXnRm4Iogb9YW1UJsp4Fbd7cMCz3ln3LvsIB3pBGdbTvuLwBdxu2Kvck2YhfybZcmHpNN8PnIApdcgAZ+se9Bv77EYx35Kz5aQJEnfBA4XHjc7kXLjRhK8z+rOaJPi4Gij3l6MhvaNSckmw1Cj3iG51Xvnh/eygvAtR5 per@dev-small"

"""
