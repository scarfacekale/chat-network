import json, logging, uuid

from src import version, hashes, ciphers
from src.database import database

from src.protocol import (
    EventCodes,
    EventType
)

from src.packets import (
    IdentificationRequest,
    SignInRequest,
    SignUpRequest,
    SubscribeRequest,
    InviteRequest,
    KeyExchangeInitiatorRequest,
    KeyExchangeResponderRequest,
    MessageRequest,

    IdentificationReply,
    ProtocolStandardReply,
    SignUpReply,
    SignInReply,
    SubscribeResponse,
)

logging.basicConfig(level=logging.INFO)

class EventHandler:

    def __init__(self, clients):
        self.clients = clients

    async def handle_event(self, ws, t, content):
        session = content.get('session')
        username = content.get('source')

        # make sure the client is actually authenticated lol
        if session:
            client = self.clients.get_from_session(session)

            # make sure they aint spoofing their name
            if client and username:
                if client.name != username:
                    logging.info(f"Request {t} failed with username {username} on client {client.name}")
                    return

        if t == EventType.IDENTIFICATION:
            await self.identify_response(ws, content)
        elif t == EventType.PROTOCOL_STANDARD:
            await self.protocol_response(ws, content)
        elif t == EventType.USER_SIGNIN:
            await self.signin_response(ws, content)
        elif t == EventType.USER_SIGNUP:
            await self.signup_response(ws, content)
        elif t == EventType.SUBSCRIBE:
            await self.subscribe_response(ws, content)
        elif t == EventType.INVITE_REQUEST:
            await self.invite_request_response(ws, content)
        elif t == EventType.KEY_EXCHANGE_INITIATE_REQUEST:
            await self.key_exchange_initiate_response(ws, content)
        elif t == EventType.KEY_EXCHANGE_RESPONDER_REQUEST:
            await self.key_exchange_responder_response(ws, content)
        elif t == EventType.MESSAGE_REQUEST:
            await self.forward_message_request(ws, content)

    async def identify_response(self, ws, content):
        request = IdentificationRequest(
            data = content
        )

        logging.info(f"Identification with {request}")

        if request.version != version:
            status = status_codes.get('version_mismatch')

            reply = IdentificationReply(
                response_code = EventCodes.VERSION_MISMATCH
            )

            logging.info(f"Completing identification error with {reply}")

            await ws.send(reply.data)
            return

        reply = IdentificationReply(
            response_code = EventCodes.SUCCESS
        )

        logging.info(f"Completing identification with {reply}")

        await ws.send(reply.data)

    async def protocol_response(self, ws, content):
        reply = ProtocolStandardReply(
            response_code = EventCodes.SUCCESS
        )

        logging.info(f"Completing protocol standard with {reply}")

        await ws.send(reply.data)


    async def signin_response(self, ws, content):
        request = SignInRequest(
            data = content
        )

        logging.info(f"Signin request with {request}")

        if not database.user_exists(request.username):

            reply = SignUpReply(
                response_code = EventCodes.USER_NOT_IN_USE
            )

            logging.info(f"Completing sign in error request with {reply}")

            await ws.send(reply.data)
            return

        if not database.validate_password(request.username, request.password):
            reply = SignUpReply(
                response_code = EventCodes.INVALID_PASSWORD
            )

            logging.info(f"Completing sign in error request with {reply}")

            await ws.send(reply.data)
            return

        session = str(uuid.uuid4())

        reply = SignInReply(
            response_code = EventCodes.SUCCESS,
            session = session
        )

        logging.info(f"Completing sign in request with {reply}")

        self.clients.create(
            ws = ws,
            name = request.username,
            session = session
        )

        await ws.send(reply.data)

    async def signup_response(self, ws, content):
        request = SignUpRequest(
            data = content
        )

        logging.info(f"Signup request with {request}")

        if database.user_exists(request.username):

            reply = SignUpReply(
                response_code = EventCodes.USER_IN_USE
            )

            logging.info(f"Completing sign up error request with {reply}")

            await ws.send(reply.data)
            return

        if not request.hash_algo in hashes:

            reply = SignUpReply(
                response_code = EventCodes.HASH_NOT_AVAILABLE
            )

            logging.info(f"Completing sign up error request with {reply}")

            await ws.send(reply.data)
            return

        session = str(uuid.uuid4())

        reply = SignUpReply(
            response_code = EventCodes.SUCCESS,
            session = session
        )

        logging.info(f"Completing sign up request with {reply}")

        self.clients.create(
            ws = ws,
            name = request.username,
            session = session
        )

        database.create_user(
            username = request.username, 
            password = request.password, 
            hash_algo = request.hash_algo
        )
    
        await ws.send(reply.data)

    async def subscribe_response(self, ws, content):
        request = SubscribeRequest(
            data = content
        )

        logging.info(f"Subscribe request with {request}")

        client = self.clients.get_from_session(request.session)

        if client:
            logging.info(f"Subscribing client {client.name} to server")

            client.connect(
                ws = ws
            )

            reply = SubscribeResponse(
                code = EventCodes.SUCCESS
            )

            await client._ws.send(reply.data)
            return

        logging.info(f"Not subscribing client to server")

        reply = SubscribeResponse(
            code = EventCodes.BAD_TOKEN
        )

        await ws.send(reply.data)

    async def invite_request_response(self, ws, content):
        request = InviteRequest(
            data = content
        )

        logging.info(f"Invite request with {request}")
        client = self.clients.get_from_username(request.dest)

        if client:

            # we dont wanna leak client session to someone else lol
            del content['session']

            await client._ws.send(json.dumps(content))

    async def key_exchange_initiate_response(self, ws, content):
        request = KeyExchangeInitiatorRequest(
            data = content
        )

        logging.info(f"Key exchange initiation with {request}")

        client = self.clients.get_from_username(request.dest)

        if client:
            # we dont wanna leak client session to someone else lol
            del content['session']

            await client._ws.send(json.dumps(content))

    async def key_exchange_responder_response(self, ws, content):
        request = KeyExchangeResponderRequest(
            data = content
        )

        logging.info(f"Key exchange responder with {request}")

        client = self.clients.get_from_username(request.dest)

        if client:
            # we dont wanna leak client session to someone else lol
            del content['session']

            await client._ws.send(json.dumps(content))

    async def forward_message_request(self, ws, content):
        request = MessageRequest(
            data = content
        )

        logging.info(f"Message Request responder with {request}")

        client = self.clients.get_from_username(request.dest)

        if client:
            # we dont wanna leak client session to someone else lol
            del content['session']

            await client._ws.send(json.dumps(content))
