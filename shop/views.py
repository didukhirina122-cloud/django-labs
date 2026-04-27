from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products_list = Product.objects.all()
    categories_list = Category.objects.all()
    context = {
        'title': 'Apex Sport ',
        'description': 'Ласкаво просимо до найкращого магазину спортивних товарів!',
        'products': products_list,
        'categories': categories_list
    }
    return render(request, 'home.html', context)


def products(request):
    products_list = Product.objects.all()
    categories_list = Category.objects.all()
    context = {
        'title': 'Наші товари',
        'description': 'Професійне спорядження та одяг для твоїх перемог.',
        'products': products_list,
        'categories': categories_list
    }
    return render(request, 'home.html', context)


# Нова функція для відображення товарів конкретної категорії
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # Фільтруємо товари: беремо тільки ті, що належать до цієї категорії
    products_list = Product.objects.filter(category=category)
    categories_list = Category.objects.all()

    context = {
        'title': f'Категорія: {category.name}',
        'description': f'Тут зібрані всі товари з розділу {category.name}.',
        'products': products_list,
        'categories': categories_list
    }
    return render(request, 'home.html', context)


def delivery(request):
    categories_list = Category.objects.all()
    context = {
        'title': 'Доставка та оплата',
        'description': 'Швидка доставка по всій Україні протягом 1-2 днів.',
        'categories': categories_list
    }
    return render(request, 'page.html', context)


def product_detail(request, pk):
    # Шукаємо конкретний товар за його ID (pk)
    product = get_object_or_404(Product, pk=pk)
    categories_list = Category.objects.all()

    return render(request, 'product_detail.html', {
        'product': product,
        'categories': categories_list
    })