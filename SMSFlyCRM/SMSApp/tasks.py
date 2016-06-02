from django.conf import settings

from django_rq import job
from time import sleep
from datetime import datetime

from smsfly import SMSFlyAPI

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@job('default')
def addNewCampaignTask(task_id):
    sleep(0.5)
    return 'Ran {}'.format(task_id)


@job('high')
def sendMessagesInstantly():
    api = SMSFlyAPI(account_id=settings.SMS_FLY['login'],
                    account_pass=settings.SMS_FLY['password'])
    api.send_sms_to_recipients(start_time=datetime.now().strftime(DATETIME_FORMAT), end_time='AUTO',
                               lifetime=24, rate='AUTO', desc='Test task',
                               source='Alpha', body='Hi man!', recipients=('380971234567',))

    pass
