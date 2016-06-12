from django.conf.urls import url

from . import views

from .views import alphanames, campaigns_list


urlpatterns = (
    # Alphanames list:
    url('^alphanames$', alphanames.AlphanameIndexView.as_view(), name='alphanames-root'),
    # Alphaname registration request form:
    url('^alphanames/new$', alphanames.AlphanameRegisterView.as_view(), name='add-alphaname'),
    # Active campaigns list:
    url('^sms-campaigns$', campaigns_list.CampaignIndexView.as_view(), name='campaigns-root'),
    # Campaign adding/scheduling form:
    url('^sms-campaigns/new/one-time$', views.CampaignNewView.as_view(), name='add-campaign'),
    url('^sms-campaigns/new/recurring$', views.CampaignNewRecurringView.as_view(), name='add-recurring-campaign'),
    url('^sms-campaigns/new/event-driven$', views.CampaignNewEventDrivenView.as_view(),
        name='add-event-driven-campaign'),
    # Campaign editing form:
    url('^sms-campaigns/edit$', views.CampaignEditView.as_view(), name='edit-campaign'),
    # Archive of inactive/sent campaigns:
    url('^sms-campaigns/archive$', campaigns_list.CampaignArchiveView.as_view(), name='campaigns-archive'),
    # List of all sent messages:
    url('^sms-campaigns/messages$', views.CampaignMessagesView.as_view(), name='campaigns-messages'),
    # Stats on campaigns:
    url('^sms-campaigns/stats$', views.CampaignStatsView.as_view(), name='campaigns-stats'),
    # Index page with a menu:
    url('^$', views.IndexView.as_view(), name='app-root'),  # Keep it in bottom
)
