import logging

from datetime import datetime, timedelta
from itertools import starmap

from django.conf import settings

from django.db.models import Q

from django_rq import job

from smsfly import SMSFlyAPI
from smsfly.errors import (
    XMLError, PhoneError, StartTimeError,
    EndTimeError, LifetimeError, SpeedError,
    AlphanameError, TextError, InsufficientFundsError,
    AuthError
)

from .models import Alphaname, Task, Campaign


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


logger = logging.getLogger(__name__)


@job('default')
def scheduleCampaignTasksFor(min_interval):
    now = datetime.now()
    end_time = now + timedelta(min=min_interval)
    tasks = Task.objects.filter(
        Q(state=0) &
        (
            Q(type=0) | Q(type=1)
        ) &
        (
            Q(end_date=None) | Q(end_date__le=now.date())
        )
    ).all()

    for task in tasks:
        if task.type == 0:
            run_at = task.start_datetime
            sendTaskMessagesInstantlyTask.enqueue_at(run_at)
            task.archive()
            logger.info('Task {task} has been scheduled to be run at {scheduled_time}'.
                        format(task=task, scheduled_time=run_at))
        elif task.type == 1:
            for occ in task.get_occurrences_between(now, end_time):
                sendTaskMessagesInstantlyTask.enqueue_at(occ)
                logger.info('Task {task} has been scheduled to be run at {scheduled_time}'.
                            format(task=task, scheduled_time=occ))


@job('high')
def sendTaskMessagesInstantlyTask(task_id):
    api = SMSFlyAPI(account_id=settings.SMS_FLY['login'],
                    account_pass=settings.SMS_FLY['password'])

    task = Task.objects.get(pk=task_id)
    message = task.message_text
    send_as = task.alphaname.name
    description = str(task)

    recipients = task.recipients_queryset  # Filter out recipients from external DB

    message_pairs = starmap(lambda r: (r.cellphone,  # Generate tuple containing cell number and message body
                                       message.format(  # substitute template tags with personalized values:
                                           firstname=r.firstname, lastname=r.lastname,
                                           middlename=r.middlename, cellphone=r.cellphone,
                                           address=r.address,
                                       )),
                            recipients)

    try:
        api_result = api.send_sms_pairs(
            start_time=datetime.now().strftime(DATETIME_FORMAT), end_time='AUTO',
            lifetime=24, rate='AUTO', desc=description, source=send_as,
            message_pairs=message_pairs
        )
    except (XMLError, PhoneError, StartTimeError,
            EndTimeError, LifetimeError, SpeedError,
            AlphanameError, TextError, InsufficientFundsError,
            AuthError) as exc:
        err_msg = "Couldn't submit task {task} (task_id={task_id})".format(task=task, task_id=task_id)
        logger.exception(err_msg)
        raise RuntimeError(err_msg) from exc
    else:
        res_state = api_result.message.state
        campaign = Campaign.objects.create(
            task=task, code=res_state.attrs['code'], state=res_state.text,
            datetime_sent=datetime.strptime(res_state.attrs['date'], DATETIME_FORMAT),
            smsfly_campaign_id=int(res_state.attrs['campaignID']))
        logger.info('Campaign {camp} (smsfly_campaign_id={api_id}) has been accepted by SMS-Fly '
                    'for sending to recipients, defined in task {task} (task_id={task_id})'.
                    format(camp=campaign, api_id=campaign.smsfly_campaign_id, task=task, task_id=task_id))

        return api_result


@job('high')
def submitAlphanameInstantly(name):
    api = SMSFlyAPI(account_id=settings.SMS_FLY['login'],
                    account_pass=settings.SMS_FLY['password'])
    logger.info('Submitting register request for alphaname `{}`...'.format(name))

    api_response_status = api.add_alphaname(alphaname=name).state.attrs['status']
    Alphaname.objects.get(name=name).change_status_to(api_response_status, commit=True)

    logger.info('Saved')
    logger.info('Got status `{}`...'.format(api_response_status))

    return api_response_status
