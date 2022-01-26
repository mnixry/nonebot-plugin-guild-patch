import inspect
from typing import Optional, Union

import nonebot
from nonebot.adapters.onebot.v11 import (
    Adapter,
    Bot,
    Event,
    Message,
    MessageSegment,
    escape,
)
from nonebot.log import logger

from . import models

original_send = Bot.send


async def patched_send(
    self: Bot, event: Event, message: Union[Message, MessageSegment, str], **kwargs
):
    guild_id: Optional[int] = getattr(event, "guild_id", None)
    channel_id: Optional[int] = getattr(event, "channel_id", None)
    if not (guild_id and channel_id):
        return await original_send(self, event, message, **kwargs)

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


driver = nonebot.get_driver()


@driver.on_startup
def patch():
    Bot.send = patched_send

    for model in models.__dict__.values():
        if inspect.isclass(model) and issubclass(model, Event):
            Adapter.add_custom_model(model)

    logger.debug("Patch for NoneBot2 guild adaptation has been applied.")
