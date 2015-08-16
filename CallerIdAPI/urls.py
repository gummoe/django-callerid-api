from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^load-file$', views.file_load, name='load-file'),
    url(r'^query$', views.query, name='query'),
    url(r'^number$', views.number, name='number')
]
