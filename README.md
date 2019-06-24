# mqtt
A [maubot](https://github.com/maubot/maubot) to send and receive mqtt messages.

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

type in your caht window
```
!pub info Hello World
```