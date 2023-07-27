from django.urls import path
from accounts import views

urlpatterns = [
    path('registerUser/', views.register_user, name='register_user'),
    path('registerVendor/', views.register_vendor, name='register_vendor'),

    # Login and Logout pages
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
