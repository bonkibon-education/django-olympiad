# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: doc_service/api/proto/hospital.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'doc_service/api/proto/hospital.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$doc_service/api/proto/hospital.proto\"&\n\x0fHospitalRequest\x12\x13\n\x0bhospital_id\x18\x01 \x01(\x05\"6\n\x10HospitalResponse\x12\x13\n\x0bhospital_id\x18\x01 \x01(\x05\x12\r\n\x05valid\x18\x02 \x01(\x08\"5\n\x0bRoomRequest\x12\x13\n\x0bhospital_id\x18\x01 \x01(\x05\x12\x11\n\troom_name\x18\x02 \x01(\t\"E\n\x0cRoomResponse\x12\x13\n\x0bhospital_id\x18\x01 \x01(\x05\x12\x11\n\troom_name\x18\x02 \x01(\t\x12\r\n\x05valid\x18\x03 \x01(\x08\x32z\n\x12HospitalRpcService\x12\x37\n\x10ValidateHospital\x12\x10.HospitalRequest\x1a\x11.HospitalResponse\x12+\n\x0cValidateRoom\x12\x0c.RoomRequest\x1a\r.RoomResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'doc_service.api.proto.hospital_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HOSPITALREQUEST']._serialized_start=40
  _globals['_HOSPITALREQUEST']._serialized_end=78
  _globals['_HOSPITALRESPONSE']._serialized_start=80
  _globals['_HOSPITALRESPONSE']._serialized_end=134
  _globals['_ROOMREQUEST']._serialized_start=136
  _globals['_ROOMREQUEST']._serialized_end=189
  _globals['_ROOMRESPONSE']._serialized_start=191
  _globals['_ROOMRESPONSE']._serialized_end=260
  _globals['_HOSPITALRPCSERVICE']._serialized_start=262
  _globals['_HOSPITALRPCSERVICE']._serialized_end=384
# @@protoc_insertion_point(module_scope)
