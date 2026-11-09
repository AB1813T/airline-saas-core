from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist, NotUniqueError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Flight
from .serializers import FlightSerializer

# This decorator tells Swagger how to render the API docs
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("tenant_id", OpenApiTypes.STR, description="Filter by tenant ID"),
            OpenApiParameter("origin", OpenApiTypes.STR, description="Origin airport code (e.g. DAC)"),
            OpenApiParameter("destination", OpenApiTypes.STR, description="Destination code (e.g. DXB)"),
            OpenApiParameter("departure_from", OpenApiTypes.DATETIME, description="Departure after this date"),
            OpenApiParameter("departure_to", OpenApiTypes.DATETIME, description="Departure before this date"),
        ],
        responses={200: FlightSerializer(many=True)}
    ),
    create=extend_schema(
        request=FlightSerializer, 
        responses={201: FlightSerializer}
    ),
    retrieve=extend_schema(
        responses={200: FlightSerializer}
    )
)
class FlightViewSet(ViewSet):
    """
    Flight search & CRUD.
    """

    def list(self, request):
        # Start with active flights only
        q = Flight.objects(is_active=True)

        # Apply query parameter filters if provided
        tenant_id      = request.query_params.get("tenant_id")
        origin         = request.query_params.get("origin")
        destination    = request.query_params.get("destination")
        departure_from = request.query_params.get("departure_from")
        departure_to   = request.query_params.get("departure_to")

        if tenant_id:      q = q.filter(tenant_id=tenant_id)
        if origin:         q = q.filter(origin__iexact=origin)
        if destination:    q = q.filter(destination__iexact=destination)
        if departure_from: q = q.filter(departure_at__gte=departure_from)
        if departure_to:   q = q.filter(departure_at__lte=departure_to)

        # Order by departure and limit results for safety
        flights = q.order_by("departure_at")[:100]
        
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FlightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            flight = serializer.save()
            return Response(
                FlightSerializer(flight).data, 
                status=status.HTTP_201_CREATED
            )
        except NotUniqueError:
            return Response(
                {"detail": "Duplicate flight"}, 
                status=status.HTTP_409_CONFLICT
            )

    def retrieve(self, request, pk=None):
        try:
            flight = Flight.objects.get(id=pk, is_active=True)
        except (DoesNotExist, Exception):
            return Response(
                {"detail": "Flight not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = FlightSerializer(flight)
        return Response(serializer.data)