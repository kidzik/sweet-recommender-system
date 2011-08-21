from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.models import User
from recommender.models import Rating
import settings
#import socialregistration

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^srs/', include('sweetrs.recommender.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
#    (r'^social/', include('sweetrs.socialregistration.urls')),

    (r'^$', 'sweetrs.views.about', {} ,'about_us'),
    (r'^logout/$', 'sweetrs.views.logout', {} ,'logout'),
)
urlpatterns += patterns('django.views.generic.simple',
    (r'^faq/$', 'direct_to_template', {'template': 'flatpages/faq.html'}, 'faq'),
)

urlpatterns += patterns('',
    (r"static/(?P<path>.*)$", "django.views.static.serve", {
            "document_root": settings.MEDIA_ROOT,
    }),
)
