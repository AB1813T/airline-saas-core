from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .services import AnalyticsService

class AnalyticsOverviewView(APIView):
    """
    Unified dashboard endpoint fetching data from external marketing APIs.
    """
    @extend_schema(
        parameters=[
            OpenApiParameter("tenant_id", OpenApiTypes.STR, required=True, description="Tenant ID"),
        ],
        description="Fetch combined analytics from Google and Facebook."
    )
    def get(self, request):
        tenant_id = request.query_params.get("tenant_id")
        
        if not tenant_id:
            return Response(
                {"error": "tenant_id query parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        ga_data = AnalyticsService.get_google_analytics(tenant_id)
        fb_data = AnalyticsService.get_facebook_ads(tenant_id)

        return Response({
            "tenant_id": tenant_id,
            "google_analytics": ga_data,
            "facebook_ads": fb_data
        }, status=status.HTTP_200_OK)