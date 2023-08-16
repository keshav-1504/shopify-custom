from django.urls import path

from .views import *
from django.urls import include, path

# ++++=====================================================++++ >> KJ
urlpatterns = [
    path('products', products, name='products'),
    path('orders', orders, name='orders'),
    path('addProduct', addProduct, name='addProduct'),
    path('updateInventory', updateInventory, name='updateInventory'),
    path('addProductMetafield', addProductMetafield,),
    path('addOrderMetafield', addOrderMetafield),
    path('createOrder', createOrder, name='createOrder'),
    path('orderFulfillment', orderFulfillment, name='orderFulfillment'),
    # path('test', test, name='test'),
]

# ++++=====================================================++++ >> KJ