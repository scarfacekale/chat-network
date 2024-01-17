import json
from src import version, server, ciphers, hashes
from src.protocol import EventCodes, EventType

class IdentificationRequest:

    def __init__(self, data):
        self._version = data.get('version')
        self._client_name = data.get('client')

    def __repr__(self):
        return f"IdentificationRequest(version={self.version}, client_name={self.client_name})"

    @property
    def type(self):
        return EventType.IDENTIFICATION

    @property
    def version(self):
        return self._version

    @property
    def client_name(self):
        return self._client_name

class IdentificationReply:

    def __init__(self, response_code=EventCodes.SUCCESS, server=server, invitations=True, version=version):
        self._server = server
        self._invitations = invitations
        self._response_code = response_code
        self._version = version

    def __repr__(self):
        return f"IdentificationReply(response_code={self.response_code})"

    @property
    def type(self):
        return EventType.IDENTIFICATION

    @property
    def server(self):
        return self._server

    @property
    def version(self):
        return self._version

    @property
    def invitations(self):
        return self._invitations

    @property
    def response_code(self):
        return self._response_code

    @property
    def data(self):
        if self.response_code == EventCodes.SUCCESS:
            return json.dumps({
                "type": EventType.IDENTIFICATION,
                "version": self.version,
                "server": self.server,
                "invitations": True,
                "resp_code": EventCodes.SUCCESS,
            })

        return json.dumps({
            "type": EventType.IDENTIFICATION,
            "resp_code": self.response_code,
        })

class IdentificationResponse:

    def __init__(self, data):
        self._version = data.get('version')
        self._server_name = data.get('server')
        self._invitations = data.get('invitations')

    def __repr__(self):
        return f"IdentificationResponse(version={self.version}, server_name={self.client_name}, invitations={self.invitations})"

    @property
    def type(self):
        return EventType.IDENTIFICATION

    @property
    def version(self):
        return self._version

    @property
    def server_name(self):
        return self._server_name

    @property
    def invitations(self):
        return self._invitations

class ProtocolStandardReply:

    def __init__(self, response_code=EventCodes.SUCCESS, ciphers=ciphers, hashes=hashes):
        self._response_code = response_code
        self._ciphers = ciphers
        self._hashes = hashes

    def __repr__(self):
        return f"ProtocolStandardReply(response_code={self.response_code}, ciphers={self.ciphers}, hashes={self.hashes})"

    @property
    def type(self):
        return EventType.PROTOCOL_STANDARD

    @property
    def response_code(self):
        return self._response_code

    @property
    def ciphers(self):
        return self._ciphers

    @property
    def hashes(self):
        return self._hashes

    @property
    def data(self):
        if self.response_code == EventCodes.SUCCESS:
            return json.dumps({
                "type": EventType.PROTOCOL_STANDARD,
                "ciphers": self.ciphers,
                "hashes": self.hashes,
                "resp_code": EventCodes.SUCCESS,
            })

        return json.dumps({
            "type": EventType.PROTOCOL_STANDARD,
            "resp_code": self.response_code,
        })

class SignInRequest:

    def __init__(self, data):
        self._username = data.get('username')
        self._password = data.get('password')

    def __repr__(self):
        return f"SignInRequest(username={self.username}, password={self.password})"

    @property
    def type(self):
        return EventType.USER_SIGNIN

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

class SignInReply:

    def __init__(self, response_code=EventCodes.SUCCESS, session=None):
        self._session = session
        self._response_code = response_code

    def __repr__(self):
        return f"SignInReply(session={self.session}, response_code={self.response_code})"

    @property
    def type(self):
        return EventType.USER_SIGNUP

    @property
    def session(self):
        return self._session

    @property
    def response_code(self):
        return self._response_code

    @property
    def data(self):
        if self.response_code == EventCodes.SUCCESS:
            return json.dumps({
                "type": EventType.USER_SIGNUP,
                "session": self.session,
                "resp_code": EventCodes.SUCCESS,
            })

        return json.dumps({
            "type": EventType.USER_SIGNUP,
            "resp_code": self.response_code,
        })

class SignUpRequest:

    def __init__(self, data):
        self._username = data.get('username')
        self._password = data.get('password')
        self._hash_algo = data.get('hash')

    def __repr__(self):
        return f"SignUpRequest(username={self.username}, password={self.password}, hash={self.hash_algo})"

    @property
    def type(self):
        return EventType.USER_SIGNUP

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def hash_algo(self):
        return self._hash_algo

class SignUpReply:

    def __init__(self, response_code=EventCodes.SUCCESS, session=None):
        self._session = session
        self._response_code = response_code

    def __repr__(self):
        return f"SignUpReply(session={self.session}, response_code={self.response_code})"

    @property
    def type(self):
        return EventType.USER_SIGNUP

    @property
    def session(self):
        return self._session

    @property
    def response_code(self):
        return self._response_code

    @property
    def data(self):
        if self.response_code == EventCodes.SUCCESS:
            return json.dumps({
                "type": EventType.USER_SIGNUP,
                "session": self.session,
                "resp_code": EventCodes.SUCCESS,
            })

        return json.dumps({
            "type": EventType.USER_SIGNUP,
            "resp_code": self.response_code,
        })

class SubscribeRequest:

    def __init__(self, data):
        self._session = data.get('session')

    def __repr__(self):
        return f"SubscribeRequest(session={self.session})"

    @property
    def type(self):
        return EventType.SUBSCRIBE

    @property
    def session(self):
        return self._session

class SubscribeResponse:

    def __init__(self, code):
        self._code = code

    def __repr__(self):
        return f"SubscribeResponse(code={self.code})"

    @property
    def type(self):
        return EventType.SUBSCRIBE

    @property
    def code(self):
        return self._code

    @property
    def data(self):
        return json.dumps({
            "type": EventType.SUBSCRIBE,
            "resp_code": self.code
        })

class InviteRequest:

    def __init__(self, data):
        self._source = data.get('source')
        self._dest = data.get('dest')
        self._session = data.get('session')

    def __repr__(self):
        return f"InviteRequest(source={self.source}, dest={self.dest}, session={self.session}"

    @property
    def type(self):
        return EventType.INVITE_REQUEST

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

    @property
    def session(self):
        return self._session

class KeyExchangeInitiatorRequest:
    def __init__(self, data):
        self._identity_key = data.get('ik')
        self._signed_prekey = data.get('spk')
        self._onetime_prekey = data.get('opk')

        self._source = data.get('source')
        self._dest = data.get('dest')
        self._session = data.get('session')

    def __repr__(self):
        return f"KeyExchangeInitiatorRequest()"

    @property
    def type(self):
        return EventType.KEY_EXCHANGE_INITIATE

    @property
    def identity_key(self):
        return self._identity_key

    @property
    def signed_prekey(self):
        return self._signed_prekey

    @property
    def onetime_prekey(self):
        return self._onetime_prekey

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

    @property
    def session(self):
        return self._session

class KeyExchangeResponderRequest:
    def __init__(self, data):
        self._identity_key = data.get('ik')
        self._epheremal_key = data.get('epk')

        self._source = data.get('source')
        self._dest = data.get('dest')
        self._session = data.get('session')

    def __repr__(self):
        return f"KeyExchangeResponderRequest()"

    @property
    def type(self):
        return EventType.KEY_EXCHANGE_RESPONSE

    @property
    def identity_key(self):
        return self._identity_key

    @property
    def epheremal_key(self):
        return self._epheremal_key

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

    @property
    def session(self):
        return self._session

class MessageRequest:

    def __init__(self, data):
        self._source = data.get('source')
        self._dest = data.get('dest')
        self._session = data.get('session')
        self._message = data.get('message')
        self._nonce = data.get('nonce')

    def __repr__(self):
        return f"MessageRequest(source={self.source}, dest={self.dest})"

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

    @property
    def session(self):
        return self._session

    @property
    def message(self):
        return self._message

    @property
    def nonce(self):
        return self._nonce
