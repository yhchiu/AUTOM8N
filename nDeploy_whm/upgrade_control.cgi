#!/bin/python

import commoninclude
import cgi
import cgitb
import os
import subprocess


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()
#&& ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy upgrade *nDeploy*\"
form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('upgrade_control'):

    if form.getvalue('upgrade_control') == 'check':
        subprocess.Popen(installation_path+'/scripts/check_for_updates.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('Checking for updates!')
    elif form.getvalue('upgrade_control') == 'reinstall':
        if os.path.isfile(cluster_config_file):
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy reinstall *nDeploy* && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy reinstall *nDeploy*\"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy reinstall *nDeploy*', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('<ul class="shelloutput">')
        print('    <li><b>Reinstalling Application:</b></li>')
    elif form.getvalue('upgrade_control') == 'upgrade':
        if os.path.isfile(cluster_config_file):
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy upgrade *nDeploy* && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy upgrade *nDeploy*\" && '+installation_path+'/scripts/attempt_autofix.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy upgrade *nDeploy* && '+installation_path+'/scripts/attempt_autofix.sh && nginx -t && needs-restarting | grep nginx && service nginx restart', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('<ul class="shelloutput">')
        print('    <li><b>Upgrading Application:</b></li>')

    if form.getvalue('upgrade_control') == 'reinstall' or form.getvalue('upgrade_control') == 'upgrade':
        print('    <li>&nbsp;</li>')
        for line in iter(procExe.stdout.readline, b''):
            print('    <li>'+line.rstrip()+'</li>')
        print('    <li>&nbsp;</li>')
        print('    <li><b>Application maintenance completed!</b></li>')
        print('</ul>')

else:
    print('Forbidden::Mising Upgrade Control Data')

print('</body>')
print('</html>')
