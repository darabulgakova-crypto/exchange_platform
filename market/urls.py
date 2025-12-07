from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/reviews/', views.product_reviews, name='product_reviews'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
