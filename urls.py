from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'django_tenderize.views.login_and_tenderize', name="login"),
)


