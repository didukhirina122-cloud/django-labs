from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категорія")
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ціна",
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    is_available = models.BooleanField(default=True, verbose_name="В наявності")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото товару")

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def review_count(self):
        return self.reviews.count()


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я покупця")
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return self.name


# ========== КОШИК ==========

class Cart(models.Model):
    session_key = models.CharField(max_length=40, verbose_name="Сесія")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Кошик {self.session_key}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity


# ========== ЗАМОВЛЕННЯ ==========

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('nova_poshta', 'Нова Пошта'),
        ('ukr_poshta', 'Укрпошта'),
    ]
    DELIVERY_TYPE_CHOICES = [
        ('branch', 'Відділення'),
        ('index', 'За індексом'),
        ('address', 'Адреса'),
    ]
    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    delivery_service = models.CharField(max_length=20, choices=DELIVERY_CHOICES, verbose_name="Служба доставки")
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, verbose_name="Тип доставки")
    city = models.CharField(max_length=100, verbose_name="Місто/село")
    branch_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер відділення")
    postal_index = models.CharField(max_length=10, blank=True, null=True, verbose_name="Індекс")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Адреса")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    def __str__(self):
        return f"Замовлення #{self.pk} — {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def total_price(self):
        return self.price * self.quantity


# ========== ОЦІНКА ТОВАРУ ==========

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оцінка"
    )
    comment = models.TextField(verbose_name="Коментар", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.product.name} ({self.rating}★)"


# ========== РОЗСИЛКА ==========

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name="Ім'я", blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Підписник"
        verbose_name_plural = "Підписники"