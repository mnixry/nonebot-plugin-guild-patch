from typing import Optional, Union

from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, escape
from nonebot.log import logger

original_send = Bot.send


async def patched_send(
    self: Bot, event: Event, message: Union[Message, MessageSegment, str], **kwargs
):
    guild_id: Optional[int] = getattr(event, "guild_id", None)
    channel_id: Optional[int] = getattr(event, "channel_id", None)

    if not (guild_id and channel_id):
        return await original_send(self, event, message, **kwargs)
    logger.opt(colors=True).debug(
        "Sending guild message to "
        f"guild_id=<e>{guild_id}</e>, channel_id=<e>{channel_id}</e>"
    )

    user_id: Optional[int] = getattr(event, "user_id", None)
    message = (
        escape(message, escape_comma=False) if isinstance(message, str) else message
    )

    message_sent = message if isinstance(message, Message) else Message(message)
    if user_id and kwargs.get("at_sender", False):
        message_sent = MessageSegment.at(user_id) + " " + message_sent

    return await self.send_guild_channel_msg(
        guild_id=guild_id, channel_id=channel_id, message=message_sent
    )


Bot.send = patched_send

from .models import *  # noqa
