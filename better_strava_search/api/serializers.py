from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "id",
            "start_date",
            "elapsed_time",
            "type",
            "average_speed",
            "max_speed",
            "average_cadence",
            "average_heartrate",
            "max_heartrate",
            "suffer_score",
            "calories",
            "gear_name",
            "description",
            "distance",
            "name"
        ]
