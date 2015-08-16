from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.file_load(), name='file_load'),
]
