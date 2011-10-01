from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^secure/', 'app1.views.secure', name='secure'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'app1.views.home', name='home'),
)
