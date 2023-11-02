from django.contrib import admin
from django.urls import reverse_lazy

from .models import Product

admin.site.site_header = 'Store | Main Admin'
admin.site.site_title = 'Main Admin | Store App'
admin.site.index_title = 'Admin | Store App'
admin.site.site_url = reverse_lazy('products')

admin.site.register(Product)
