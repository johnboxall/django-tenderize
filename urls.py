from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'tenderize.views.login_and_tenderize', name="login"),
)


