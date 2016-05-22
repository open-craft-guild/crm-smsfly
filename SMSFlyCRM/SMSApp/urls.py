from django.conf.urls import url

from . import views


urlpatterns = (
    # Index page with a menu:
    url('', views.IndexView.as_view(), name='app-root'),
    # Alphanames list:
    url('alphanames', views.AlphanameIndexView.as_view(), name='alphanames-root'),
    # Alphaname registration request form:
    url('alphanames/new', views.AlphanameRegisterView.as_view(), name='add-alphaname'),
    # Active campaigns list:
    url('sms-campaigns', views.CampaignIndexView.as_view(), name='campaigns-root'),
    # Campaign adding/scheduling form:
    url('sms-campaigns/new', views.CampaignNewView.as_view(), name='add-campaign'),
    # Campaign editing form:
    url('sms-campaigns/edit', views.CampaignEditView.as_view(), name='edit-campaign'),
    # Archive of inactive/sent campaigns:
    url('sms-campaigns/archive', views.CampaignArchiveView.as_view(), name='campaigns-archive'),
)
