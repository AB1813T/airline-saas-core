import logging
from .models import LoyaltyAccount

logger = logging.getLogger(__name__)

def award_loyalty_points(event: dict, context: dict = None) -> dict:
    """
    Simulates a Serverless Lambda function.
    Triggered when a booking is confirmed.
    """
    try:
        tenant_id = event.get("tenant_id")
        email = event.get("passenger_email")
        total_price = float(event.get("total_price", 0))

        # 10 points for every $100 spent
        points_to_award = int(total_price / 10) 

        if points_to_award <= 0:
            return {"statusCode": 200, "body": "No points awarded"}

        # Update or create the loyalty account (upsert)
        account = LoyaltyAccount.objects(tenant_id=tenant_id, email=email).first()
        
        if account:
            account.update(inc__points=points_to_award)
        else:
            LoyaltyAccount(
                tenant_id=tenant_id, 
                email=email, 
                points=points_to_award
            ).save()

        logger.info(f"Awarded {points_to_award} points to {email}")
        return {
            "statusCode": 200, 
            "body": f"Successfully awarded {points_to_award} points"
        }

    except Exception as e:
        logger.error(f"Loyalty processing failed: {str(e)}")
        return {"statusCode": 500, "body": "Internal Server Error"}