#!/usr/bin/python3

import googleapiclient


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

