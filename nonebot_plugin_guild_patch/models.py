from typing import List, Optional

from nonebot.adapters.onebot.v11 import Message, MessageEvent, NoticeEvent
from pydantic import BaseModel, Field, validator
from typing_extensions import Literal


class GuildMessageEvent(MessageEvent):
    __event__ = "message.guild"
    self_tiny_id: int

    message_type: Literal["guild"]
    message_id: str
    guild_id: int
    channel_id: int

    raw_message: str = Field(alias="message")
    font: None = None

    @validator("raw_message", pre=True)
    def _validate_raw_message(cls, raw_message):
        if isinstance(raw_message, str):
            return raw_message
        elif isinstance(raw_message, list):
            return str(Message(raw_message))
        raise ValueError("unknown raw message type")


class ReactionInfo(BaseModel):
    emoji_id: str
    emoji_index: int
    emoji_type: int
    emoji_name: str
    count: int
    clicked: bool

    class Config:
        extra = "allow"


class ChannelNoticeEvent(NoticeEvent):
    __event__ = "notice.channel"
    self_tiny_id: int
    guild_id: int
    channel_id: int
    user_id: int

    sub_type: None = None


class MessageReactionUpdatedNoticeEvent(ChannelNoticeEvent):
    __event__ = "notice.message_reactions_updated"
    notice_type: Literal["message_reactions_updated"]
    message_id: str
    current_reactions: Optional[List[ReactionInfo]] = None


class SlowModeInfo(BaseModel):
    slow_mode_key: int
    slow_mode_text: str
    speak_frequency: int
    slow_mode_circle: int

    class Config:
        extra = "allow"


class ChannelInfo(BaseModel):
    owner_guild_id: int
    channel_id: int
    channel_type: int
    channel_name: str
    create_time: int
    creator_id: int
    creator_tiny_id: int
    talk_permission: int
    visible_type: int
    current_slow_mode: int
    slow_modes: List[SlowModeInfo] = []

    class Config:
        extra = "allow"


class ChannelUpdatedNoticeEvent(ChannelNoticeEvent):
    __event__ = "notice.channel_updated"
    notice_type: Literal["channel_updated"]
    operator_id: int
    old_info: ChannelInfo
    new_info: ChannelInfo


class ChannelCreatedNoticeEvent(ChannelNoticeEvent):
    __event__ = "notice.channel_created"
    notice_type: Literal["channel_created"]
    operator_id: int
    channel_info: ChannelInfo


class ChannelDestroyedNoticeEvent(ChannelNoticeEvent):
    __event__ = "notice.channel_destroyed"
    notice_type: Literal["channel_destroyed"]
    operator_id: int
    channel_info: ChannelInfo
