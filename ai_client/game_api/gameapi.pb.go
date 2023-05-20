// Code generated by protoc-gen-go. DO NOT EDIT.
// source: gameapi.proto

package game_api

import (
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

type PlayerRegistration int32

const (
	PlayerRegistration_REGISTRATION_SUCCESS PlayerRegistration = 0
	PlayerRegistration_NO_PLAYER_SLOT_LEFT  PlayerRegistration = 1
	PlayerRegistration_ALREADY_REGISTERED   PlayerRegistration = 2
)

var PlayerRegistration_name = map[int32]string{
	0: "REGISTRATION_SUCCESS",
	1: "NO_PLAYER_SLOT_LEFT",
	2: "ALREADY_REGISTERED",
}

var PlayerRegistration_value = map[string]int32{
	"REGISTRATION_SUCCESS": 0,
	"NO_PLAYER_SLOT_LEFT":  1,
	"ALREADY_REGISTERED":   2,
}

func (x PlayerRegistration) String() string {
	return proto.EnumName(PlayerRegistration_name, int32(x))
}

func (PlayerRegistration) EnumDescriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{0}
}

type PlayerStatus int32

const (
	PlayerStatus_WON                 PlayerStatus = 0
	PlayerStatus_LOST                PlayerStatus = 1
	PlayerStatus_DRAW                PlayerStatus = 2
	PlayerStatus_CAN_MOVE            PlayerStatus = 3
	PlayerStatus_WAIT                PlayerStatus = 4
	PlayerStatus_UNREGISTERED_PLAYER PlayerStatus = 5
)

var PlayerStatus_name = map[int32]string{
	0: "WON",
	1: "LOST",
	2: "DRAW",
	3: "CAN_MOVE",
	4: "WAIT",
	5: "UNREGISTERED_PLAYER",
}

var PlayerStatus_value = map[string]int32{
	"WON":                 0,
	"LOST":                1,
	"DRAW":                2,
	"CAN_MOVE":            3,
	"WAIT":                4,
	"UNREGISTERED_PLAYER": 5,
}

func (x PlayerStatus) String() string {
	return proto.EnumName(PlayerStatus_name, int32(x))
}

func (PlayerStatus) EnumDescriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{1}
}

type MoveStatus int32

const (
	MoveStatus_MOVE_SUCCESS MoveStatus = 0
	MoveStatus_INCORRECT    MoveStatus = 1
	MoveStatus_ERROR        MoveStatus = 2
)

var MoveStatus_name = map[int32]string{
	0: "MOVE_SUCCESS",
	1: "INCORRECT",
	2: "ERROR",
}

var MoveStatus_value = map[string]int32{
	"MOVE_SUCCESS": 0,
	"INCORRECT":    1,
	"ERROR":        2,
}

func (x MoveStatus) String() string {
	return proto.EnumName(MoveStatus_name, int32(x))
}

func (MoveStatus) EnumDescriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{2}
}

type PlayerNameRequest struct {
	PlayerName           string   `protobuf:"bytes,1,opt,name=playerName,proto3" json:"playerName,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *PlayerNameRequest) Reset()         { *m = PlayerNameRequest{} }
func (m *PlayerNameRequest) String() string { return proto.CompactTextString(m) }
func (*PlayerNameRequest) ProtoMessage()    {}
func (*PlayerNameRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{0}
}

func (m *PlayerNameRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_PlayerNameRequest.Unmarshal(m, b)
}
func (m *PlayerNameRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_PlayerNameRequest.Marshal(b, m, deterministic)
}
func (m *PlayerNameRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_PlayerNameRequest.Merge(m, src)
}
func (m *PlayerNameRequest) XXX_Size() int {
	return xxx_messageInfo_PlayerNameRequest.Size(m)
}
func (m *PlayerNameRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_PlayerNameRequest.DiscardUnknown(m)
}

var xxx_messageInfo_PlayerNameRequest proto.InternalMessageInfo

func (m *PlayerNameRequest) GetPlayerName() string {
	if m != nil {
		return m.PlayerName
	}
	return ""
}

type RegisterPlayerResponse struct {
	RegistrationStatus   PlayerRegistration `protobuf:"varint,1,opt,name=registrationStatus,proto3,enum=game_api.PlayerRegistration" json:"registrationStatus,omitempty"`
	XXX_NoUnkeyedLiteral struct{}           `json:"-"`
	XXX_unrecognized     []byte             `json:"-"`
	XXX_sizecache        int32              `json:"-"`
}

func (m *RegisterPlayerResponse) Reset()         { *m = RegisterPlayerResponse{} }
func (m *RegisterPlayerResponse) String() string { return proto.CompactTextString(m) }
func (*RegisterPlayerResponse) ProtoMessage()    {}
func (*RegisterPlayerResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{1}
}

func (m *RegisterPlayerResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_RegisterPlayerResponse.Unmarshal(m, b)
}
func (m *RegisterPlayerResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_RegisterPlayerResponse.Marshal(b, m, deterministic)
}
func (m *RegisterPlayerResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_RegisterPlayerResponse.Merge(m, src)
}
func (m *RegisterPlayerResponse) XXX_Size() int {
	return xxx_messageInfo_RegisterPlayerResponse.Size(m)
}
func (m *RegisterPlayerResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_RegisterPlayerResponse.DiscardUnknown(m)
}

var xxx_messageInfo_RegisterPlayerResponse proto.InternalMessageInfo

func (m *RegisterPlayerResponse) GetRegistrationStatus() PlayerRegistration {
	if m != nil {
		return m.RegistrationStatus
	}
	return PlayerRegistration_REGISTRATION_SUCCESS
}

type GetPossibleMovesRequest struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *GetPossibleMovesRequest) Reset()         { *m = GetPossibleMovesRequest{} }
func (m *GetPossibleMovesRequest) String() string { return proto.CompactTextString(m) }
func (*GetPossibleMovesRequest) ProtoMessage()    {}
func (*GetPossibleMovesRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{2}
}

func (m *GetPossibleMovesRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetPossibleMovesRequest.Unmarshal(m, b)
}
func (m *GetPossibleMovesRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetPossibleMovesRequest.Marshal(b, m, deterministic)
}
func (m *GetPossibleMovesRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetPossibleMovesRequest.Merge(m, src)
}
func (m *GetPossibleMovesRequest) XXX_Size() int {
	return xxx_messageInfo_GetPossibleMovesRequest.Size(m)
}
func (m *GetPossibleMovesRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_GetPossibleMovesRequest.DiscardUnknown(m)
}

var xxx_messageInfo_GetPossibleMovesRequest proto.InternalMessageInfo

type GetPossibleMovesResponse struct {
	Moves                []*MoveCoordinates `protobuf:"bytes,1,rep,name=moves,proto3" json:"moves,omitempty"`
	XXX_NoUnkeyedLiteral struct{}           `json:"-"`
	XXX_unrecognized     []byte             `json:"-"`
	XXX_sizecache        int32              `json:"-"`
}

func (m *GetPossibleMovesResponse) Reset()         { *m = GetPossibleMovesResponse{} }
func (m *GetPossibleMovesResponse) String() string { return proto.CompactTextString(m) }
func (*GetPossibleMovesResponse) ProtoMessage()    {}
func (*GetPossibleMovesResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{3}
}

func (m *GetPossibleMovesResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetPossibleMovesResponse.Unmarshal(m, b)
}
func (m *GetPossibleMovesResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetPossibleMovesResponse.Marshal(b, m, deterministic)
}
func (m *GetPossibleMovesResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetPossibleMovesResponse.Merge(m, src)
}
func (m *GetPossibleMovesResponse) XXX_Size() int {
	return xxx_messageInfo_GetPossibleMovesResponse.Size(m)
}
func (m *GetPossibleMovesResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_GetPossibleMovesResponse.DiscardUnknown(m)
}

var xxx_messageInfo_GetPossibleMovesResponse proto.InternalMessageInfo

func (m *GetPossibleMovesResponse) GetMoves() []*MoveCoordinates {
	if m != nil {
		return m.Moves
	}
	return nil
}

type MoveCoordinates struct {
	X                    int32    `protobuf:"varint,1,opt,name=x,proto3" json:"x,omitempty"`
	Y                    int32    `protobuf:"varint,2,opt,name=y,proto3" json:"y,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *MoveCoordinates) Reset()         { *m = MoveCoordinates{} }
func (m *MoveCoordinates) String() string { return proto.CompactTextString(m) }
func (*MoveCoordinates) ProtoMessage()    {}
func (*MoveCoordinates) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{4}
}

func (m *MoveCoordinates) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MoveCoordinates.Unmarshal(m, b)
}
func (m *MoveCoordinates) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MoveCoordinates.Marshal(b, m, deterministic)
}
func (m *MoveCoordinates) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MoveCoordinates.Merge(m, src)
}
func (m *MoveCoordinates) XXX_Size() int {
	return xxx_messageInfo_MoveCoordinates.Size(m)
}
func (m *MoveCoordinates) XXX_DiscardUnknown() {
	xxx_messageInfo_MoveCoordinates.DiscardUnknown(m)
}

var xxx_messageInfo_MoveCoordinates proto.InternalMessageInfo

func (m *MoveCoordinates) GetX() int32 {
	if m != nil {
		return m.X
	}
	return 0
}

func (m *MoveCoordinates) GetY() int32 {
	if m != nil {
		return m.Y
	}
	return 0
}

type GetCurrentBoardRequest struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *GetCurrentBoardRequest) Reset()         { *m = GetCurrentBoardRequest{} }
func (m *GetCurrentBoardRequest) String() string { return proto.CompactTextString(m) }
func (*GetCurrentBoardRequest) ProtoMessage()    {}
func (*GetCurrentBoardRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{5}
}

func (m *GetCurrentBoardRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetCurrentBoardRequest.Unmarshal(m, b)
}
func (m *GetCurrentBoardRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetCurrentBoardRequest.Marshal(b, m, deterministic)
}
func (m *GetCurrentBoardRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetCurrentBoardRequest.Merge(m, src)
}
func (m *GetCurrentBoardRequest) XXX_Size() int {
	return xxx_messageInfo_GetCurrentBoardRequest.Size(m)
}
func (m *GetCurrentBoardRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_GetCurrentBoardRequest.DiscardUnknown(m)
}

var xxx_messageInfo_GetCurrentBoardRequest proto.InternalMessageInfo

type GetCurrentBoardResponse struct {
	Grid                 []*BoardRow `protobuf:"bytes,1,rep,name=grid,proto3" json:"grid,omitempty"`
	XXX_NoUnkeyedLiteral struct{}    `json:"-"`
	XXX_unrecognized     []byte      `json:"-"`
	XXX_sizecache        int32       `json:"-"`
}

func (m *GetCurrentBoardResponse) Reset()         { *m = GetCurrentBoardResponse{} }
func (m *GetCurrentBoardResponse) String() string { return proto.CompactTextString(m) }
func (*GetCurrentBoardResponse) ProtoMessage()    {}
func (*GetCurrentBoardResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{6}
}

func (m *GetCurrentBoardResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetCurrentBoardResponse.Unmarshal(m, b)
}
func (m *GetCurrentBoardResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetCurrentBoardResponse.Marshal(b, m, deterministic)
}
func (m *GetCurrentBoardResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetCurrentBoardResponse.Merge(m, src)
}
func (m *GetCurrentBoardResponse) XXX_Size() int {
	return xxx_messageInfo_GetCurrentBoardResponse.Size(m)
}
func (m *GetCurrentBoardResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_GetCurrentBoardResponse.DiscardUnknown(m)
}

var xxx_messageInfo_GetCurrentBoardResponse proto.InternalMessageInfo

func (m *GetCurrentBoardResponse) GetGrid() []*BoardRow {
	if m != nil {
		return m.Grid
	}
	return nil
}

type BoardRow struct {
	Items                []int32  `protobuf:"varint,1,rep,packed,name=items,proto3" json:"items,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *BoardRow) Reset()         { *m = BoardRow{} }
func (m *BoardRow) String() string { return proto.CompactTextString(m) }
func (*BoardRow) ProtoMessage()    {}
func (*BoardRow) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{7}
}

func (m *BoardRow) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_BoardRow.Unmarshal(m, b)
}
func (m *BoardRow) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_BoardRow.Marshal(b, m, deterministic)
}
func (m *BoardRow) XXX_Merge(src proto.Message) {
	xxx_messageInfo_BoardRow.Merge(m, src)
}
func (m *BoardRow) XXX_Size() int {
	return xxx_messageInfo_BoardRow.Size(m)
}
func (m *BoardRow) XXX_DiscardUnknown() {
	xxx_messageInfo_BoardRow.DiscardUnknown(m)
}

var xxx_messageInfo_BoardRow proto.InternalMessageInfo

func (m *BoardRow) GetItems() []int32 {
	if m != nil {
		return m.Items
	}
	return nil
}

type CanMoveResponse struct {
	PlayerStatus         PlayerStatus `protobuf:"varint,1,opt,name=playerStatus,proto3,enum=game_api.PlayerStatus" json:"playerStatus,omitempty"`
	XXX_NoUnkeyedLiteral struct{}     `json:"-"`
	XXX_unrecognized     []byte       `json:"-"`
	XXX_sizecache        int32        `json:"-"`
}

func (m *CanMoveResponse) Reset()         { *m = CanMoveResponse{} }
func (m *CanMoveResponse) String() string { return proto.CompactTextString(m) }
func (*CanMoveResponse) ProtoMessage()    {}
func (*CanMoveResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{8}
}

func (m *CanMoveResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_CanMoveResponse.Unmarshal(m, b)
}
func (m *CanMoveResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_CanMoveResponse.Marshal(b, m, deterministic)
}
func (m *CanMoveResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_CanMoveResponse.Merge(m, src)
}
func (m *CanMoveResponse) XXX_Size() int {
	return xxx_messageInfo_CanMoveResponse.Size(m)
}
func (m *CanMoveResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_CanMoveResponse.DiscardUnknown(m)
}

var xxx_messageInfo_CanMoveResponse proto.InternalMessageInfo

func (m *CanMoveResponse) GetPlayerStatus() PlayerStatus {
	if m != nil {
		return m.PlayerStatus
	}
	return PlayerStatus_WON
}

type MoveRequest struct {
	PlayerName           string   `protobuf:"bytes,1,opt,name=playerName,proto3" json:"playerName,omitempty"`
	Index                int32    `protobuf:"varint,2,opt,name=index,proto3" json:"index,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *MoveRequest) Reset()         { *m = MoveRequest{} }
func (m *MoveRequest) String() string { return proto.CompactTextString(m) }
func (*MoveRequest) ProtoMessage()    {}
func (*MoveRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{9}
}

func (m *MoveRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MoveRequest.Unmarshal(m, b)
}
func (m *MoveRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MoveRequest.Marshal(b, m, deterministic)
}
func (m *MoveRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MoveRequest.Merge(m, src)
}
func (m *MoveRequest) XXX_Size() int {
	return xxx_messageInfo_MoveRequest.Size(m)
}
func (m *MoveRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_MoveRequest.DiscardUnknown(m)
}

var xxx_messageInfo_MoveRequest proto.InternalMessageInfo

func (m *MoveRequest) GetPlayerName() string {
	if m != nil {
		return m.PlayerName
	}
	return ""
}

func (m *MoveRequest) GetIndex() int32 {
	if m != nil {
		return m.Index
	}
	return 0
}

type MoveResponse struct {
	Status               MoveStatus `protobuf:"varint,1,opt,name=status,proto3,enum=game_api.MoveStatus" json:"status,omitempty"`
	Move                 string     `protobuf:"bytes,2,opt,name=move,proto3" json:"move,omitempty"`
	XXX_NoUnkeyedLiteral struct{}   `json:"-"`
	XXX_unrecognized     []byte     `json:"-"`
	XXX_sizecache        int32      `json:"-"`
}

func (m *MoveResponse) Reset()         { *m = MoveResponse{} }
func (m *MoveResponse) String() string { return proto.CompactTextString(m) }
func (*MoveResponse) ProtoMessage()    {}
func (*MoveResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{10}
}

func (m *MoveResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MoveResponse.Unmarshal(m, b)
}
func (m *MoveResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MoveResponse.Marshal(b, m, deterministic)
}
func (m *MoveResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MoveResponse.Merge(m, src)
}
func (m *MoveResponse) XXX_Size() int {
	return xxx_messageInfo_MoveResponse.Size(m)
}
func (m *MoveResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_MoveResponse.DiscardUnknown(m)
}

var xxx_messageInfo_MoveResponse proto.InternalMessageInfo

func (m *MoveResponse) GetStatus() MoveStatus {
	if m != nil {
		return m.Status
	}
	return MoveStatus_MOVE_SUCCESS
}

func (m *MoveResponse) GetMove() string {
	if m != nil {
		return m.Move
	}
	return ""
}

type KeepAliveResponse struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *KeepAliveResponse) Reset()         { *m = KeepAliveResponse{} }
func (m *KeepAliveResponse) String() string { return proto.CompactTextString(m) }
func (*KeepAliveResponse) ProtoMessage()    {}
func (*KeepAliveResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_307f1899fd6c0551, []int{11}
}

func (m *KeepAliveResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_KeepAliveResponse.Unmarshal(m, b)
}
func (m *KeepAliveResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_KeepAliveResponse.Marshal(b, m, deterministic)
}
func (m *KeepAliveResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_KeepAliveResponse.Merge(m, src)
}
func (m *KeepAliveResponse) XXX_Size() int {
	return xxx_messageInfo_KeepAliveResponse.Size(m)
}
func (m *KeepAliveResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_KeepAliveResponse.DiscardUnknown(m)
}

var xxx_messageInfo_KeepAliveResponse proto.InternalMessageInfo

func init() {
	proto.RegisterEnum("game_api.PlayerRegistration", PlayerRegistration_name, PlayerRegistration_value)
	proto.RegisterEnum("game_api.PlayerStatus", PlayerStatus_name, PlayerStatus_value)
	proto.RegisterEnum("game_api.MoveStatus", MoveStatus_name, MoveStatus_value)
	proto.RegisterType((*PlayerNameRequest)(nil), "game_api.PlayerNameRequest")
	proto.RegisterType((*RegisterPlayerResponse)(nil), "game_api.RegisterPlayerResponse")
	proto.RegisterType((*GetPossibleMovesRequest)(nil), "game_api.GetPossibleMovesRequest")
	proto.RegisterType((*GetPossibleMovesResponse)(nil), "game_api.GetPossibleMovesResponse")
	proto.RegisterType((*MoveCoordinates)(nil), "game_api.MoveCoordinates")
	proto.RegisterType((*GetCurrentBoardRequest)(nil), "game_api.GetCurrentBoardRequest")
	proto.RegisterType((*GetCurrentBoardResponse)(nil), "game_api.GetCurrentBoardResponse")
	proto.RegisterType((*BoardRow)(nil), "game_api.BoardRow")
	proto.RegisterType((*CanMoveResponse)(nil), "game_api.CanMoveResponse")
	proto.RegisterType((*MoveRequest)(nil), "game_api.MoveRequest")
	proto.RegisterType((*MoveResponse)(nil), "game_api.MoveResponse")
	proto.RegisterType((*KeepAliveResponse)(nil), "game_api.KeepAliveResponse")
}

func init() {
	proto.RegisterFile("gameapi.proto", fileDescriptor_307f1899fd6c0551)
}

var fileDescriptor_307f1899fd6c0551 = []byte{
	// 645 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x8c, 0x54, 0x5b, 0x4f, 0xdb, 0x4c,
	0x10, 0xcd, 0x15, 0x92, 0xc1, 0x80, 0x19, 0xf8, 0x42, 0xe0, 0xab, 0xaa, 0xb0, 0x0f, 0x15, 0x42,
	0x6d, 0x90, 0xe0, 0xa1, 0x55, 0xdf, 0x8c, 0x71, 0xa3, 0x08, 0x63, 0xa7, 0xeb, 0x50, 0x4a, 0x5b,
	0xc9, 0x32, 0xcd, 0x36, 0xb2, 0x4a, 0x6c, 0xd7, 0x36, 0x2d, 0xfc, 0xd5, 0xfe, 0x9a, 0xca, 0x5e,
	0x3b, 0xbe, 0x90, 0x46, 0x7d, 0xf3, 0x5c, 0xce, 0xcc, 0xf1, 0xcc, 0x9c, 0x85, 0xf5, 0xa9, 0x35,
	0x63, 0x96, 0x67, 0xf7, 0x3d, 0xdf, 0x0d, 0x5d, 0x6c, 0x45, 0xa6, 0x69, 0x79, 0x36, 0x39, 0x85,
	0xad, 0xd1, 0x9d, 0xf5, 0xc8, 0x7c, 0xcd, 0x9a, 0x31, 0xca, 0x7e, 0xdc, 0xb3, 0x20, 0xc4, 0xe7,
	0x00, 0xde, 0xdc, 0xd9, 0xad, 0xf6, 0xaa, 0x87, 0x6d, 0x9a, 0xf3, 0x90, 0x6f, 0xd0, 0xa1, 0x6c,
	0x6a, 0x07, 0x21, 0xf3, 0x39, 0x98, 0xb2, 0xc0, 0x73, 0x9d, 0x80, 0xa1, 0x0a, 0xe8, 0xc7, 0x11,
	0xdf, 0x0a, 0x6d, 0xd7, 0x31, 0x42, 0x2b, 0xbc, 0x0f, 0xe2, 0x0a, 0x1b, 0x27, 0xcf, 0xfa, 0x69,
	0xd7, 0x7e, 0x8a, 0xca, 0x32, 0xe9, 0x02, 0x1c, 0xd9, 0x83, 0xdd, 0x01, 0x0b, 0x47, 0x6e, 0x10,
	0xd8, 0xb7, 0x77, 0xec, 0xd2, 0xfd, 0xc9, 0x82, 0x84, 0x22, 0xb9, 0x80, 0xee, 0xd3, 0x50, 0x42,
	0xe2, 0x18, 0x9a, 0xb3, 0xc8, 0xd1, 0xad, 0xf6, 0xea, 0x87, 0x6b, 0x27, 0x7b, 0x59, 0xdf, 0x28,
	0x4f, 0x76, 0x5d, 0x7f, 0x62, 0x3b, 0x56, 0xc8, 0x02, 0xca, 0xf3, 0xc8, 0x2b, 0xd8, 0x2c, 0x45,
	0x50, 0x80, 0xea, 0x43, 0xcc, 0xbb, 0x49, 0xab, 0x0f, 0x91, 0xf5, 0xd8, 0xad, 0x71, 0xeb, 0x91,
	0x74, 0xa1, 0x33, 0x60, 0xa1, 0x7c, 0xef, 0xfb, 0xcc, 0x09, 0xcf, 0x5c, 0xcb, 0x9f, 0xa4, 0xac,
	0xa4, 0x98, 0x70, 0x31, 0x92, 0x90, 0x7a, 0x01, 0x8d, 0xa9, 0x6f, 0x4f, 0x12, 0x4e, 0x98, 0x71,
	0xe2, 0x69, 0xee, 0x2f, 0x1a, 0xc7, 0x49, 0x0f, 0x5a, 0xa9, 0x07, 0x77, 0xa0, 0x69, 0x87, 0x6c,
	0xc6, 0x7f, 0xa4, 0x49, 0xb9, 0x41, 0x2e, 0x61, 0x53, 0xb6, 0x9c, 0x88, 0xf0, 0xbc, 0xf8, 0x5b,
	0x10, 0xf8, 0x7a, 0x0a, 0x03, 0xef, 0x94, 0x07, 0xce, 0xa3, 0xb4, 0x90, 0x4b, 0x64, 0x58, 0xe3,
	0xb5, 0xfe, 0x69, 0xf7, 0x31, 0x27, 0x67, 0xc2, 0x1e, 0x92, 0x71, 0x70, 0x83, 0x8c, 0x40, 0x28,
	0x10, 0x7a, 0x09, 0x2b, 0x41, 0x9e, 0xca, 0x4e, 0x71, 0x07, 0x09, 0x91, 0x24, 0x07, 0x11, 0x1a,
	0xd1, 0x22, 0xe2, 0x92, 0x6d, 0x1a, 0x7f, 0x93, 0x6d, 0xd8, 0xba, 0x60, 0xcc, 0x93, 0xee, 0xec,
	0xac, 0xec, 0x91, 0x09, 0xf8, 0xf4, 0x74, 0xb0, 0x0b, 0x3b, 0x54, 0x19, 0x0c, 0x8d, 0x31, 0x95,
	0xc6, 0x43, 0x5d, 0x33, 0x8d, 0x2b, 0x59, 0x56, 0x0c, 0x43, 0xac, 0xe0, 0x2e, 0x6c, 0x6b, 0xba,
	0x39, 0x52, 0xa5, 0x1b, 0x85, 0x9a, 0x86, 0xaa, 0x8f, 0x4d, 0x55, 0x79, 0x37, 0x16, 0xab, 0xd8,
	0x01, 0x94, 0x54, 0xaa, 0x48, 0xe7, 0x37, 0x26, 0x87, 0x2a, 0x54, 0x39, 0x17, 0x6b, 0x47, 0x5f,
	0x40, 0xc8, 0x8f, 0x0a, 0x57, 0xa1, 0x7e, 0xad, 0x6b, 0x62, 0x05, 0x5b, 0xd0, 0x50, 0x75, 0x23,
	0x82, 0xb6, 0xa0, 0x71, 0x4e, 0xa5, 0x6b, 0xb1, 0x86, 0x02, 0xb4, 0x64, 0x49, 0x33, 0x2f, 0xf5,
	0x0f, 0x8a, 0x58, 0x8f, 0xfc, 0xd7, 0xd2, 0x70, 0x2c, 0x36, 0xa2, 0xae, 0x57, 0x5a, 0x56, 0x36,
	0xe9, 0x2f, 0x36, 0x8f, 0xde, 0x00, 0x64, 0x7f, 0x8f, 0x22, 0x08, 0x11, 0x34, 0x47, 0x77, 0x1d,
	0xda, 0x43, 0x4d, 0xd6, 0x29, 0x55, 0xe4, 0xa8, 0x53, 0x1b, 0x9a, 0x0a, 0xa5, 0x3a, 0x15, 0x6b,
	0x27, 0xbf, 0xeb, 0xb0, 0x3a, 0xb0, 0x66, 0x4c, 0xf2, 0x6c, 0x7c, 0x0f, 0x1b, 0x7e, 0x41, 0x7d,
	0xf8, 0x7f, 0x79, 0xd1, 0x39, 0x31, 0xef, 0xf7, 0xb2, 0xe0, 0x62, 0xd1, 0x92, 0x0a, 0x7e, 0x06,
	0x71, 0x5a, 0x52, 0x13, 0x1e, 0x64, 0xb8, 0xbf, 0x88, 0x70, 0x9f, 0x2c, 0x4b, 0x99, 0x17, 0xff,
	0x08, 0x9b, 0xd3, 0xa2, 0x28, 0xb0, 0x57, 0x00, 0x2e, 0x50, 0xd2, 0xfe, 0xc1, 0x92, 0x8c, 0x79,
	0x65, 0x19, 0x56, 0xbf, 0x72, 0x25, 0x2c, 0x1f, 0x41, 0xee, 0x05, 0x28, 0x29, 0x87, 0x54, 0xf0,
	0x35, 0x3f, 0x3e, 0xfc, 0xaf, 0x78, 0xa2, 0x29, 0xb6, 0x53, 0x76, 0xcf, 0x81, 0x03, 0x68, 0x7f,
	0x4f, 0x2f, 0x74, 0x79, 0xff, 0x5c, 0xf0, 0xc9, 0x4d, 0x93, 0xca, 0x99, 0xf0, 0x09, 0xfa, 0xc7,
	0x69, 0xc6, 0xed, 0x4a, 0xfc, 0x44, 0x9f, 0xfe, 0x09, 0x00, 0x00, 0xff, 0xff, 0x11, 0x92, 0xac,
	0xac, 0xb3, 0x05, 0x00, 0x00,
}