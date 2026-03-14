from django.contrib import admin
from .models import Fruit
from .models import Order

admin.site.site_header = "Talapala's Grocery Admin"
admin.site.site_title = "Talapala Grocery Portal"
admin.site.index_title = "Welcome to Talapala Grocery Dashboard"

admin.site.register(Fruit)
admin.site.register(Order)