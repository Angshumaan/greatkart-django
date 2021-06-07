from django.urls import path
from . import views


# firstly our url gets check in project root greatkart and then it comess to specific url apps
urlpatterns = [

    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),

]
