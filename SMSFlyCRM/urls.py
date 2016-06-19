"""SMSFlyCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.i18n import javascript_catalog

import SMSFlyCRM.smartselects.urls
import SMSFlyCRM.SMSApp.urls
from SMSFlyCRM.SMSApp.views.webhooks import webhook_crm_event, webhook_smsfly_status
from SMSFlyCRM.SMSApp.views.api import preview_recipients_list

js_info_dict = {
    'packages': ('recurrence', ),
}


urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin-root'),
    url(r'^app/', include(SMSFlyCRM.SMSApp.urls), name='app-root'),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^webhooks/on(?P<crm_event>\w+)/(?P<crm_user_id>\d+)', webhook_crm_event, name='webhook-crm'),
    url(r'^webhooks/onSMSFlyStatus', webhook_smsfly_status, name='webhook-smsfly'),
    url(r'^chaining/', include(SMSFlyCRM.smartselects.urls)),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict),
    url(r'^api/preview_recipients/$', preview_recipients_list, name='preview-recipients'),
]
