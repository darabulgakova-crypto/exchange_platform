from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/reviews/', views.product_reviews, name='product_reviews'),
    path('profile/', views.profile_view, name='profile'),
]
