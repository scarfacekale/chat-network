import websocket, json, logging, gi, time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject

from src import version, client_name
from src.protocol import EventType, EventCodes
from src.database import (
    log_credentials,
    get_username,
    log_channel,
)

from src.communication import (
    Sender,
    Receiver
)

from src.packets import (
    IdentificationRequest, 
    ProtocolStandardRequest, 
    SignUpRequest,
    SignInRequest,
    SubscribeRequest,
    InviteRequest,
    KeyExchangeInitiatorRequest,
    KeyExchangeResponderRequest,
    MessageRequest,

    IdentificationResponse,
    ProtocolStandardResponse,
    SignUpResponse,
    InviteRequestResponse,
    KeyExchangeInitiatorResponse,
    KeyExchangeResponderResponse,
    MessageResponse,
    SubscribeResponse,
)

from src.dialog import (
    message_error_dialog,
    message_dialog
)

logging.basicConfig(level=logging.INFO)

class EventHandler:

    def __init__(self, app):
        self.app = app

        self.server = None
        self.ws = None
        self.dispatcher = None

    def connect(self, server):
        self.server = "ws://" + server
        self.ws = websocket.WebSocketApp(self.server,
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close,
                                    on_open = self.identify)

        self.dispatcher = EventDispatcher(
            app = self.app,
            ws = self.ws,
            server = server
        )

        self.ws.run_forever()

    def connect_and_subscribe(self, server, session):
        self.server = "ws://" + server
        self.ws = websocket.WebSocketApp(self.server,
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close,
                                    on_open = self.subscribe)

        self.dispatcher = EventDispatcher(
            app = self.app,
            ws = self.ws,
            session = session,
            server = server
        )

        self.ws.run_forever()

    def close(self):
        self.ws.close()

    def on_close(self, ws, error, t):
        print('closed')

    def on_error(self, ws, error):
        print(error)

    def identify(self, ws):
        self.dispatcher.identify_request()

    def subscribe(self, ws):
        self.dispatcher.subscribe_request()

    def on_message(self, ws, message):
        message = json.loads(message)
        t = message.get('type')

        # next up implement states to only dispatch state if its actually relevant

        if t == EventType.IDENTIFICATION:
            self.dispatcher.identify_response(message)
        elif t == EventType.PROTOCOL_STANDARD:
            self.dispatcher.protocol_response(message)
        elif t == EventType.USER_SIGNUP:
            self.dispatcher.signup_response(message)
        elif t == EventType.SUBSCRIBE:
            self.dispatcher.subscribe_response(message)
        elif t == EventType.INVITE_REQUEST:
            self.dispatcher.invite_response(message)
        elif t == EventType.KEY_EXCHANGE_INITIATE_REQUEST:
            self.dispatcher.key_exchange_initiate_response(message)
        elif t == EventType.KEY_EXCHANGE_RESPONDER_REQUEST:
            self.dispatcher.key_exchange_responder_response(message)
        elif t == EventType.MESSAGE_REQUEST:
            self.dispatcher.receive_message(message)

class EventDispatcher:

    def __init__(self, app, ws, server=None, session=None, username=None, password=None):
        self.app = app
        self.ws = ws
        self.server = server
        self.username = username
        self.password = password
        self.session = session

        if self.username is None:
            self.username = get_username()

    def identify_request(self):
        request = IdentificationRequest(
            version = version,
            client_name = client_name
        )

        logging.info(f"Identifying request with {request}")

        self.ws.send(request.data)

    def identify_response(self, message):
        response = IdentificationResponse(
            data = message
        )

        logging.info(f"Completing identification with {response}")

        if not response.invitations:
            message_dialog("Server is not accepting invites.")
            return

        self.protocol_request()

    def protocol_request(self):
        request = ProtocolStandardRequest(

        )

        logging.info(f"Requesting protocol standard with {request}")

        self.ws.send(request.data)

    def protocol_response(self, message):
        response = ProtocolStandardResponse(message)
        logging.info(f"Completing protocol standard with {response}")

    def signup_request(self, username, password, hash_algo):
        request = SignUpRequest(
            username = username,
            password = password,
            hash_algo = hash_algo
        )

        # set username and password
        self.username = username
        self.password = password

        logging.info(f"Requesting sign up request with {request}")
        self.ws.send(request.data)

    def signup_response(self, message):
        response = SignUpResponse(
            data = message
        )

        logging.info(f"Completing sign up response with {response}")

        if response.code != EventCodes.SUCCESS:
            message_error_dialog(self.app.window, response.code)
            return

        logging.info(f"Successfully signed up to server!")

        # make sure we actually have credentials to set lol
        if self.username and self.password:
            self.session = response.session

            log_credentials(
                server = self.server,
                username = self.username,
                password = self.password,
                session = response.session
            )

    def signin_request(self, username, password):
        request = SignInRequest(
            username = username,
            password = password,
        )

        # set username and password
        self.username = username
        self.password = password

        logging.info(f"Requesting sign in with {request}")
        self.ws.send(request.data)

    def signin_response(self, message):
        response = SignInResponse(
            data = message
        )

        if response.code != EventCodes.SUCCESS:
            message_error_dialog(self.app.window, response.code)
            return

        logging.info(f"Successfully signed in to server!")

        # make sure we actually have credentials to set lol
        if self.username and self.password:
            self.session = response.session

            log_credentials(
                server = self.server,
                username = self.username,
                password = self.password,
                session = response.session
            )

    def subscribe_request(self):
        request = SubscribeRequest(
            session = self.session
        )

        logging.info(f"Requesting subscribe with {request}")

        self.ws.send(request.data)

    def subscribe_response(self, message):
        response = SubscribeResponse(
            data = message
        )

        logging.info(f"Subscribe response with {response}")

        if response.code != EventCodes.SUCCESS:
            message_error_dialog(self.app.window, response.code)
            return

        self.app.title_bar.set_property('subtitle', f'Online as {self.username}')
        self.app.subscribed = True

    def invite_request(self, username):
        request = InviteRequest(
            source = self.username,
            dest = username,
            session = self.session
        )

        logging.info(f"Requesting invite with {request}")

        self.ws.send(request.data)

    def invite_response(self, message):
        response = InviteRequestResponse(
            data = message
        )

        logging.info(f"Invite request from {response.source} with {response}")

        # create sender channel
        GObject.idle_add(
           self.app.create_channel,
           response.source,
           Sender
        )

    def key_exchange_request(self, channel, username):

        # respond with key initiator
        request = KeyExchangeInitiatorRequest(
            source = self.username,
            dest = username,
            session = self.session,

            identity_key = channel.comm.ik_public_bytes,
            signed_prekey = channel.comm.spk_public_bytes,
            onetime_prekey = channel.comm.opk_public_bytes
        )

        logging.info(f"Key exchange request with {request}")
        self.ws.send(request.data)

    def key_exchange_initiate_response(self, message):
        response = KeyExchangeInitiatorResponse(
            data = message
        )

        logging.info(f"Key exchange initiate response with {response}")

        # create receiver channel
        GObject.idle_add(
           self.app.create_channel,
           response.source,
           Receiver
        )

        # just to be sure lol
        time.sleep(1)

        channel = self.app.get_channel(
            username = response.source
        )

        channel.comm.x3dh(
            identity_key = response.identity_key,
            signed_prekey = response.signed_prekey,
            onetime_prekey = response.onetime_prekey
        )

        log_channel(
            channel = channel
        )

        reply = KeyExchangeResponderRequest(
            source = self.username,
            dest = response.source,
            session = self.session,
            identity_key = channel.comm.ik_public_bytes,
            epheremal_key = channel.comm.epk_public_bytes
        )

        self.ws.send(reply.data)

    def key_exchange_responder_response(self, message):
        response = KeyExchangeResponderResponse(
            data = message
        )

        channel = self.app.get_channel(
            username = response.source
        )

        channel.comm.x3dh(
            identity_key = response.identity_key,
            epheremal_key = response.epheremal_key,
        )

        log_channel(
            channel = channel
        )

        # done

    def send_message(self, username, message, comm):
        ciphertext, nonce = comm.encrypt(
            message = message
        )

        request = MessageRequest(
            source = self.username,
            dest = username,
            session = self.session,

            message = ciphertext,
            nonce = nonce
        )

        logging.info(f"Sending Message request with {request}")

        self.ws.send(request.data)

    def receive_message(self, message):
        message = MessageResponse(
            data = message
        )

        logging.info(f"Receiving Message request with {message}")

        channel = self.app.get_channel(
            username = message.source
        )

        plaintext = channel.comm.decrypt(
            message = message.message,
            nonce = message.nonce
        )

        channel.receive_message(
            message = plaintext
        )
