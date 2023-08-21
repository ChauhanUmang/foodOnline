from django.urls import path, include
from vendor import views
from accounts import views as account_views

urlpatterns = [
    path('', account_views.vendor_dashboard, name='vendor'),
    path('profile/', views.profile, name='vendor_profile'),

    # Category CRUD
    path('menu/', include('menu.urls')),

    # Opening Hours
    path('opening-hours/', views.opening_hours, name='opening_hours'),
]
