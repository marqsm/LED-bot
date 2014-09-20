import requests
import threading
from time import sleep
import datetime

class WebFillerHandler(object):
	"""docstring for WeatherReportListener"""
	def __init__(self):
		self.counter = 0
		self.time_interval = 10.0
		
		# base url, params to pass to self.fetch_json()
		self.data_sources = {
		0 : ("http://forecast.weather.gov/MapClick.php",{'lat':'37.7915388','lon':'-122.4200488','FcstType':'json' }),
		1 : ("http://proximobus.appspot.com/agencies/sf-muni/stops/16826/predictions.json",None),
		2 : ("http://api.ihackernews.com/page",None),
		3 : ("http://iheartquotes.com/api/v1/random",{'format':'json','max_characters':'200','source':'computer'})
		}
		
		self.formats = { 
		0 : self.format_weather,
		1 : self.format_muni,
		2 : self.format_hn,
		3 : self.format_quote
		}
		
		self.t = threading.Timer(self.time_interval, self.send_new_message).start()

	
	def send_response(self, response, msg):
		""" Send the response to a user who sent a message to us. """

	def listen(self,callback):
		self.callback = callback
		#self.send_new_message()

	def send_new_message(self):
		formatted_data = self.formats[self.counter](self.fetch_json(self.data_sources[self.counter]))
		print ("trying to send",formatted_data)
		msg = {
			'content': " ".join(formatted_data)
		}
		self.callback(msg, self)

		if self.counter >= len(self.data_sources)-1:
			self.counter = 0
		else:
			self.counter += 1
		
		self.t = threading.Timer(self.time_interval, self.send_new_message).start()


	def fetch_json(self,src):
		try:
			print ("source",src[0],src[1])
			data = requests.get(src[0],params=src[1])
			json = data.json()
		except:
			json = None
		
		return json


	def format_weather(self, json):
		pieces = ["led-bot show-text","Current",json['currentobservation']['Temp'],json['time']['startPeriodName'][0],json['data']['weather'][0],json['data']['temperature'][0],json['time']['startPeriodName'][1],json['data']['weather'][1],json['data']['temperature'][1]]
		return pieces

	def format_muni(self,json):
	# example with SF MTA, change to transit agency of site
		pieces = ["led-bot show-text","Muni",json['items'][0]['run_id'][:2],str(json['items'][0]['minutes']),"min",json['items'][1]['run_id'][:2],str(json['items'][1]['minutes']),"min"]
		return pieces

	def format_hn(self,json):
		pieces = ["led-bot show-text",json['items'][0]['title'],json['items'][1]['title'],json['items'][2]['title']]
		return pieces

	def format_quote(self,json):
		pieces = ["led-bot show-text","quote:",json['quote']]
		return pieces


