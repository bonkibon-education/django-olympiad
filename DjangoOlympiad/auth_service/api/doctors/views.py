from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.functions import Concat
from ..serializers import CustomUserSerializer

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter("from", description="Selection start (not by ID!)",
                             type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter("count", description="Selection size (not by ID!)",
                             type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter("nameFilter", description="Full name filter (fullName = BOTH firstName + "
                                                       "surname AND surname + firstName)",
                             type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ]
    )
)
class DoctorsListView(ListAPIView):
    """
    Doctors list endpoint. Basically, it's just the users list but with the Doctor role.
    GET /api/Doctors
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    allowed_methods = ["get"]

    def get_queryset(self):
        from_index = int(self.request.query_params.get('from', 0))
        count = int(self.request.query_params.get('count', 10))
        name_filter = self.request.query_params.get("nameFilter", "").replace(' ', '')

        found_queryset = (User.objects
                          .filter(role__name="Doctor")  # Updated to check the single role
                          .annotate(full_name_1=Concat('last_name', 'first_name'))
                          .annotate(full_name_2=Concat('first_name', 'last_name'))
                          .filter(Q(full_name_1__icontains=name_filter) | Q(full_name_2__icontains=name_filter)))

        return found_queryset[from_index:from_index + count]  # Apply the slice to limit results


class DoctorByIdView(RetrieveAPIView):
    """
    Doctor details endpoint. Basically, it's just the user-by-id but with the Doctor role.
    GET /api/Doctors/{id}
    """
    serializer_class = CustomUserSerializer
    queryset = User.objects.filter(role__name="Doctor")  # Updated to check the single role
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    allowed_methods = ["get"]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
