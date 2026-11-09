from datetime import datetime
import mongoengine as me
from apps.flights.models import Flight


class Booking(me.Document):
    tenant_id       = me.StringField(required=True, index=True)
    flight          = me.ReferenceField(Flight, required=True, reverse_delete_rule=me.DENY)
    
    passenger_name  = me.StringField(required=True)
    passenger_email = me.EmailField(required=True)
    
    status          = me.StringField(choices=["CONFIRMED", "CANCELLED"], default="CONFIRMED")
    total_price     = me.DecimalField(required=True, precision=2)
    
    created_at      = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "bookings",
        "indexes": ["tenant_id", "passenger_email"],
    }
    