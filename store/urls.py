from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/store
    path('', views.store, name='store'),
    # 127.0.0.1:8000/store/category_slug/
    path('<slug:category_slug>/', views.store, name="products_by_category"),
    # 127.0.0.1:8000/store/category_slug/product_slug/
    path('<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail')
]
