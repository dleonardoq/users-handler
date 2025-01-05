from django.urls import re_path
from .views import users

urlpatterns = [
    re_path(r'^users/(?P<user_id>\w+)?$', users, name='users'),
]
