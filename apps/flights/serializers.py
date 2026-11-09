from rest_framework import serializers
from .models import Flight


class FlightSerializer(serializers.Serializer):
    # Read-only fields
    id              = serializers.CharField(read_only=True)
    created_at      = serializers.DateTimeField(read_only=True)
    
    # Writable fields
    tenant_id       = serializers.CharField()
    flight_number   = serializers.CharField()
    origin          = serializers.CharField(max_length=3)
    destination     = serializers.CharField(max_length=3)
    departure_at    = serializers.DateTimeField()
    arrival_at      = serializers.DateTimeField()
    price           = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency        = serializers.CharField(max_length=3, default="USD")
    seats_total     = serializers.IntegerField(default=180)
    seats_available = serializers.IntegerField(default=180)
    is_active       = serializers.BooleanField(default=True)

    def create(self, validated_data):
        # Create the MongoEngine document
        return Flight(**validated_data).save()

    def update(self, instance, validated_data):
        # Update fields manually
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance