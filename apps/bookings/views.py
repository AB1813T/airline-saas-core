from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Booking
from .serializers import BookingSerializer


@extend_schema_view(
    create=extend_schema(request=BookingSerializer, responses={201: BookingSerializer}),
    list=extend_schema(
        parameters=[
            OpenApiParameter("tenant_id", OpenApiTypes.STR, required=True, description="Tenant ID"),
        ],
        responses={200: BookingSerializer(many=True)}
    )
)
class BookingViewSet(ViewSet):
    """
    Create and view passenger bookings.
    """

    def create(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        booking = serializer.save()
        # We serialize the response manually to include read-only fields
        response_data = BookingSerializer(booking).data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request):
        tenant_id = request.query_params.get("tenant_id")
        if not tenant_id:
            return Response({"detail": "tenant_id is required"}, status=400)
            
        bookings = Booking.objects(tenant_id=tenant_id).order_by("-created_at")[:50]
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)