from datetime import timedelta
import json
import logging

from django.http import JsonResponse, HttpResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django_rq import get_scheduler

from ..models.task import Task

from ..tasks import sendTaskMessagesInstantlyTask


logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def webhook_crm_event(request, crm_event, crm_user_id):
    task_args = {
        'created_by_crm_user_id': int(crm_user_id),
        'type': 2,  # event-driven
        'triggered_by': 'on{}'.format(crm_event),
    }
    json_res = {}
    try:
        json_req = json.loads(request.body.decode())
        task_args.update(dict(
            filter(lambda k, v: v,
                   {
                       'touch_project_id': json_req.get('project_id'),
                       'touch_status_id': json_req.get('follower_status_id'),
                       'touch_contact_id': json_req.get('contact_id'),
                       'touch_candidate_id': json_req.get('candidate_id'),
                       'trigger_status_id': json_req.get('follower_status_id'),
                   }.items())
        ))
        logger.debug('Following event has occurred: {}'.format(str(task_args)))
    except json.decoder.JSONDecodeError:
        json_res = {
            'result': 'Client Error',
            'status': 400,
            'message': 'The trigger processing has failed',
        }
        logger.exception("Couldn't parse input request")
    else:
        for task in Task.objects.filter(**task_args):
            sendTaskMessagesInstantlyTask.delay(task_id=task.pk)
            logger.info('Task {task} has been triggered'.format(task=task))

        json_res = {
            'result': 'OK',
            'status': 200,
            'message': 'The trigger processing has been queued',
        }
    finally:
        return JsonResponse(json_res)


@require_POST
@csrf_exempt
def webhook_smsfly_status(request):
    logger.debug(request)
    logger.debug(request.body.decode())
    get_scheduler('default').enqueue_in(timedelta(minutes=1), logger.info, 'hi there!')
    return HttpResponse(request.body)
