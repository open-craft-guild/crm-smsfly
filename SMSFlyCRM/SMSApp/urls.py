from django.conf.urls import url

from . import views


urlpatterns = (
    # Alphanames list:
    url('^alphanames', views.AlphanameIndexView.as_view(), name='alphanames-root'),
    # Alphaname registration request form:
    url('^alphanames/new', views.AlphanameRegisterView.as_view(), name='add-alphaname'),
    # Active campaigns list:
    url('^sms-campaigns', views.CampaignIndexView.as_view(), name='campaigns-root'),
    # Campaign adding/scheduling form:
    url('^sms-campaigns/new', views.CampaignNewView.as_view(), name='add-campaign'),
    # Campaign editing form:
    url('^sms-campaigns/edit', views.CampaignEditView.as_view(), name='edit-campaign'),
    # Archive of inactive/sent campaigns:
    url('^sms-campaigns/archive', views.CampaignArchiveView.as_view(), name='campaigns-archive'),
    # List of all sent messages:
    url('^sms-campaigns/messages', views.CampaignMessagesView.as_view(), name='campaigns-messages'),
    # Stats on campaigns:
    url('^sms-campaigns/stats', views.CampaignStatsView.as_view(), name='campaigns-stats'),
    # Index page with a menu:
    url('^', views.IndexView.as_view(), name='app-root'),  # Keep it in bottom
)
