#!/usr/bin/python

import cgi
import cgitb
import os
import yaml
import jinja2
import codecs
import sys
import re
from commoninclude import print_simple_header, print_simple_footer, print_success, print_error, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backup_config_file = "/opt/nDeploy/conf/backup_config.yaml"
borgmatic_config_file = "/etc/borgmatic/config.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('system_files') and form.getvalue('mysql_backup'):
    system_files = form.getvalue('system_files')
    mysql_backup = form.getvalue('mysql_backup')
    # Check if backup config file is present or initilize otherwise
    if os.path.isfile(backup_config_file):
        # Get all config settings from the backup config file
        with open(backup_config_file, 'r') as backup_config_file_stream:
            yaml_parsed_backupyaml = yaml.safe_load(backup_config_file_stream)
        yaml_parsed_backupyaml['system_files'] = system_files
        yaml_parsed_backupyaml['mysql_backup'] = mysql_backup
        if form.getvalue('backup_path'):
            if not form.getvalue('backup_path').startswith('/'):
                backup_path_pass1 = '/'+form.getvalue('backup_path')
            else:
                backup_path_pass1 = form.getvalue('backup_path')
            if backup_path_pass1.endswith('/'):
                backup_path = backup_path_pass1[:-1]
            else:
                backup_path = backup_path_pass1
            if not backup_path:
                print_error('Error: Invalid backup_path')
                sys.exit(0)
            if not re.match("^[\.0-9a-zA-Z/_-]*$", backup_path):
                print_error("Error: Invalid char in backup_path")
                sys.exit(0)
            yaml_parsed_backupyaml['backup_path'] = backup_path
        else:
            backup_path = yaml_parsed_backupyaml.get('backup_path')
        with open(backup_config_file, 'w') as new_backup_config_file:
            yaml.dump(yaml_parsed_backupyaml, new_backup_config_file, default_flow_style=False)
        # Adjust backup path in borgmatic config file
        if os.path.isfile(borgmatic_config_file):
            with open(borgmatic_config_file, 'r') as borgmatic_conf:
                yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_conf)
            backup_dir_list = yaml_parsed_borgmaticyaml['location']['source_directories']
            backup_dir_list[0] = backup_path
            yaml_parsed_borgmaticyaml['location']['source_directories'] = backup_dir_list
            with open(borgmatic_config_file, 'w') as borgmatic_conf:
                yaml.dump(yaml_parsed_borgmaticyaml, borgmatic_conf, default_flow_style=False)
            os.chmod(borgmatic_config_file, 0o640)
        # We create the borgmatic hook now
        # Initiate Jinja2 templateEnv
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateVars = {"BACKUP_PATH": backup_path,
                        "SYSTEM_FILES": system_files,
                        "MYSQL_BACKUP": mysql_backup
                        }
        borgmatic_hook_template = templateEnv.get_template("borgmatic_cpanel_backup_hook.sh.j2")
        borgmatic_hook_script = borgmatic_hook_template.render(templateVars)
        with codecs.open('/opt/nDeploy/scripts/borgmatic_cpanel_backup_hook.sh', 'w', 'utf-8') as borgmatic_hook_myscript:
            borgmatic_hook_myscript.write(borgmatic_hook_script)
        os.chmod("/opt/nDeploy/scripts/borgmatic_cpanel_backup_hook.sh", 0o755)
        print_success('Backup settings saved')
    else:
        print_error('Backup config error')
else:
    print_forbidden()

print_simple_footer()
