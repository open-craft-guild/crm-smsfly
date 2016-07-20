from django.conf.urls import include, url

from ..views import stats, messages, IndexView

from . import alphaname as alphaname_urls
from . import campaign as campaign_urls
from .third_party import urlpatterns as third_party_urlpatterns


urlpatterns = (
    # Index page with a menu:
    url('^$', IndexView.as_view(), name='app-root'),  # Keep it in bottom

    # Alphanames:
    url('^alphanames/', include(alphaname_urls), name='alphanames-root'),

    # SMS campaigns:
    url('^sms-campaigns/', include(campaign_urls), name='campaigns-root'),

    # List of all sent messages:
    url('^sms-campaigns/messages(/(?P<page>\d+)?)?$',
        messages.CampaignMessagesView.as_view(),
        name='campaigns-messages'),

    # Stats on campaigns:
    url('^sms-campaigns/stats$', stats.CampaignStatsView.as_view(), name='campaigns-stats'),
) + third_party_urlpatterns
