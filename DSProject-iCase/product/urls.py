from django.urls import path
from .views import product_view,product_test_filter,product_collections_view,product_detail_view


urlpatterns = [
    # cases/

    path('',product_view,name='cases.html') ,
    path('collection/',product_collections_view,name='collection.html'),
    # path('<int:product_id>',product_detail_view),
    path('product/<slug:product_slug>',product_detail_view),
    path('test/',product_test_filter),
    path('test/<int:product_id>',product_detail_view,name = 'cases_test')
    
] 