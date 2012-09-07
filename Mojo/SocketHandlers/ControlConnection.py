from tornadio2 import SocketConnection

class ControlConnection(SocketConnection):
    def on_message(self, msg):
        pass