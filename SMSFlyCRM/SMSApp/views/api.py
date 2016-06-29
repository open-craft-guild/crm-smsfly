import json
import logging

from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from ..models.task import Task

from ..utils import calculate_price_for, get_price_for

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def preview_recipients_list(request):
    json_req = json.loads(request.body.decode())
    user_id = request.session['crm_user_id']
    offset = int(json_req.get('offset', 0))
    limit = int(json_req.get('limit', 100))
    until = offset + limit
    amount = Task.get_recipients_amount_by_filter(json_req['recipients_filter'], user_id)
    msg_length = int(json_req.get('msg_length', 1))
    price_per_msg = get_price_for(amount)
    price = calculate_price_for(amount, msg_length)
    rec_qs = Task.get_recipients_queryset_by_filter(json_req['recipients_filter'], user_id)
    rec_list = []
    for el in rec_qs[offset:until]:
        rec = {}
        for attr in ('name', 'cellphone', 'sex', 'age', 'poll_place',
                     'family_status', 'social_category',
                     'education', 'status',
                     ('address_full', 'address'),
                     ('regaddress_full', 'regaddress')):
            if isinstance(attr, str):
                attr_name = attr_key = attr
            else:
                attr_name, attr_key = attr

            try:
                attr_val = getattr(el, attr_name)
                if attr_val is None:
                    raise ObjectDoesNotExist
                rec[attr_key] = str(attr_val)
                rec[attr_key] = int(rec[attr_key])
            except ObjectDoesNotExist:
                rec[attr_key] = None
            except ValueError:
                pass  # Not an integer
        rec_list.append(rec)
    result = {
        'amount': amount,
        'attrs': [
            'name', 'cellphone', 'sex', 'age', 'regaddress', 'address', 'poll_place',
            'social_category', 'family_status',
            'education', 'status'
            ],
        'sms_price': float(price_per_msg),
        'campaign_cost': float(price),
        'recipients': rec_list,
        'offset': offset,
        'limit': limit,
    }
    return JsonResponse(result, safe=False)
