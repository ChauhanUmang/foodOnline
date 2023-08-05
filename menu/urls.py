from django.urls import path
from menu import views

urlpatterns = [
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.products_by_category,
         name='products_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
]
