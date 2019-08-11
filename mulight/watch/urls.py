from django.conf.urls import url

from watch.views import do_checkout


urlpatterns = [
    url(r'^checkout/$', do_checkout, name='do_checkout'),
]
