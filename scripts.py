# coding:utf-8

import logging
import os

from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.jumpserver.settings")
setup()


def finish_yestoday_sessions():
    from apps.audits.models import ProxyLog
    import datetime
    two_days_ago = datetime.datetime.today() - datetime.timedelta(2)
    total = ProxyLog.objects \
        .filter(date_start__lte=two_days_ago) \
        .filter(is_finished=False) \
        .update(is_finished=True)
    logging.info('结束了：%s 个挂起进程', total)
