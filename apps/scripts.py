# coding:utf-8

import logging
import os

from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jumpserver.settings")
setup()


def finish_yestoday_sessions():
    from audits.models import ProxyLog
    import django.utils.timezone as datetime
    two_days_ago = datetime.now() - datetime.timedelta(2)
    total = ProxyLog.objects \
        .filter(date_start__lte=two_days_ago) \
        .filter(is_finished=False) \
        .update(is_finished=True)
    logging.info('结束了：%s 个挂起进程', total)

if __name__ == '__main__':
    finish_yestoday_sessions()