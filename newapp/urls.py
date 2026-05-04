from django.urls import path
from .views import*

urlpatterns = [
    path('register/',view=register,name='register'),
    path('login/', view=login, name='login'),
    path('', view=index, name='index'),
    path('cart/', view=cart, name='cart'),
    path('checkout/', view=checkout, name='checkout'),
    path('contact/', view=contact, name='contact'),
    path('shop-detail/', view=shop_detail, name='shop-detail'),
    path('shop/', view=shop, name='shop'),
    path('testimonial/', view=testimonial, name='testimonial'),
    path('error/', view=error, name='error'),
    path('add-to-cart/<int:product_id>/', view=add_to_cart, name='add_to_cart'),
    path('plus-cart/<int:product_id>/', view=plus_cart, name='plus_cart'),
    path('minus-cart/<int:product_id>/', view=minus_cart, name='minus_cart'),
    path('remove-cart/<int:product_id>/', view=remove_cart, name='remove_cart'),
    path('place-order/', view=place_order, name='place_order'),
    path('confirm-order/', view=confirm_order, name='confirm_order'),
    path('search/', view=search_item, name='search_item'),
    path('payment/', view=payment, name='payment'),
   
]

