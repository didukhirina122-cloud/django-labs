from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, Order, OrderItem, ProductReview, NewsletterSubscriber


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# ========== ГОЛОВНА ==========

def home(request):
    cheapest = Product.objects.order_by('price').first()
    categories = Category.objects.all()
    return render(request, 'home.html', {'cheapest': cheapest, 'categories': categories})


# ========== БРЕНДИ ==========

def products(request):
    categories_list = Category.objects.all()
    return render(request, 'categories.html', {
        'title': 'Бренди',
        'categories': categories_list,
    })


# ========== КАТЕГОРІЯ ==========

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products_list = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {
        'title': category.name,
        'description': f'Всі товари бренду {category.name}.',
        'products': products_list,
    })


# ========== ПОШУК ==========

def search(request):
    query = request.GET.get('q', '').strip()
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'search.html', {'query': query, 'results': results})


# ========== ТОВАР ==========

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.order_by('-created_at')
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': product.average_rating(),
        'review_count': product.review_count(),
    })


# ========== ДОСТАВКА ==========

def delivery(request):
    return render(request, 'page.html', {
        'title': 'Доставка та оплата',
        'description': 'Швидка доставка по всій Україні протягом 1-2 днів.',
    })


# ========== КОШИК ==========

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart.html', {'cart': cart})


def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" додано до кошика!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def cart_remove(request, pk):
    cart = get_or_create_cart(request)
    CartItem.objects.filter(cart=cart, id=pk).delete()
    return redirect('cart')


def cart_update(request, pk):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, cart=cart, id=pk)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('cart')


# ========== ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ==========

def checkout(request):
    cart = get_or_create_cart(request)
    if cart.items.count() == 0:
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            delivery_service=request.POST.get('delivery_service'),
            delivery_type=request.POST.get('delivery_type'),
            city=request.POST.get('city'),
            branch_number=request.POST.get('branch_number', ''),
            postal_index=request.POST.get('postal_index', ''),
            address=request.POST.get('address', ''),
            total_price=cart.total_price(),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        cart.items.all().delete()
        return redirect('order_success', pk=order.pk)

    return render(request, 'checkout.html', {'cart': cart})


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_success.html', {'order': order})


# ========== ВІДГУК ==========

def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if name and rating:
            ProductReview.objects.create(
                product=product,
                name=name,
                rating=int(rating),
                comment=comment,
            )
            messages.success(request, 'Дякуємо за вашу оцінку!')
    return redirect('product_detail', pk=pk)


# ========== РОЗСИЛКА ==========

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        if email:
            _, created = NewsletterSubscriber.objects.get_or_create(
                email=email, defaults={'name': name}
            )
            if created:
                messages.success(request, 'Ви успішно підписались на розсилку!')
            else:
                messages.info(request, 'Ви вже підписані на розсилку.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))