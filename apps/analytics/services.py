import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    @staticmethod
    def get_google_analytics(tenant_id: str) -> dict:
        logger.info(f"Fetching GA data for tenant: {tenant_id}")
        return {
            "source": "Google Analytics 4",
            "tenant_id": tenant_id,
            "metrics": {
                "active_users": 1450,
                "sessions": 3200,
                "conversion_rate": "3.2%"
            }
        }

    @staticmethod
    def get_facebook_ads(tenant_id: str) -> dict:
        logger.info(f"Fetching FB data for tenant: {tenant_id}")
        return {
            "source": "Facebook Marketing API",
            "tenant_id": tenant_id,
            "metrics": {
                "impressions": 45000,
                "clicks": 1200,
                "cost_per_click": "0.45"
            }
        }