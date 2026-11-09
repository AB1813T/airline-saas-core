from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import mongoengine

class HealthCheckView(APIView):
    """
    Ping the database to ensure Django and MongoDB are talking.
    """
    def get(self, request):
        try:
            # Get the raw pymongo client from mongoengine and ping it
            mongoengine.connection.get_connection().admin.command('ping')
            return Response({
                "status": "ok",
                "database": "connected",
                "message": "Airline SaaS API is healthy"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)