from .subscriber import MultiSubscriber, Subscriber
from gi.repository import Gtk, GLib, Gdk
import json
import socket

class Bot(Subscriber):
    def __init__(self, client):
        self.client = client
        self.conn = BotConnection(("127.0.0.1", 12314), self)

    def on_key_pressed(self, val, char):
        if char == 'o':
            print("o pressed :)")

    def on_new_target(self, x, y):
        print("sending target:", x, y)
        self.client.send_target(x, y)

class BotConnection():
    def __init__(self, address, subscriber):
        self.sub = subscriber

        # connect
        self.socket = socket.create_connection(address)

        self.watch()

    def on_message(self):
        pos = json.loads(self.socket.recv(255).decode('utf8'))
        print("now pos: ", str(pos))
        self.sub.on_new_target(*pos)

    def watch(self):
        GLib.io_add_watch(self.socket, GLib.IO_IN, lambda ws, _: self.on_message() or True)

