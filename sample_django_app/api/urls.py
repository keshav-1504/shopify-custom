from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.products, name="products"),
    path("orders/", views.orders, name="orders"),
    # ++++=====================================================++++ >> KJ
    path('addProduct/', views.addProduct, name='addProduct'),
    path('updateInventory/', views.updateInventory, name='updateInventory'),
    path('addOrderMetafield/', views.addOrderMetafield, name='addOrderMetafield'),
    path('addProductMetafield/', views.addProductMetafield,
         name='addProductMetafield'),
    path('createOrder/', views.createOrder, name='createOrder'),
    path('orderFulfillment/', views.orderFulfillment, name='orderFulfillment'),
    # ++++=====================================================++++ >> KJ
]
