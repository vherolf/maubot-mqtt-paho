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
from mautrix.types import RoomID, EventType, MessageType, GenericEvent
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

    async def stop(self) -> None:
        await super().stop()
        self.client.disconnect()

    @command.new("mqtt", aliases=["mq"])
    @command.argument("channel", required=False)
    @command.argument("message", pass_raw=True, required=True)
    async def command_handler(self, evt: MessageEvent,channel:Optional[str], message: str) -> None:
        if not message:
            await evt.reply("Usage: !mqtt [channel] [text to send]")
            return
        if not channel:
            channel = "generic"
        self.client.publish(channel, message)
        await evt.respond(f"sent channel {channel} the message {message}")

    @command.new("dim")
    @command.argument("step", pass_raw=True, required=False)
    async def dim_handler(self, evt: MessageEvent, step: str) -> None:
        if not step:
            step = "10"
        channel = "light"
        self.client.publish(channel, step)
        await evt.respond(f"dimming lights")

    @command.passive(regex=r"^(?i)on$")
    async def light_on(self, evt: GenericEvent, _: Tuple[str]) -> None:
        channel = "light"
        message = "on"
        self.client.publish(channel, message)
        await evt.respond( "AND THERE WILL BE LIGHT ... " )

    @command.passive(regex=r"^(?i)off$")
    async def light_off(self, evt: GenericEvent, _: Tuple[str]) -> None:
        channel = "light"
        message = "off"
        self.client.publish(channel, message)
        await evt.respond( "Light off" )
