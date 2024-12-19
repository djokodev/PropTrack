from django.contrib import admin
from .models import Property, PropertyTransfer, PropertyImage

admin.site.register(Property)
admin.site.register(PropertyTransfer)
admin.site.register(PropertyImage)
