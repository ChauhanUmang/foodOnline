from django.urls import path
from menu import views

urlpatterns = [
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.products_by_category,
         name='products_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:category_id>', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:category_id>', views.delete_category, name='delete_category'),
]
