"""A simple simulator for the OPC LED panels.

Usage: python simulator.py

To make the LED-bot talk to this server, change the server address to
`localhost:7890` in your configuration.

"""

from struct import unpack

import SocketServer

W = 64
H = 32
led_num = W * H

led_width = led_height = led_spacing = 3

screen_width = W * (led_width + led_spacing) + led_spacing
screen_height = H * (led_height + led_spacing) + led_spacing

header = 'B' * 4
udp_format = header + ''.join('B' for _ in xrange(led_num * 3))


class OPCHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(4096*32).strip()

        values = unpack(udp_format, data)

        # reverse the data, since we do the craziness in our client.
        values = values[::-1][:-4]

        screen = self.server.screen

        for h in range(H):
            for w in range(W):
                i = (h*W + w) * 3
                fill = '#%02x%02x%02x' % values[i:i+3]
                left = led_spacing + w * (led_width + led_spacing)
                top = led_spacing + h * (led_height + led_spacing)
                screen.create_rectangle(
                    left, top, left+led_width, top+led_height, fill=fill
                )

        screen.update()


class OPCServer(SocketServer.TCPServer):

    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.screen = get_canvas()
        self.screen.update()

def get_canvas():
    """ Creates a Tkinter canvas. """

    from Tkinter import Tk, Canvas, BOTH

    root = Tk()
    root.title('LED bot simulator')
    root.geometry("%sx%s" % (screen_width, screen_height))

    canvas = Canvas(root)
    canvas.pack(fill=BOTH, expand=1)
    canvas.create_rectangle(
        0, 0, screen_width, screen_height, outline="#000", fill="#000"
    )

    return canvas


if __name__ == "__main__":
    HOST, PORT = "localhost", 7890

    # Create the server
    server = OPCServer((HOST, PORT), OPCHandler)

    # Start the server; Interrupt with Ctrl-C
    server.serve_forever()
