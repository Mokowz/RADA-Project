from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .prediction import predict_flood, predict_drought, predict_all

# Create your views here.
@api_view(['GET'])
def get_flood_predictions(request):
    try:
        predictions = predict_all()
        return Response({
            'status': 'success',
            'predictions': predictions
        })
    except Exception as err:
        return Response({
            'status': 'error',
            'Message': str(err)
        }, status=500)
