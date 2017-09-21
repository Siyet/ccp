# coding: utf-8

from __future__ import with_statement

from fabric.api import local, run, cd, env, roles, prefix
from fabric.operations import prompt

env.roledefs['staging'] = ['root@shirts.wecreateapps.ru']

try:
    import credentials
except:
    pass


def staging_env():
    try:
        env.user = credentials.user
        env.password = credentials.password
        env.gituser = credentials.gituser
        env.gitpassword = credentials.gitpassword
    except:
        print("Couldn't find crdentials file...")
        env.gituser = prompt("What is your git user?")
        env.gitpassword = prompt("What is your git password?")

    env.project_root = '/var/webapps/costumecode/costumecode_configurator'  # Путь до каталога проекта (на сервере)
    env.virtualenv = 'source /var/venv/costumecode/bin/activate'  # Путь до virtualenv (на сервере)


def prepare_deploy():
    local("git add . && git commit")
    local("git push")


@roles('staging')
def deploy():
    staging_env()
    with cd(env.project_root):
        git_credentials = "%s:%s" % (env.gituser, env.gitpassword)
        run("git pull https://%s@bitbucket.org/wecreateapps/costumecode_configurator.git master" % git_credentials)
        with prefix(env.virtualenv):
            run("pip install -r requirements.txt")
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")
            run("python manage.py compilemessages")

        run("touch ../uwsgi/ccback.ini")


@roles('staging')
def rebuild_textures():
    staging_env()
    with cd(env.project_root):
        git_credentials = "%s:%s" % (env.gituser, env.gitpassword)
        run("git pull https://%s@bitbucket.org/wecreateapps/costumecode_configurator.git master" % git_credentials)
        with prefix(env.virtualenv):
            run("python manage.py rebuild_textures")
