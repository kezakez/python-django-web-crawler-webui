from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
import model

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^search$', model.search),
)
