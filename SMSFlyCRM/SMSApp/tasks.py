from datetime import datetime
from time import sleep

from django.conf import settings

from django_rq import job

from smsfly import SMSFlyAPI

from .models import Alphaname


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@job('default')
def addNewCampaignTask(task_id):
    sleep(0.5)
    return 'Ran {}'.format(task_id)


@job('high')
def sendMessagesInstantly(message='Hi man!', send_as='Alpha',
                          description='Test task', to=('380971234567',),
                          task_id=100500):
    api = SMSFlyAPI(account_id=settings.SMS_FLY['login'],
                    account_pass=settings.SMS_FLY['password'])
    return api.send_sms_to_recipients(
        start_time=datetime.now().strftime(DATETIME_FORMAT), end_time='AUTO',
        lifetime=24, rate='AUTO', desc=description,
        source=send_as, body=message, recipients=to
    )


@job('high')
def submitAlphanameInstantly(name):
    api = SMSFlyAPI(account_id=settings.SMS_FLY['login'],
                    account_pass=settings.SMS_FLY['password'])
    print('Submitting register request for alphaname `{}`...'.format(name))

    api_response_status = api.add_alphaname(alphaname=name).state.attrs['status']
    alphaname = Alphaname.objects.get(name=name)
    alphaname.status = api_response_status
    alphaname.save()

    print('Saved')
    print('Got status `{}`...'.format(api_response_status))

    return api_response_status
