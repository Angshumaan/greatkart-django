from django.urls import path
from . import views


# firstly our url gets check in project root greatkart and then it comess to specific url apps
urlpatterns = [
    # 127.0.0.1:8000/store
    path('', views.store, name='store'),
    # 127.0.0.1:8000/store/category_slug/
    path('category/<slug:category_slug>/',
         views.store, name="products_by_category"),
    # 127.0.0.1:8000/store/category_slug/product_slug/
    path('category/<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail'),
    # 127.0.0.1:8000/store/search/?keyword=aaaaaadhhdhdhhhd
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>',
         views.submit_review, name='submit_review'),
]
