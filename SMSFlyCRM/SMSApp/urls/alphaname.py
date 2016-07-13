from django.conf.urls import url

from ..views import alphanames


urlpatterns = (
    # Alphanames list:
    url('^$', alphanames.AlphanameIndexView.as_view(), name='alphanames-root'),
    # Alphaname registration request form:
    url('^new$', alphanames.AlphanameRegisterView.as_view(), name='add-alphaname'),
)
