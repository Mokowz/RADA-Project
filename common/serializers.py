from rest_framework import serializers

from .models import Predictions


class PredictionSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_day(self, obj):
        return obj.date.strftime("%A")  # e.g., "Monday"

    def get_created_at(self, obj):
        return obj.created_at.strftime("%B %d, %Y %H:%M")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%B %d, %Y %H:%M")
    class Meta:
        model = Predictions
        fields = ['date', 'day', 'flood_probability', 'drought_probability', 'created_at', 'updated_at']