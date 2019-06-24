import paho.mqtt.client as mqtt

broker_url = "localhost"
broker_port = 1883

client = mqtt.Client()
client.connect(broker_url, broker_port)

client.subscribe("info", qos=1)

client.publish(topic="info", payload="TestingPayload", qos=1, retain=False)