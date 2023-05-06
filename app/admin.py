from django.contrib import admin
#import all model of models.py
from .models import (Customer,Product,Cart,OrderPlaced)
# Register your models here.

#--------------
from .models import *
# Register your models here.


admin.site.register(Profile)
#----------------
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','category','upload_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status']
    


