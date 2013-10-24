from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('mim.views',
    url(r'^$', 'index'),
    url(r'^fetch/$', 'fetch'),
    url(r'^result/$', 'result'),
    url(r'^log/$', 'log'),
#    url(r'^fetched/$', 'fetched')
)
