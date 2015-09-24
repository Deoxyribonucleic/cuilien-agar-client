from .subscriber import MultiSubscriber, Subscriber
from gi.repository import Gtk, GLib, Gdk
import json
import socket
import struct

class Bot(Subscriber):
    def __init__(self, client):
        self.client = client
        self.conn = BotConnection(("127.0.0.1", 12314), self)

    def on_key_pressed(self, val, char):
        if char == 'o':
            print("o pressed :)")

    def on_set_target_command(self, x, y):
        print("sending target:", x, y)
        self.client.send_target(x, y)

    def on_ingame(self):
        self.conn.send_ready()
    
    def on_death(self):
        self.conn.send_death()
    
    def on_respawn(self):
        self.conn.send_spawned()

    def on_respawn_command(self):
        print("respawning!")
        self.client.send_respawn()

class MessageType:
    ready = 1
    respawn = 2
    death = 3
    update = 4
    set_target = 5
    spawned = 6

class BotConnection():

    def __init__(self, address, subscriber):
        self.sub = subscriber

        # connect
        self.socket = socket.create_connection(address)

        self.watch()

    def on_message(self):
        length = struct.unpack("!H", self.socket.recv(2))[0]
        raw_data = self.socket.recv(length).decode('utf8')
        print(raw_data)

        message = json.loads(raw_data)
        message_type = message["type"]

        if message_type == MessageType.respawn:
            self.sub.on_respawn_command()

        elif message_type == MessageType.set_target:
            self.sub.on_set_target_command(message["x"], message["y"])

    def send_ready(self):
        self.send_message({ "type": MessageType.ready });

    def send_death(self):
        self.send_message({ "type": MessageType.death });

    def send_spawned(self):
        self.send_message({ "type": MessageType.spawned });

    def send_message(self, msg):
        data = json.dumps(msg).encode('utf8')
        self.socket.send(struct.pack("!H", len(data)) + data)

    def watch(self):
        GLib.io_add_watch(self.socket, GLib.IO_IN, lambda ws, _: self.on_message() or True)

