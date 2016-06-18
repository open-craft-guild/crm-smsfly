"""Views for Django Smart Selects

This module has been shamelessly ripped out from
https://github.com/digi604/django-smart-selects/blob/master/smart_selects/views.py
and modify to conform SQL authentication requirements of SMSApp
"""

from django.http import JsonResponse

from smart_selects.views import (
    is_m2m,  # views helper
    get_model,  # django

    # utils:
    get_keywords, sort_results, serialize_results,
    get_queryset, get_limit_choices_to
)


def filterchain(request, app, model, field, foreign_key_app_name, foreign_key_model_name,
                foreign_key_field_name, value, manager=None):
    model_class = get_model(app, model)
    m2m = is_m2m(model_class, field)
    keywords = get_keywords(field, value, m2m=m2m)
    # filter queryset using limit_choices_to
    limit_choices_to = get_limit_choices_to(foreign_key_app_name, foreign_key_model_name, foreign_key_field_name)
    queryset = get_queryset(model_class, manager, limit_choices_to)

    try:
        queryset = queryset.for_user(request.session['crm_user_id'])
    except AttributeError:
        pass  # There's no `for_user(user_id)` method in current manager

    results = queryset.filter(**keywords)

    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        results = list(results)
        sort_results(results)

    serialized_results = serialize_results(results)
    return JsonResponse(serialized_results, safe=False)


def filterchain_all(request, app, model, field, foreign_key_app_name,
                    foreign_key_model_name, foreign_key_field_name, value):
    """Returns filtered results followed by excluded results below."""
    model_class = get_model(app, model)
    keywords = get_keywords(field, value)
    # filter queryset using limit_choices_to
    limit_choices_to = get_limit_choices_to(foreign_key_app_name, foreign_key_model_name, foreign_key_field_name)
    queryset = get_queryset(model_class, limit_choices_to=limit_choices_to)

    try:
        queryset = queryset.for_user(request.session['crm_user_id'])
    except AttributeError:
        pass  # There's no `for_user(user_id)` method in current manager

    filtered = list(queryset.filter(**keywords))
    sort_results(filtered)

    excluded = list(queryset.exclude(**keywords))
    sort_results(excluded)

    # Empty choice to separate filtered and excluded results.
    empty_choice = {'value': '', 'display': '-' * 9}

    serialized_results = (
        serialize_results(filtered) +
        [empty_choice] +
        serialize_results(excluded)
    )

    return JsonResponse(serialized_results, safe=False)
