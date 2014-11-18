import paho.mqtt.client as mqtt

class mqttHandler:
	"""Send MQTT 'push' messages to your LEDScreen """
	def __init__(self,server="test.mosquitto.org",channel="ledbot/"):
		self.channel = channel
		self.client= mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.send_new_message
		self.client.connect(server, 1883, 60)

	def on_connect(self,client, userdata, flags, rc):
		print("Connected to MQTT server with result code "+str(rc))
		self.client.subscribe(self.channel)

	def send_response(self, response, msg):
		""" Send the response to a user who sent a message to us. """

	def listen(self,callback):
		self.callback = callback
		while True:
			self.client.loop()

	def send_new_message(self,client, userdata, message):
		if message.payload is not None:
			print ("trying to send",message.payload)
			msg = {
			'text': [message.payload],
			'type':'text',
			'color':(0,0,120),
			'background':(0,0,0)
			}
			self.callback(msg, self)