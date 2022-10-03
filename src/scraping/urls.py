from django.urls import path
from scraping.views import home_authorized, list_view

urlpatterns = [
    path('home_authorized/', home_authorized, name='home_authorized'),
    path('home/', list_view, name='home'),
]