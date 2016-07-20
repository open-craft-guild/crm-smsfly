from django.conf import settings
from django.conf.urls import include, url

urlpatterns = ()
try:
    import rosetta.urls

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += (
            url(r'^rosetta/', include(rosetta.urls)),
        )
except ImportError:
    pass
