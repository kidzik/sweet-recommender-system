__author__ = 'kidzik'
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^reviews/$', 'sweetrs.recommender.views.product_reviews', {} ,'product_reviews'),
    (r'^results/$', 'sweetrs.recommender.views.product_recommends', {} ,'product_recommends'),
    (r'^add/$', 'sweetrs.recommender.views.product_add', {} ,'product_add'),
    (r'^rate/$', 'sweetrs.recommender.views.product_rate', {} ,'product_rate'),
#    (r'^canvas/$', 'sweetrs.recommender.views.facebook_intro', {}, 'facebook_intro'),
    (r'^canvas/$', 'sweetrs.recommender.views.product_reviews', {
        'template_path': "facebook.html",
        'add_friends': False},
     'facebook_canvas'),
    (r'^canvas/result/$', 'sweetrs.recommender.views.product_recommends', {
        'template_path': "facebook_result.html"
        },
     'facebook_canvas_result'),
)
  
