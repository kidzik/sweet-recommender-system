from django.forms.models import ModelForm
from sweetrs.recommender.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
             'name',
             'photo',
        )