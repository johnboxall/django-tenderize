from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'jungle.tender.views.login_and_tenderize', name="login"),
)


