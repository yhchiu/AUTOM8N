#!/bin/bash

masterrpms=$(rpm -qa|egrep '^ea-apache24|^ea-php|^nginx-nDeploy|^openresty-nDeploy' | sed 's/-[0-9].*//')
ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "yum --enablerepo=ndeploy -y install ${masterrpms}"
echo -e '\e[93m In case you see errors remove conflicting RPMs on slave and rerun this script \e[0m'
