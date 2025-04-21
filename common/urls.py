from django.urls import path
from .views import get_flood_predictions, show_predictions, normal_predictions

urlpatterns = [
    path('trigger_preds', get_flood_predictions, name='predict'), # Manuallyy trigger the celery workers to do the prediction
    path('normal_preds', normal_predictions, name='predict'), # Does the prediction without depending on celery
    path('preds/', show_predictions, name='show_preds'),  # Displays the result of the last run prediction
]
