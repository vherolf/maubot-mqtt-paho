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
from typing import Optional, Tuple, NamedTuple, Set, Dict, TYPE_CHECKING
from importlib import import_module

from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from mautrix.types import RoomID
from maubot import MessageEvent
from maubot.handlers.command import Argument
        
import paho.mqtt.client as mqtt

if TYPE_CHECKING:
    from .bot import MqttBot

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("mqttserver")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def connect_mqtt(self):
        mqttclient = mqtt.Client()
        mqttclient.on_connect = self.on_connect
        mqttclient.connect(self['mqttserver']['hostname'],self['mqttserver']['port'], 60)
        mqttclient.loop_start()
        return mqttclient