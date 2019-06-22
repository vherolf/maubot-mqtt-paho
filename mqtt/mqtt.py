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


class MqttBot(Plugin):
    config: Config

    async def start(self) -> None:
        await super().start()
        self.on_external_config_update()
        self.client = self.config.connect_mqtt()

    def on_external_config_update(self) -> None:
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type['BaseProxyConfig']:
        return Config

    @command.new("mqtt", aliases=["mq"])
    @command.argument("message", pass_raw=True, required=False)
    async def command_handler(self, evt: MessageEvent, message: str) -> None:
        if not message:
            await evt.reply("Usage: !mqtt [channel] [text to send]")
            return
        self.client.publish("test", message)
        await evt.reply(f"sent to test: {message}")