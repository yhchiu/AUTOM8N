#!/usr/bin/env python


import sys
import subprocess
import os
import pwd
import grp
import shutil
try:
    import simplejson as json
except ImportError:
    import json
from commoninclude import sighupnginx


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# This hook script is supposed to be called after account creation by cPanel
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
# Loading the json in on stdin send by cPanel
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
cpaneldomain = mydict["domain"]
hostingplan = mydict["plan"]
hostingplan_filename = hostingplan.encode('utf-8').replace(" ", "_")
domain_data_file = installation_path+"/domain-data/"+cpaneldomain
if not os.path.isfile(domain_data_file):
    if hostingplan_filename == 'undefined' or hostingplan_filename == 'default':
        if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
        else:
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
    else:
        if os.path.isfile(installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"):
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"
        else:
            if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
            else:
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
    if os.path.isfile(TEMPLATE_FILE):
        shutil.copyfile(TEMPLATE_FILE, domain_data_file)
        cpuser_uid = pwd.getpwnam(cpaneluser).pw_uid
        cpuser_gid = grp.getgrnam(cpaneluser).gr_gid
        os.chown(domain_data_file, cpuser_uid, cpuser_gid)
        os.chmod(domain_data_file, 0o660)
user_shell = pwd.getpwnam(cpaneluser).pw_shell
# If nDeploy cluster is enabled we need to add users,DNS entry for the same
if os.path.exists(cluster_config_file):
    cpaneluserhome = mydict["homedir"]
    # Calling ansible ad-hoc command to create users across the cluster
    # Using subprocess.call here as we are not in a hurry and no async call is required
    subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpaneluser+' home='+cpaneluserhome+' shell='+user_shell+'"', shell=True)
    if os.path.isfile(installation_path+"/conf/skip_geodns"):
        subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpaneluser, shell=True)
    else:
        subprocess.call(installation_path + "/scripts/cluster_gdnsd_ensure_user.py "+cpaneluser, shell=True)
    subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
    sighupnginx()
    print("1 nDeploy:clusteraccountcreate:"+cpaneluser)
else:
    # We just need to generate config for the local machine
    subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
    sighupnginx()
    print("1 nDeploy:accountcreate:"+cpaneluser)
