# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: foodchain.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='foodchain.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0f\x66oodchain.proto\"\x1b\n\x0bTransaction\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t20\n\x06Maketx\x12&\n\x06maketx\x12\x0c.Transaction\x1a\x0c.Transaction\"\x00\x62\x06proto3')
)




_TRANSACTION = _descriptor.Descriptor(
  name='Transaction',
  full_name='Transaction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Transaction.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=46,
)

DESCRIPTOR.message_types_by_name['Transaction'] = _TRANSACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), dict(
  DESCRIPTOR = _TRANSACTION,
  __module__ = 'foodchain_pb2'
  # @@protoc_insertion_point(class_scope:Transaction)
  ))
_sym_db.RegisterMessage(Transaction)



_MAKETX = _descriptor.ServiceDescriptor(
  name='Maketx',
  full_name='Maketx',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=48,
  serialized_end=96,
  methods=[
  _descriptor.MethodDescriptor(
    name='maketx',
    full_name='Maketx.maketx',
    index=0,
    containing_service=None,
    input_type=_TRANSACTION,
    output_type=_TRANSACTION,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MAKETX)

DESCRIPTOR.services_by_name['Maketx'] = _MAKETX

# @@protoc_insertion_point(module_scope)
