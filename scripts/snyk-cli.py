import json
import os
import re
import requests
import sys
import subprocess
import tarfile

def main(docker_image_to_test):
    snyk_token = os.getenv('SNYK_TOKEN')
    snyk_org = os.getenv('SNYK_ORG')
    cfcr_account=os.getenv('CFCR_ACCOUNT')
    cf_user_name=os.getenv('CF_USER_NAME')
    CFCR_LOGIN_TOKEN=os.getenv('CFCR_LOGIN_TOKEN')

    docker_image_name=docker_image_to_test

    if cfcr_account != "" and (cf_user_name == "" or CFCR_LOGIN_TOKEN == ""):
        raise ValueError('If logging in codefresh registry, you must provide username and login token')
        sys.exit(1)

    docker_command="docker pull "+docker_image_to_test;
    if cfcr_account!= "":
        docker_login="docker login r.cfcr.io -u "+cf_user_name+" -p "+CFCR_LOGIN_TOKEN
        proc = subprocess.Popen(docker_login, shell=True)
        out, err = proc.communicate()
        docker_command="docker pull r.cfcr.io/"+cfcr_account+"/"+docker_image_to_test;
        docker_image_name="r.cfcr.io/"+cfcr_account+"/"+docker_image_to_test;

    proc = subprocess.Popen(docker_command, shell=True)
    out, err = proc.communicate()
    
    # Base snykcli commnad to scan images
    snykcli_base_command = 'snyk test --docker '
    snykcli_org_option = ''
    if snyk_org:
        snykcli_org_option = ' --org='+snyk_org

    # Concatenate snykcli executable with options from pipeline variables
    snykcli_exec = ' '\
    .join([snykcli_base_command, docker_image_name, snykcli_org_option])

    proc = subprocess.Popen(snykcli_exec, shell=True)
    stdout = proc.communicate()

    if proc.returncode == 0:
        # Monitor snykcli commnad to scan images
        snykcli_monitor_command = 'snyk monitor --docker '
        snykcli_org_option = ''
        if snyk_org:
            snykcli_org_option = ' --org='+snyk_org

        # Concatenate snykcli executable with options from pipeline variables
        snykcli_exec = ' '\
        .join([snykcli_monitor_command, docker_image_to_test, snykcli_org_option])

        proc = subprocess.Popen(snykcli_exec, shell=True)
        stdout = proc.communicate()


    if proc.returncode != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])
