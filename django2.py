#!/usr/bin/python

import os
import re
import subprocess

def local_repo():
    repo="""[local-epel]
name=NTI300 EPEL
baseurl=http://146.148.68.114/epel/
gpgcheck=0
enabled=1"""
    os.system('for file in $( ls /etc/yum.repos.d/ ); do mv /etc/yum.repos.d/$file /etc/yum.repos.d/$file.bak; done')
    print(repo)
    with open("/etc/yum.repos.d/local-repo.repo","w+") as f:
      f.write(repo)
    f.close()
local_repo()

def setup_install():
        print('installing pip and virtualenv so we can give django its own version of python')
        os.system('yum -y install python-pip && pip install --upgrade pip')
        os.system('pip install virtualenv')
        os.chdir('/opt')
        os.mkdir('/opt/django')
        os.chdir('/opt/django')
        os.system('virtualenv django-env')

def django_install():
        print('activating virtualenv and installing django after pre-requirements have been met')
        os.system('source /opt/django/django-env/bin/activate && pip install django')
        os.chdir('/opt/django')
        os.system('source /opt/django/django-env/bin/activate ' + \
                          '&& django-admin --version ' + \
                          '&& django-admin startproject project1')

        os.system('adduser -M django')
        os.system('chown -R django /opt/django')
        os.system('usermod -L django')

def django_start():
        print('starting django')
        os.system('chown -R django /opt/django')
        os.chdir('/opt/django/project1')
        os.system('source /opt/django/django-env/bin/activate '+ \
                  '&& python  manage.py migrate')
        os.system('source /opt/django/django-env/bin/activate && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'admin\',\'admin@newproject.com\',\'P@ssw0rd1\')" | python manage.py shell')
        outputwithnewline = subprocess.check_output('curl -s checkip.dyndns.org | sed -e \'s/.*Current IP Address: //\' -e \'s/<.*$//\'',shell=True)
        print outputwithnewline
        output = outputwithnewline.replace("\n", "")
        old_string = "ALLOWED_HOSTS = []"
        new_string = 'ALLOWED_HOSTS = [\'{}\']'.format(output)
        print(new_string)
        print(old_string)

        with open('project1/settings.py') as f:
         newText=f.read().replace(old_string, new_string)
        with open('project1/settings.py', "w") as f:
         f.write(newText)
         f.close(newText) 

        os.system('sudo -u django sh -c "source /opt/django/django-env/bin/activate && python manage.py runserver 0.0.0.0:8000&"')

setup_install()
django_install()
django_start()
