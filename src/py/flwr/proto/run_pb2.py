# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/run.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import transport_pb2 as flwr_dot_proto_dot_transport__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x66lwr/proto/run.proto\x12\nflwr.proto\x1a\x1a\x66lwr/proto/transport.proto\"\xd5\x01\n\x03Run\x12\x0e\n\x06run_id\x18\x01 \x01(\x12\x12\x0e\n\x06\x66\x61\x62_id\x18\x02 \x01(\t\x12\x13\n\x0b\x66\x61\x62_version\x18\x03 \x01(\t\x12<\n\x0foverride_config\x18\x04 \x03(\x0b\x32#.flwr.proto.Run.OverrideConfigEntry\x12\x10\n\x08\x66\x61\x62_hash\x18\x05 \x01(\t\x1aI\n\x13OverrideConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.flwr.proto.Scalar:\x02\x38\x01\"\x1f\n\rGetRunRequest\x12\x0e\n\x06run_id\x18\x01 \x01(\x12\".\n\x0eGetRunResponse\x12\x1c\n\x03run\x18\x01 \x01(\x0b\x32\x0f.flwr.proto.Runb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flwr.proto.run_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RUN_OVERRIDECONFIGENTRY']._options = None
  _globals['_RUN_OVERRIDECONFIGENTRY']._serialized_options = b'8\001'
  _globals['_RUN']._serialized_start=65
  _globals['_RUN']._serialized_end=278
  _globals['_RUN_OVERRIDECONFIGENTRY']._serialized_start=205
  _globals['_RUN_OVERRIDECONFIGENTRY']._serialized_end=278
  _globals['_GETRUNREQUEST']._serialized_start=280
  _globals['_GETRUNREQUEST']._serialized_end=311
  _globals['_GETRUNRESPONSE']._serialized_start=313
  _globals['_GETRUNRESPONSE']._serialized_end=359
# @@protoc_insertion_point(module_scope)
