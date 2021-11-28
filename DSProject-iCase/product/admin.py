from django.contrib import admin
from .models import Product,IphoneModel,CollectionFeature

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','image','price','model','collection','slug',)
    prepopulated_fields = {'slug': ('title',)} 


admin.site.register(Product,ProductAdmin)
admin.site.register(IphoneModel)
admin.site.register(CollectionFeature)