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

import paho.mqtt.client as mqtt

class MqttBot(Plugin):
    config: Config

    async def start(self) -> None:
        await super().start()
        print("------------------",type(self), dir(self))
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
        self.client.loop_stop()

    def on_message(self,client, userdata, message):
        evt = MessageEvent()
        print("received message =",str(message.payload.decode("utf-8")))
        evt.respond( str( message.payload.decode("utf-8") ) )

    @command.new("publish", aliases=["pub"])
    @command.argument("channel", required=True)
    @command.argument("message", pass_raw=True, required=True)
    async def pub_handler(self, evt: MessageEvent, channel:str, message: str) -> None:
        if not message:
            await evt.reply("Usage: !publish [channel] [text to send]")
            return
        self.client.publish(channel, message)
        print(dir(evt))    
        await evt.respond(f"sent channel {channel} the message {message}")

    @command.new("subscribe", aliases=["sub"])
    @command.argument("channel", required=False)
    @command.argument("unsubscribe", required=False)
    async def sub_handler(self, evt: MessageEvent, channel:Optional[str], unsubscribe: Optional[str]) -> None:
        if not channel:
            await evt.reply("Usage: !subscribe [channel]")
            return
        self.client.subscribe(channel)
        self.client.message_callback_add(channel, self.on_message)
        await evt.respond(f"subscribe channel {channel}")


    @command.passive(regex=r"^(?i)on|--- -\.$")
    async def event_on(self, evt: GenericEvent, _: Tuple[str]) -> None:
        channel = config["event_on"]["channel"]
        channel = config["event_on"]["message"]
        self.client.publish(channel, message)
        await evt.respond( "switched on" )

    @command.passive(regex=r"^(?i)off|--- \.\.-\. \.\.-\.$")
    async def event_off(self, evt: GenericEvent, _: Tuple[str]) -> None:
        channel = config["event_off"]["channel"]
        channel = config["event_off"]["message"]
        self.client.publish(channel, message)
        await evt.respond( "switched off" )
