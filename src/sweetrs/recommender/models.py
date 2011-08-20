from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
class Product(models.Model):
    name = models.CharField(blank = False,
                          null = False,
                          max_length = 150,
                          verbose_name = _(u'Product name'))
    description = models.TextField(blank = True,
                          null = True,
                          verbose_name = _(u'Description'))
    photo = models.ImageField(upload_to='photos')

    class Meta:
        ordering = ('-id',)

class Rating(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    value = models.IntegerField(blank = True,
                               null = True,
                               verbose_name = _(u'Ocena produktu'))
