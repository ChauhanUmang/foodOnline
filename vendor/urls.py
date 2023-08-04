from django.urls import path
from vendor import views
from accounts import views as account_views

urlpatterns = [
    path('', account_views.vendor_dashboard, name='vendor'),
    path('profile/', views.profile, name='vendor_profile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
]