from rest_framework import serializers
from mongoengine.errors import DoesNotExist
from .models import Booking
from apps.flights.models import Flight
from apps.loyalty.handler import award_loyalty_points


class BookingSerializer(serializers.Serializer):
    id              = serializers.CharField(read_only=True)
    tenant_id       = serializers.CharField()
    flight_id       = serializers.CharField(write_only=True)
    passenger_name  = serializers.CharField()
    passenger_email = serializers.EmailField()
    
    status          = serializers.CharField(read_only=True)
    total_price     = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    created_at      = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        flight_id = validated_data.pop("flight_id")
        # Use pop instead of get so it's removed from validated_data
        tenant_id = validated_data.pop("tenant_id") 

        try:
            flight = Flight.objects.get(id=flight_id, tenant_id=tenant_id, is_active=True)
        except DoesNotExist:
            raise serializers.ValidationError({"flight_id": "Flight not found."})

        if flight.seats_available <= 0:
            raise serializers.ValidationError({"detail": "Flight is sold out."})

        # --- ATOMIC DECREMENT ---
        updated_count = Flight.objects(
            id=flight_id, 
            seats_available__gt=0
        ).update_one(inc__seats_available=-1)

        if updated_count == 0:
            raise serializers.ValidationError({"detail": "Flight sold out during transaction."})

        # Create the booking (validated_data no longer contains tenant_id)
        booking = Booking(
            tenant_id=tenant_id,
            flight=flight,
            total_price=flight.price,
            **validated_data
        ).save()

        # --- Simulate Serverless Event Trigger ---
        event = {
            "tenant_id": tenant_id,
            "passenger_email": booking.passenger_email,
            "total_price": str(booking.total_price)
        }
        award_loyalty_points(event, context=None)

        return booking