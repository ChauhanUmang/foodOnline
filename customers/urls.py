from django.urls import path
from customers import views
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.cust_dashboard, name='custDashboard'),
    path('profile/', views.profile, name='cust_profile'),
]