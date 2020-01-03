from fabric import task
from invoke import Responder
from _credentials import github_password, github_username


def _get_github_auth_responders():
    username_responder = Responder(
        pattern='Username for "https://github.com":',
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern='Password for "https://{}@github.com":'.format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '/home/tony/etc/'
    supervisor_program_name = 'blog'
    project_root_path = '/home/tony/apps/test_blog/'

    # 停止应用
    print('---------------停止应用-------------------')
    with c.cd(supervisor_conf_path):
        cmd = f'supervisorctl stop {supervisor_program_name}'
        c.run(cmd)

    # git拉取代码
    print('---------------git拉取代码-------------------')
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装依赖
    print('---------------安装依赖-------------------')
    with c.cd(project_root_path):
        c.run('source ll_env/bin/activate && pip install requirements.txt -r')
        c.run('python manage.py migrate')
        c.run('python manage.py collectstatic --noinput')

    # 重启服务
    print('---------------重启服务-------------------')
    with c.cd(supervisor_conf_path):
        cmd = f'supervisorctl start {supervisor_program_name}'
        c.run(cmd)
