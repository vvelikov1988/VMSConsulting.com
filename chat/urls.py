from django.urls import path, re_path

from .views import index, thread, test
from .api import message_fetcher

app_name = 'chat'

urlpatterns = [
    path('', message_fetcher, name='home'),
    path('test/', test, name='fetcher'),
    path('api/test/', message_fetcher, name='api_fetcher'),
    re_path(r'^(?P<username>[\w.@+-]+)', thread, name='message'),

]
