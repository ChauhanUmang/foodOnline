from django.urls import path
from vendor import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendor_dashboard, name='vendor'),
    path('profile/', views.profile, name='vendor_profile'),
]