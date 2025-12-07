from django import forms
from .models import Review, Profile, Product


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'rating': 'Оценка (1-5)',
            'text': 'Текст отзыва',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'phone_number']
        labels = {
            'display_name': 'Отображаемое имя',
            'bio': 'О себе',
            'phone_number': 'Телефон для связи',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Пара слов о себе'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+7...'}),
        }

class ProductForm(forms.ModelForm):
    image = forms.ImageField(label='Фото товара', required=False)

    class Meta:
        model = Product
        fields = ['title', 'sku', 'description']
        labels = {
            'title': 'Название товара',
            'sku': 'Артикул',
            'description': 'Описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
