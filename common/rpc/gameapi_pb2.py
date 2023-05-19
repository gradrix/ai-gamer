# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gameapi.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rgameapi.proto\"\'\n\x11PlayerNameRequest\x12\x12\n\nplayerName\x18\x01 \x01(\t\"I\n\x16RegisterPlayerResponse\x12/\n\x12registrationStatus\x18\x01 \x01(\x0e\x32\x13.PlayerRegistration\"\x19\n\x17GetPossibleMovesRequest\";\n\x18GetPossibleMovesResponse\x12\x1f\n\x05moves\x18\x01 \x03(\x0b\x32\x10.MoveCoordinates\"\'\n\x0fMoveCoordinates\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\"\x18\n\x16GetCurrentBoardRequest\"2\n\x17GetCurrentBoardResponse\x12\x17\n\x04grid\x18\x01 \x03(\x0b\x32\t.BoardRow\"\x19\n\x08\x42oardRow\x12\r\n\x05items\x18\x01 \x03(\x05\"6\n\x0f\x43\x61nMoveResponse\x12#\n\x0cplayerStatus\x18\x01 \x01(\x0e\x32\r.PlayerStatus\"0\n\x0bMoveRequest\x12\x12\n\nplayerName\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\x05\"9\n\x0cMoveResponse\x12\x1b\n\x06status\x18\x01 \x01(\x0e\x32\x0b.MoveStatus\x12\x0c\n\x04move\x18\x02 \x01(\t\"\x13\n\x11KeepAliveResponse*_\n\x12PlayerRegistration\x12\x18\n\x14REGISTRATION_SUCCESS\x10\x00\x12\x17\n\x13NO_PLAYER_SLOT_LEFT\x10\x01\x12\x16\n\x12\x41LREADY_REGISTERED\x10\x02*\\\n\x0cPlayerStatus\x12\x07\n\x03WON\x10\x00\x12\x08\n\x04LOST\x10\x01\x12\x08\n\x04\x44RAW\x10\x02\x12\x0c\n\x08\x43\x41N_MOVE\x10\x03\x12\x08\n\x04WAIT\x10\x04\x12\x17\n\x13UNREGISTERED_PLAYER\x10\x05*8\n\nMoveStatus\x12\x10\n\x0cMOVE_SUCCESS\x10\x00\x12\r\n\tINCORRECT\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x32\xee\x02\n\x07GameApi\x12?\n\x0eregisterPlayer\x12\x12.PlayerNameRequest\x1a\x17.RegisterPlayerResponse\"\x00\x12I\n\x10getPossibleMoves\x12\x18.GetPossibleMovesRequest\x1a\x19.GetPossibleMovesResponse\"\x00\x12\x46\n\x0fgetCurrentBoard\x12\x17.GetCurrentBoardRequest\x1a\x18.GetCurrentBoardResponse\"\x00\x12\x31\n\x07\x63\x61nMove\x12\x12.PlayerNameRequest\x1a\x10.CanMoveResponse\"\x00\x12%\n\x04move\x12\x0c.MoveRequest\x1a\r.MoveResponse\"\x00\x12\x35\n\tkeepAlive\x12\x12.PlayerNameRequest\x1a\x12.KeepAliveResponse\"\x00\x62\x06proto3')

_PLAYERREGISTRATION = DESCRIPTOR.enum_types_by_name['PlayerRegistration']
PlayerRegistration = enum_type_wrapper.EnumTypeWrapper(_PLAYERREGISTRATION)
_PLAYERSTATUS = DESCRIPTOR.enum_types_by_name['PlayerStatus']
PlayerStatus = enum_type_wrapper.EnumTypeWrapper(_PLAYERSTATUS)
_MOVESTATUS = DESCRIPTOR.enum_types_by_name['MoveStatus']
MoveStatus = enum_type_wrapper.EnumTypeWrapper(_MOVESTATUS)
REGISTRATION_SUCCESS = 0
NO_PLAYER_SLOT_LEFT = 1
ALREADY_REGISTERED = 2
WON = 0
LOST = 1
DRAW = 2
CAN_MOVE = 3
WAIT = 4
UNREGISTERED_PLAYER = 5
MOVE_SUCCESS = 0
INCORRECT = 1
ERROR = 2


_PLAYERNAMEREQUEST = DESCRIPTOR.message_types_by_name['PlayerNameRequest']
_REGISTERPLAYERRESPONSE = DESCRIPTOR.message_types_by_name['RegisterPlayerResponse']
_GETPOSSIBLEMOVESREQUEST = DESCRIPTOR.message_types_by_name['GetPossibleMovesRequest']
_GETPOSSIBLEMOVESRESPONSE = DESCRIPTOR.message_types_by_name['GetPossibleMovesResponse']
_MOVECOORDINATES = DESCRIPTOR.message_types_by_name['MoveCoordinates']
_GETCURRENTBOARDREQUEST = DESCRIPTOR.message_types_by_name['GetCurrentBoardRequest']
_GETCURRENTBOARDRESPONSE = DESCRIPTOR.message_types_by_name['GetCurrentBoardResponse']
_BOARDROW = DESCRIPTOR.message_types_by_name['BoardRow']
_CANMOVERESPONSE = DESCRIPTOR.message_types_by_name['CanMoveResponse']
_MOVEREQUEST = DESCRIPTOR.message_types_by_name['MoveRequest']
_MOVERESPONSE = DESCRIPTOR.message_types_by_name['MoveResponse']
_KEEPALIVERESPONSE = DESCRIPTOR.message_types_by_name['KeepAliveResponse']
PlayerNameRequest = _reflection.GeneratedProtocolMessageType('PlayerNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERNAMEREQUEST,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:PlayerNameRequest)
  })
_sym_db.RegisterMessage(PlayerNameRequest)

RegisterPlayerResponse = _reflection.GeneratedProtocolMessageType('RegisterPlayerResponse', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERPLAYERRESPONSE,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:RegisterPlayerResponse)
  })
_sym_db.RegisterMessage(RegisterPlayerResponse)

GetPossibleMovesRequest = _reflection.GeneratedProtocolMessageType('GetPossibleMovesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPOSSIBLEMOVESREQUEST,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:GetPossibleMovesRequest)
  })
_sym_db.RegisterMessage(GetPossibleMovesRequest)

GetPossibleMovesResponse = _reflection.GeneratedProtocolMessageType('GetPossibleMovesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETPOSSIBLEMOVESRESPONSE,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:GetPossibleMovesResponse)
  })
_sym_db.RegisterMessage(GetPossibleMovesResponse)

MoveCoordinates = _reflection.GeneratedProtocolMessageType('MoveCoordinates', (_message.Message,), {
  'DESCRIPTOR' : _MOVECOORDINATES,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:MoveCoordinates)
  })
_sym_db.RegisterMessage(MoveCoordinates)

GetCurrentBoardRequest = _reflection.GeneratedProtocolMessageType('GetCurrentBoardRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCURRENTBOARDREQUEST,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:GetCurrentBoardRequest)
  })
_sym_db.RegisterMessage(GetCurrentBoardRequest)

GetCurrentBoardResponse = _reflection.GeneratedProtocolMessageType('GetCurrentBoardResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCURRENTBOARDRESPONSE,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:GetCurrentBoardResponse)
  })
_sym_db.RegisterMessage(GetCurrentBoardResponse)

BoardRow = _reflection.GeneratedProtocolMessageType('BoardRow', (_message.Message,), {
  'DESCRIPTOR' : _BOARDROW,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:BoardRow)
  })
_sym_db.RegisterMessage(BoardRow)

CanMoveResponse = _reflection.GeneratedProtocolMessageType('CanMoveResponse', (_message.Message,), {
  'DESCRIPTOR' : _CANMOVERESPONSE,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:CanMoveResponse)
  })
_sym_db.RegisterMessage(CanMoveResponse)

MoveRequest = _reflection.GeneratedProtocolMessageType('MoveRequest', (_message.Message,), {
  'DESCRIPTOR' : _MOVEREQUEST,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:MoveRequest)
  })
_sym_db.RegisterMessage(MoveRequest)

MoveResponse = _reflection.GeneratedProtocolMessageType('MoveResponse', (_message.Message,), {
  'DESCRIPTOR' : _MOVERESPONSE,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:MoveResponse)
  })
_sym_db.RegisterMessage(MoveResponse)

KeepAliveResponse = _reflection.GeneratedProtocolMessageType('KeepAliveResponse', (_message.Message,), {
  'DESCRIPTOR' : _KEEPALIVERESPONSE,
  '__module__' : 'gameapi_pb2'
  # @@protoc_insertion_point(class_scope:KeepAliveResponse)
  })
_sym_db.RegisterMessage(KeepAliveResponse)

_GAMEAPI = DESCRIPTOR.services_by_name['GameApi']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PLAYERREGISTRATION._serialized_start=553
  _PLAYERREGISTRATION._serialized_end=648
  _PLAYERSTATUS._serialized_start=650
  _PLAYERSTATUS._serialized_end=742
  _MOVESTATUS._serialized_start=744
  _MOVESTATUS._serialized_end=800
  _PLAYERNAMEREQUEST._serialized_start=17
  _PLAYERNAMEREQUEST._serialized_end=56
  _REGISTERPLAYERRESPONSE._serialized_start=58
  _REGISTERPLAYERRESPONSE._serialized_end=131
  _GETPOSSIBLEMOVESREQUEST._serialized_start=133
  _GETPOSSIBLEMOVESREQUEST._serialized_end=158
  _GETPOSSIBLEMOVESRESPONSE._serialized_start=160
  _GETPOSSIBLEMOVESRESPONSE._serialized_end=219
  _MOVECOORDINATES._serialized_start=221
  _MOVECOORDINATES._serialized_end=260
  _GETCURRENTBOARDREQUEST._serialized_start=262
  _GETCURRENTBOARDREQUEST._serialized_end=286
  _GETCURRENTBOARDRESPONSE._serialized_start=288
  _GETCURRENTBOARDRESPONSE._serialized_end=338
  _BOARDROW._serialized_start=340
  _BOARDROW._serialized_end=365
  _CANMOVERESPONSE._serialized_start=367
  _CANMOVERESPONSE._serialized_end=421
  _MOVEREQUEST._serialized_start=423
  _MOVEREQUEST._serialized_end=471
  _MOVERESPONSE._serialized_start=473
  _MOVERESPONSE._serialized_end=530
  _KEEPALIVERESPONSE._serialized_start=532
  _KEEPALIVERESPONSE._serialized_end=551
  _GAMEAPI._serialized_start=803
  _GAMEAPI._serialized_end=1169
# @@protoc_insertion_point(module_scope)