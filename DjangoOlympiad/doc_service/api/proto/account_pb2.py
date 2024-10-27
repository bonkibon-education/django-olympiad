# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: doc_service/api/proto/account.proto
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
    'doc_service/api/proto/account.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#doc_service/api/proto/account.proto\"b\n\x0eUserSerialized\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tfirstName\x18\x02 \x01(\t\x12\x10\n\x08lastName\x18\x03 \x01(\t\x12\x10\n\x08username\x18\x04 \x01(\t\x12\r\n\x05roles\x18\x05 \x03(\t\"\x19\n\nJWTRequest\x12\x0b\n\x03jwt\x18\x01 \x01(\t\"G\n\x0bJWTResponse\x12\x0b\n\x03jwt\x18\x01 \x01(\t\x12\"\n\x04user\x18\x02 \x01(\x0b\x32\x0f.UserSerializedH\x00\x88\x01\x01\x42\x07\n\x05_user\":\n\x0bUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x11\n\x04role\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x07\n\x05_role\"w\n\x0cUserResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x11\n\x04role\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\"\n\x04user\x18\x03 \x01(\x0b\x32\x0f.UserSerializedH\x01\x88\x01\x01\x12\r\n\x05valid\x18\x04 \x01(\x08\x42\x07\n\x05_roleB\x07\n\x05_user2j\n\x11\x41\x63\x63ountRpcService\x12(\n\x0bValidateJWT\x12\x0b.JWTRequest\x1a\x0c.JWTResponse\x12+\n\x0cValidateUser\x12\x0c.UserRequest\x1a\r.UserResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'doc_service.api.proto.account_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USERSERIALIZED']._serialized_start=39
  _globals['_USERSERIALIZED']._serialized_end=137
  _globals['_JWTREQUEST']._serialized_start=139
  _globals['_JWTREQUEST']._serialized_end=164
  _globals['_JWTRESPONSE']._serialized_start=166
  _globals['_JWTRESPONSE']._serialized_end=237
  _globals['_USERREQUEST']._serialized_start=239
  _globals['_USERREQUEST']._serialized_end=297
  _globals['_USERRESPONSE']._serialized_start=299
  _globals['_USERRESPONSE']._serialized_end=418
  _globals['_ACCOUNTRPCSERVICE']._serialized_start=420
  _globals['_ACCOUNTRPCSERVICE']._serialized_end=526
# @@protoc_insertion_point(module_scope)