from django.contrib import admin
from sweetrs.recommender.models import Product, Rating

admin.site.register([Product, Rating])


