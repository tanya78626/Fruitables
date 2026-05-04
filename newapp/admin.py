from django.contrib import admin

from . models import *

#credentials for django admin panel.
#username: fruit
#password: t.123456

# Register your models here.
admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Checkout)
admin.site.register(OrderItem)