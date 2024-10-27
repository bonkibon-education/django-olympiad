import json

from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..permissions import IsAdminUserWithRole
from ..serializers import CustomUserSerializer, CustomUserSerializerWithRole

User = get_user_model()


class MeView(GenericAPIView):
    """
    Current account details endpoint
    GET /api/Accounts/Me
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    allowed_methods = ["get"]
    serializer_class = CustomUserSerializer

    def get(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)


class UpdateAccountView(GenericAPIView):
    """
    Current account update endpoint
    PUT /api/Accounts/Update
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']
    allowed_methods = ["put"]
    serializer_class = CustomUserSerializer
    lookup_field = "id"

    def put(self, request):
        put_data = request.data

        last_name = put_data.get("surname")
        first_name = put_data.get("firstName")
        password = put_data.get("password")

        if not (last_name and first_name and password):
            return Response({"details": "surname, firstName and password are required!"},
                            status=status.HTTP_400_BAD_REQUEST)

        data = {"surname": last_name, "firstName": first_name, "password": password}

        serializer = self.serializer_class(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    accounts=extend_schema(
        parameters=[
            OpenApiParameter(name='from', description='Selection start (not by id!)',
                             type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='count', description='How many users to return?',
                             type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        ]
    )
)
class AdminAccountsViewSet(ModelViewSet):
    """
    ViewSet for admin accounts CRUD with role creation support
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializerWithRole
    permission_classes = [IsAdminUserWithRole]
    lookup_field = "id"

    @action(detail=False, methods=['get'], name="accounts")
    def accounts(self, request):
        """
        Accounts list endpoint (from and count are query params, they limit the performed selection)

        GET /api/Accounts?from=&count=
        """
        from_ = request.query_params.get('from', None)
        count = request.query_params.get('count', None)
        accounts = User.objects.all()

        errors = []

        if from_ is not None:
            from_ = int(from_)
            if from_ < 0:
                errors.append({"from": "from parameter must be either None or non-negative!"})
            else:
                accounts = accounts[int(from_):]
        if count is not None:
            count = int(count)
            if count < 0:
                errors.append({"count": "count parameter must be either None or non-negative!"})
            else:
                accounts = accounts[: int(count)]
        if not errors:
            serializer = self.serializer_class(accounts, many=True)
            return Response(serializer.data)
        else:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        Endpoint for creating a User with a role
        POST /api/Accounts
        """
        put_data = request.data
        role_name = put_data.pop('role', None)

        if role_name:
            request.data['role'] = {"name": role_name}  # Format role correctly for serializer

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Endpoint for updating a User with a role
        PUT /api/Accounts/{id}
        """
        put_data = request.data
        role_name = put_data.pop('role', None)

        if role_name:
            request.data['role'] = {"name": role_name}  # Format role correctly for serializer

        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.soft_delete()
