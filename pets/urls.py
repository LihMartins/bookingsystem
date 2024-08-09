from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_pet, name='register_pet'),  # URL for registering a pet
    path('', views.pet_list, name='pet_list'),  # URL for listing all pets
]
