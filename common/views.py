from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .prediction import predict_flood, predict_drought, predict_all
from .models import Predictions
from .serializers import PredictionSerializer

# Create your views here.
@api_view(['POST'])
def get_flood_predictions(request):
    try:
        # predictions = predict_all.delay_on_commit()
        predictions = predict_all.delay()
        # return Response({
        #     'status': 'success',
        #     'predictions': predictions
        # })
        return Response({
            'status': 'Prediction task has been triggered',
        })
    except Exception as err:
        return Response({
            'status': 'error',
            'Message': str(err)
        }, status=500)


@api_view(['GET'])
def show_predictions(request):
    today = timezone.localdate()
    end_date = today + timedelta(days=6)

    preds = Predictions.objects.filter(
        date__gte=today,
        date__lte=end_date
    ).order_by('date')

    serializer = PredictionSerializer(preds, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def normal_predictions(request):
    try:
        predictions = predict_all()
        return Response({
            'status': 'success',
            'predictions': predictions
        })
        # return Response({
        #     'status': 'Prediction task has been triggered',
        # })
    except Exception as err:
        return Response({
            'status': 'error',
            'Message': str(err)
        }, status=500)
