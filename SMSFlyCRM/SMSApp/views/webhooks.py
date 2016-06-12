import json
import logging

from django.http import JsonResponse, HttpResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from ..models import Project


logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def webhook_crm_event(request, crm_event, crm_user_id):
    crm_user_id = int(crm_user_id)
    json_res = {}
    try:
        json_req = json.loads(request.body.decode())
        'sms_view_projects.project_id'
        'sms_view_follower_status.follower_status_id'
        'sms_view_project_contacts.contact_id'
        'sms_view_candidates.candidate_id'
    except json.decoder.JSONDecodeError:
        json_res = {
            'result': 'Client Error',
            'status': 400,
            'message': 'The trigger processing has failed',
        }
    else:
        json_res = {
            'result': 'OK',
            'status': 200,
            'message': 'The trigger processing has been queued',
            'data': Project.objects.for_user(crm_user_id).filter(project_id=json_req['project_id']).all()[0].
            project_name,
        }
    finally:
        return JsonResponse(json_res)


@require_POST
@csrf_exempt
def webhook_smsfly_status(request):
    logger.debug(request)
    logger.debug(request.body.decode())
    return HttpResponse(request.body)
