from django.urls import path
from .views import get_flood_predictions

urlpatterns = [
    path('', get_flood_predictions, name='predict')
]
