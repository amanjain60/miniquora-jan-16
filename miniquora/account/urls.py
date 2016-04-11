from django.conf.urls import url
from .views import login, home, logout,forgot_password, reset_password, signup, activate,get_all_users
urlpatterns = [
    url(r'^logout/$', logout, name ="logout" ),
    url(r'^login/$', login, name ="another-login" ),
    url(r'^allusers/$', get_all_users, name ="all-users" ),
    url(r'^signup/$', signup, name ="signup" ),
    url(r'^forgot-password/$', forgot_password, name ="forgot-password" ),
    url(r'^reset/(?P<id>\d+)/(?P<otp>\d{4})/$', reset_password, name='reset-password'),
    url(r'^activate/(?P<id>\d+)/(?P<otp>\d{4})/$', activate, name='activate-account'),
    url(r'^(?P<id>\d+)/home/$', home, name = "home"),
    
]
