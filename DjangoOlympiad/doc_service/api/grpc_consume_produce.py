import grpc
import logging
from django.conf import settings
from .proto import account_pb2, account_pb2_grpc, hospital_pb2, hospital_pb2_grpc

GRPC_PORT_ACCOUNT = settings.GRPC_PORT_ACCOUNT
GRPC_PORT_HOSPITAL = settings.GRPC_PORT_HOSPITAL
logger = logging.getLogger(__name__)

def grpc_user_by_jwt(raw_token):
    try:
        with grpc.secure_channel("auth_service:50051", grpc.ssl_channel_credentials()) as channel:
            client = account_pb2_grpc.AccountRpcServiceStub(channel)
            request = account_pb2.JWTRequest(jwt=raw_token)
            response = client.ValidateJWT(request)
            return getattr(response, "user", None)
    except grpc.RpcError as e:
        logging.error(f"gRPC connection error in grpc_user_by_jwt: {e.code()} - {e.details()}")
        return None

def grpc_check_roles(user_id, role=None):
    try:
        with grpc.secure_channel(f"auth_service:{GRPC_PORT_ACCOUNT}", grpc.ssl_channel_credentials()) as channel:
            client = account_pb2_grpc.AccountRpcServiceStub(channel)
            request = account_pb2.UserRequest(user_id=user_id, role=role)
            response = client.ValidateUser(request)
            user = getattr(response, "user", None)
            return user, response.valid
    except grpc.RpcError as e:
        logger.error(f"gRPC ERROR IN grpc_check_roles (user_id = {user_id}, role = {role}): {e.code()} - {e.details()}")
        return None, False

def grpc_check_hospital(hospital_id):
    try:
        with grpc.secure_channel(f"health_service:{GRPC_PORT_HOSPITAL}", grpc.ssl_channel_credentials()) as channel:
            client = hospital_pb2_grpc.HospitalRpcServiceStub(channel)
            request = hospital_pb2.HospitalRequest(hospital_id=hospital_id)
            response = client.ValidateHospital(request)
            valid = getattr(response, "valid", False)
            return valid
    except grpc.RpcError as e:
        logger.error(f"gRPC ERROR IN grpc_check_hospital (hospital_id = {hospital_id}): {e.code()} - {e.details()}")
        return False

def grpc_check_room(hospital_id, room_name):
    try:
        with grpc.secure_channel(f"health_service:{GRPC_PORT_HOSPITAL}", grpc.ssl_channel_credentials()) as channel:
            client = hospital_pb2_grpc.HospitalRpcServiceStub(channel)
            request = hospital_pb2.RoomRequest(hospital_id=hospital_id, room_name=room_name)
            response = client.ValidateRoom(request)
            valid = getattr(response, "valid", False)
            return valid
    except grpc.RpcError as e:
        logger.error(f"gRPC ERROR IN grpc_check_room (hospital_id = {hospital_id}, room_name = {room_name}): {e.code()} - {e.details()}")
        return False
