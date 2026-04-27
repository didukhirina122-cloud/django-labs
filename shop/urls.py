from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('delivery/', views.delivery, name='delivery'),
    # Додаємо шлях для категорій, який ми використали в шаблоні:
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
path('product/<int:pk>/', views.product_detail, name='product_detail'),
]