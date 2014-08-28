# Standard library
from cmd import Cmd
import sys

class CLIHandler(Cmd):

    def send_response(self, response, msg):
        """ Send the response to a user who sent a message to us. """

    def listen(self, callback):
        self.callback = callback
        self.cmdloop()

    def default(self, line):
        if line == 'EOF':
            print('Exiting ...\n')
            sys.exit(0)

        message = {
            'content': line
        }

        self.callback(message, self)
