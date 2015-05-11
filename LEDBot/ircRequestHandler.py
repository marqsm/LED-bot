import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class IRCBot(irc.bot.SingleServerIRCBot):

	def __init__(self, channel="#ledbot", nick="ledbot_test5678", server="chat.freenode.net",port=6667):
		irc.bot.SingleServerIRCBot.__init__(self,[(server,port)],nick,nick)
		self.channel = channel
		self.debug = True
		self.default_color = (0,0,255)
		self.default_bg = (0,0,0)
		self.callback = None

	def send_response(self, response, msg):
		""" Send the response to a user who sent a message to us. """
		return response["content"]

	def listen(self,callback):
		self.callback = callback
		self.start()

	def send_text(self,data="blank message",color=(0,0,255),background=(0,0,0)):

		print ("trying to send",data)
		msg = {
			'text': data.split(),
			'type':'text',
			'color':color,
			'background':background
		}
		try:
			self.callback(msg, self)
		except:
			print "err with callback"

	def send_image(self,data):
		msg = {
			'url': data,
			'type':'image'
		}
		try:
			self.callback(msg, self)
		except:
			print "err with callback"

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_privmsg(self, c, e):
		self.do_command(e, e.arguments[0])

	def on_pubmsg(self, c, e):
		a = e.arguments[0].split(":", 1)
		if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
			self.do_command(e, a[1].strip())
		return

	def do_command(self, e, cmd):
		source = e.source.nick 
		c = self.connection
		parsed = cmd.split(" ")

		if parsed[0] == "help":
			c.notice(source,"---- commands ----")
			c.notice(source,"show <message>     # sends your text to LEDs")
			c.notice(source,"img <url>     		# sends an image url to LEDs")
			c.notice(source,"color <r> <g> <b>  # sets the text color")
			c.notice(source,"bg <r> <g> <b>     # sets the background color")

		elif parsed[0] == "color":
			if len(parsed) is 4:
				self.default_color = (int(parsed[1]),int(parsed[2]),int(parsed[3]))

		elif parsed[0] == "bg":
			if len(parsed) is 4:
				self.default_bg = (int(parsed[1]),int(parsed[2]),int(parsed[3]))

		elif parsed[0] == "show":
			print("sending %s" % " ".join(parsed[1:]))
			c.notice(source,"Sending message %s" % " ".join(parsed[1:]))
			self.send_text(source+": "+" ".join(parsed[1:]),self.default_color)

		elif parsed[0] == "img":
			print("sending %s" % " ".join(parsed[1:]))
			c.notice(source,"Sending message %s" % " ".join(parsed[1:]))
			self.send_image(parsed[1])

#		elif parsed[0] == "disconnect":
#			self.disconnect()
#		elif parsed[0] == "die":
#			self.die()
		else:
			print(cmd,e)
			c.notice(source,"I didn't understand that! Try messaging me `help` for more commands")

#def main():
#	bot = IRCBot("#mytestbot","testbot67543","chat.freenode.net",port=6667)
#	bot.start()
#
#if __name__ == "__main__":
#	main()