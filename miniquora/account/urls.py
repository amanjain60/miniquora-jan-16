from django.conf.urls import url
from .views import login, home, logout,forgot_password, reset_password
urlpatterns = [
    url(r'^logout/$', logout, name ="logout" ),
    url(r'^forgot-password/$', forgot_password, name ="forgot-password" ),
    url(r'^reset/(?P<id>\d+)/(?P<otp>\d{4})/$', reset_password, name='reset-password'),
    url(r'^(?P<id>\d+)/home/$', home, name = "home"),
]
