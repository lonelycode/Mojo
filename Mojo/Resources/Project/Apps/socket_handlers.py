from Mojo.SocketHandlers.BaseSocketHandler import MojoSocketHandler, CURRENT_SESSIONS, LOGGED_IN_SESSIONS

#Setup your socket connections here
class SocketConnectionHandler(MojoSocketHandler):

    def on_message(self, msg):
        pass
