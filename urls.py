from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout_then_login
from dpro.bilet.views import * #index, doldur, listele, csvdeneme, degistir, 

urlpatterns = patterns(
    '',
    (r'^bilet/admin/',   include('django.contrib.admin.urls')),
    (r'^bilet/login/$',  login, {'template_name': 'login.html'}),
    (r'^bilet/logout/$', logout_then_login),
    (r'^bilet/index/$',  index),
    (r'^bilet/biletdoldur/([H, O, D])/(\d{1,})/$', doldur),
    (r'^bilet/biletlistele/(\d{1,})/$',    listele),
#    (r'^bilet/csvdeneme/$', csvdeneme),
    (r'^bilet/degistir/(\d{1,})/$', degistir),
    (r'^bilet/biletsil/(\d{1,})/$', sil),
    (r'^bilet/ara/$', ara),
)
