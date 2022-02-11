from django.urls import path

from .views import signin, log_out, Google_login

urlpatterns = [
    path('login/', signin),
    path('logout/', log_out),
    path('google-login/', Google_login),

]
