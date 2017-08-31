from fabric.api import cd, env, put, run
from fabric.colors import cyan
from fabric.contrib.console import confirm
from fabric.utils import warn

env.use_ssh_config = True
env.user = 'root'


def update_secret():
    # run('mkdir -p /home/jms/.ssh/', )
    # put('~/.ssh/others/id_rsa_jms', '/home/jms/.ssh/id_rsa', mode='400')
    # put('~/.ssh/others/id_rsa_jms.pub', '/home/jms/.ssh/id_rsa.pub', mode='400')
    # run('chown jms:jms /home/jms/.ssh/*')
    put('./data/pwd.txt', '~/pwd.txt', mode='400')
    put('./data/jms', '/etc/sudoers.d/jms', mode='400')
    run('cat ~/pwd.txt | chpasswd')


def create_jms_user():
    """
    1. jms 用户是否存在
    2. 否
      2.1 创建jms
      2.2 上传key文件     
    
    """
    ret = run('cat /etc/passwd | grep jms', warn_only=True)
    if ret:
        warn('jms用户已经存在')

    else:
        warn('创建jms用户...')
        run('useradd -m jms')

    ret = run('cat /etc/passwd | grep pyer', warn_only=True)
    if ret:
        warn('pyer用户已经存在')

    else:
        warn('创建pyer用户...')
        run('useradd -m pyer')

    is_update_secret = confirm('是否更新jms/pyer的密码？', default=False)
    if is_update_secret:
        update_secret()

    print(cyan('操作完成'))


def pub():
    """生产发布"""
    with cd('/data/prd/jumpserver'):
        run('git pull')
