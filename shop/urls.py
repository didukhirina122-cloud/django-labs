from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('delivery/', views.delivery, name='delivery'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),

    # Кошик
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:pk>/', views.cart_update, name='cart_update'),

    # Замовлення
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),

    # Відгук
    path('product/<int:pk>/review/', views.add_review, name='add_review'),

    # Розсилка
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
]