import json
import os
import re
import requests
import sys
import subprocess
import tarfile

def main(docker_image_to_test):

    # proc = subprocess.Popen(docker_command, shell=True, stdout=subprocess.PIPE)
    # out, err = proc.communicate()
    # docker_image_id = out.decode("utf-8").strip('\n')


    snyk_token = os.getenv('SNYK_TOKEN')
    snyk_org = os.getenv('SNYK_ORG')

    proc = subprocess.Popen("docker pull "+docker_image_to_test, shell=True)
    out, err = proc.communicate()
    # docker_image_id = out.decode("utf-8").strip('\n')
    # print("image")
    # print(docker_image_id)
    # print("end of image")

    # Base snykcli commnad to scan images
    #snykcli_base_command = '/usr/local/bin/snyk-linux test https://github.com/aarlaud-snyk/github-stats'
    snykcli_base_command = 'snyk test --docker '
    snykcli_org_option = ''
    if snyk_org:
        snykcli_org_option = ' --org='+snyk_org

    # Concatenate snykcli executable with options from pipeline variables
    snykcli_exec = ' '\
    .join([snykcli_base_command, docker_image_to_test, snykcli_org_option])

    proc = subprocess.Popen(snykcli_exec, shell=True)
    stdout = proc.communicate()

    #
    #
    # # Execute command pipe stdout to variable and pipe to stdout and use for final exit code for threshold support
    # proc = subprocess.Popen(snykcli_exec, shell=True)
    # proc.communicate()

    if proc.returncode != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])
