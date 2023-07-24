from django.urls import path
from accounts import views

urlpatterns = [
    path('registerUser/', views.register_user, name='register_user'),
]
