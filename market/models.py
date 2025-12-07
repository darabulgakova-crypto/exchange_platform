from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    display_name = models.CharField(
        'Отображаемое имя',
        max_length=100,
        blank=True,
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    phone_number = models.CharField(
        'Телефон для связи',
        max_length=20,
        blank=True,
    )

    def __str__(self):
        return self.display_name or self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Product(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
    )
    title = models.CharField('Название', max_length=200)
    sku = models.CharField('Артикул', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='product_images/',
    )

    def __str__(self):
        return f'Фото для {self.product.title}'

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Отзыв на {self.product.title} от {self.author}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
