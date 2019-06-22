# mqtt - A maubot plugin to send and receive messages from a mqtt server .
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Optional, Tuple, Type, Dict

from mautrix.util.config import BaseProxyConfig
from mautrix.types import RoomID, EventType, MessageType
from maubot import Plugin, MessageEvent
from maubot.handlers import command, event

from .util import Config

class mqtt(Plugin):
    config: Config

    async def start(self) -> None:
        await super().start()
        self.on_external_config_update()

    def on_external_config_update(self) -> None:
        self.config.load_and_update()
        self.mqtt_server = self.config.load_mqtt_server()

    @classmethod
    def get_config_class(cls) -> Type['BaseProxyConfig']:
        return Config

    @event.on(EventType.ROOM_MESSAGE)
    async def event_handler(self, evt: MessageEvent) -> None:
        if (evt.content.msgtype == MessageType.NOTICE 
                        or evt.sender == self.client.mxid):
            return
        result = await evt.content.body
        await evt.respond(f"[{evt.sender}](https://matrix.to/#/{evt.sender}) said "
                          f"{result.text}")

    @command.new("mqtt", aliases=["mq"])
    @command.argument("text", pass_raw=True, required=False)
    async def command_handler(self, evt: MessageEvent, language: Optional[Tuple[str, str]],
                              text: str) -> None:
        if not text:
            await evt.reply("Usage: !translate [from] <to> [text or reply to message]")
            return
        await evt.reply(text)