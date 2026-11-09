import mongoengine as me

class LoyaltyAccount(me.Document):
    tenant_id = me.StringField(required=True, index=True)
    email     = me.EmailField(required=True)
    points    = me.IntField(default=0)

    meta = {
        "collection": "loyalty_accounts",
        "indexes": [
            # Compound index: One account per email per tenant
            {"fields": ("tenant_id", "email"), "unique": True}
        ],
    }