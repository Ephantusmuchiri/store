from django.forms import ModelForm

from .models import Product

# form to modify the product quantity


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['stock']