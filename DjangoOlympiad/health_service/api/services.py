import logging

from django_grpc_framework import services

from django.contrib.auth import get_user_model
from .rpc_data_processors import data_process_hospital_or_room

logger = logging.getLogger(__name__)
User = get_user_model()


class HospitalGrpcService(services.Service):
    """
    gRPC service that allows to find Hospital & Room objects by hospital_id & maybe room_name
    """

    def ValidateHospital(self, request, context):
        """
        request: {"hospital_id": int}

        response: {"hospital_id": int, valid: bool}
        """
        result = data_process_hospital_or_room(request.hospital_id)
        logger.error(f"Validated hospital {request.hospital_id} --> {result}")
        return HospitalResponse(**result)

    def ValidateRoom(self, request, context):
        """
        request: {"hospital_id": int, "room_name": }

        response: {"hospital_id": int, valid: bool}
        """
        result = data_process_hospital_or_room(request.hospital_id, room_name=request.room_name)
        logger.error(f"Validated room {request.hospital_id}, {request.room_name} --> {result}")
        return RoomResponse(**result)
