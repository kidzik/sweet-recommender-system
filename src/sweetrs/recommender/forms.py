from django import forms
from django.forms.models import ModelForm
from sweetrs.recommender.models import Product
from django.core.validators import validate_email

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
             'name',
             'photo',
        )
        
class EmailField(forms.CharField):
    default_error_messages = {
        'invalid': (u'Enter a valid e-mail address.'),
    }
    default_validators = [validate_email]
        
class AccessForm(forms.Form):
    email = forms.EmailField(required=False)
    secret = forms.CharField(required=False)
