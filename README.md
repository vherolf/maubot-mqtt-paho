# maubot mqtt bot with paho
A [maubot](https://github.com/maubot/maubot) plugin to publish/subscribe mqtt messages to a MQTT broker.

## install python mqtt client library

In our virtualenv
```
pip install paho-mqtt
```

## Install Mosquitto Broker

```
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

## testing and usage

fire up a termnial and subscribe to the info channel
```
mosquito_sub -h localhost -t info
```

type in your chat window
```
!pub info Hello World
```
