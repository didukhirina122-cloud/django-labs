from django.shortcuts import render
from django.shortcuts import render

def home(request):
    context = {
        'title': 'Sport Shop',
        'description': 'Ласкаво просимо до магазину спортивних товарів!'
    }
    return render(request, 'home.html', context)


def products(request):
    context = {
        'title': 'Наші товари',
        'description': 'Тут ви знайдете спортивний одяг, взуття та інвентар.'
    }
    return render(request, 'page.html', context)


def delivery(request):
    context = {
        'title': 'Доставка',
        'description': 'Швидка доставка по всій Україні.'
    }
    return render(request, 'page.html', context)
