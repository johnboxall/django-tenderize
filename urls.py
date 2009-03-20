from django.conf.urls.defaults import *

urlpatterns = patterns('tenderize.views',
    url(r'^login/$', 'login_and_tenderize', name="login"),
    url(r'^logout/$', 'logout_and_detenderize', name="logout"),
)


