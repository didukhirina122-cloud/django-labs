from django.shortcuts import render
from .models import Product  # 1. Додаємо імпорт моделі


def home(request):
    # 2. Беремо всі товари з бази
    products_list = Product.objects.all()

    context = {
        'title': 'Sport Shop',
        'description': 'Ласкаво просимо до магазину спортивних товарів!',
        'products': products_list  # 3. Додаємо їх у контекст
    }
    return render(request, 'home.html', context)


def products(request):
    products_list = Product.objects.all()

    context = {
        'title': 'Наші товари',
        'description': 'Тут ви знайдете спортивний одяг, взуття та інвентар.',
        'products': products_list  # Додаємо і сюди, якщо хочеш бачити їх на цій сторінці
    }
    return render(request, 'page.html', context)


def delivery(request):
    context = {
        'title': 'Доставка',
        'description': 'Швидка доставка по всій Україні.'
    }
    return render(request, 'page.html', context)