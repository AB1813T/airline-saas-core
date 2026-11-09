from datetime import datetime
import mongoengine as me


class Flight(me.Document):
    # Multi-tenant support (e.g., 'acme-air')
    tenant_id        = me.StringField(required=True, index=True)
    
    # Flight details
    flight_number    = me.StringField(required=True)
    origin           = me.StringField(required=True, max_length=3)   # e.g. DAC
    destination      = me.StringField(required=True, max_length=3)   # e.g. DXB
    
    # Schedule & Pricing
    departure_at     = me.DateTimeField(required=True)
    arrival_at       = me.DateTimeField(required=True)
    price            = me.DecimalField(required=True, precision=2)
    currency         = me.StringField(default="USD", max_length=3)
    
    # Inventory
    seats_total      = me.IntField(default=180)
    seats_available  = me.IntField(default=180)
    
    is_active        = me.BooleanField(default=True)
    created_at       = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "flights",
        "indexes": [
            "tenant_id",
            # Compound index: Optimizes searching by route and date (great for CV)
            ("origin", "destination", "departure_at"),
            "departure_at",
        ],
    }

    def __str__(self):
        return f"{self.flight_number} {self.origin}->{self.destination}"