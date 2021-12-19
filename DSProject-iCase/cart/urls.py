from django.urls import path, include
from .views import cart_view, update_item_view

urlpatterns = [
    path('', cart_view,name='cart_view'),
    path('update_item/', update_item_view,name='update_item_view'),

]
