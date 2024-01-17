import json

from base64 import b64encode, b64decode
from src.protocol import EventCodes, EventType

class IdentificationRequest:

    def __init__(self, version, client_name):
        self._version = version
        self._client_name = client_name

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

    @property
    def data(self):
        return json.dumps({
            "type": EventType.IDENTIFICATION,
            "version": self.version,
            "client": self.client_name
        })

class IdentificationResponse:

    def __init__(self, data):
        self._version = data.get('version')
        self._server_name = data.get('server')
        self._invitations = data.get('invitations')
        self._code = data.get('resp_code')

    def __repr__(self):
        return f"IdentificationResponse(code={self.code}, version={self.version}, server_name={self.server_name}, invitations={self.invitations})"

    @property
    def type(self):
        return EventType.IDENTIFICATION

    @property
    def code(self):
        return self._code

    @property
    def version(self):
        return self._version

    @property
    def server_name(self):
        return self._server_name

    @property
    def invitations(self):
        return self._invitations

class ProtocolStandardRequest:

    def __repr__(self):
        return f"ProtocolStandardRequest()"

    @property
    def type(self):
        return EventType.PROTOCOL_STANDARD

    @property
    def data(self):
        return json.dumps({
            "type": EventType.PROTOCOL_STANDARD,
            "standards": "ciphers,hashes"
        })

class ProtocolStandardResponse:

    def __init__(self, data):
        self._ciphers = data.get('ciphers')
        self._hashes = data.get('hashes')
        self._code = data.get('resp_code')

    def __repr__(self):
        return f"ProtocolStandardResponse(code={self.code}, ciphers={self.ciphers}, hashes={self.hashes})"

    @property
    def type(self):
        return EventType.PROTOCOL_STANDARD

    @property
    def code(self):
        return self._code

    @property
    def ciphers(self):
        return self._ciphers

    @property
    def hashes(self):
        return self._hashes

    @property
    def type(self):
        return EventType.PROTOCOL_STANDARD

class SignInRequest:

    def __init__(self, username, password):
        self._username = username
        self._password = password

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

    @property
    def data(self):
        return json.dumps({
            "type": EventType.USER_SIGNIN,
            "username": self.username,
            "password": self.password,
        })

class SignInResponse:

    def __init__(self, data):
        self._session = data.get('session')
        self._code = data.get('resp_code')

    def __repr__(self):
        return f"SignInResponse(session={self.session}, code={self.code})"

    @property
    def type(self):
        return EventType.USER_SIGNIN

    @property
    def session(self):
        return self._session

    @property
    def code(self):
        return self._code

class SignUpRequest:

    def __init__(self, username, password, hash_algo="argon2id"):
        self._username = username
        self._password = password
        self._hash_algo = hash_algo

    def __repr__(self):
        return f"SignupRequest(username={self.username}, password={self.password})"

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

    @property
    def data(self):
        return json.dumps({
            "type": EventType.USER_SIGNUP,
            "username": self.username,
            "password": self.password,

            "hash": self.hash_algo
        })

class SignUpResponse:

    def __init__(self, data):
        self._session = data.get('session')
        self._code = data.get('resp_code')

    def __repr__(self):
        return f"SignUpResponse(session={self.session}, code={self.code})"

    @property
    def type(self):
        return EventType.USER_SIGNUP

    @property
    def session(self):
        return self._session

    @property
    def code(self):
        return self._code

class SubscribeRequest:

    def __init__(self, session):
        self._session = session

    def __repr__(self):
        return f"SubscribeRequest(session={self.session}"

    @property
    def type(self):
        return EventType.SUBSCRIBE

    @property
    def session(self):
        return self._session

    @property
    def data(self):
        return json.dumps({
            "type": EventType.SUBSCRIBE,
            "session": self.session
        })

class SubscribeResponse:

    def __init__(self, data):
        self._code = data.get('resp_code')

    def __repr__(self):
        return f"SubscribeResponse(code={self.code})"

    @property
    def type(self):
        return EventType.SUBSCRIBE

    @property
    def code(self):
        return self._code

class InviteRequest:

    def __init__(self, source, dest, session):
        self._source = source
        self._dest = dest
        self._session = session

    def __repr__(self):
        return f"InviteRequest(source={self.source}, dest={self.dest}, session={self.session})"

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

    @property
    def data(self):
        return json.dumps({
            "type": EventType.INVITE_REQUEST,
            "source": self.source,
            "dest": self.dest,
            "session": self.session
        })

class InviteRequestResponse:

    def __init__(self, data):
        self._source = data.get('source')
        self._dest = data.get('dest')

    def __repr__(self):
        return f"InviteRequest(source={self.source}, dest={self.dest})"

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

    @property
    def data(self):
        return json.dumps({
            "type": EventType.INVITE_REQUEST,
            "source": self.source,
            "dest": self.dest
        })

class KeyExchangeInitiatorRequest:
    def __init__(self, source, dest, session, identity_key, signed_prekey, onetime_prekey):
        self._identity_key = identity_key
        self._signed_prekey = signed_prekey
        self._onetime_prekey = onetime_prekey

        self._source = source
        self._dest = dest
        self._session = session

    def __repr__(self):
        return f"KeyExchangeInitiatorRequest(source={self.source}, dest={self.dest})"

    @property
    def type(self):
        return EventType.KEY_EXCHANGE_INITIATE_REQUEST

    @property
    def identity_key(self):
        return b64encode(self._identity_key).decode()

    @property
    def signed_prekey(self):
        return b64encode(self._signed_prekey).decode()

    @property
    def onetime_prekey(self):
        return b64encode(self._onetime_prekey).decode()

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
    def data(self):
        return json.dumps({
            "type": EventType.KEY_EXCHANGE_INITIATE_REQUEST,
            "session": self.session,
            "source": self.source,
            "dest": self.dest,

            "ik": self.identity_key,
            "spk": self.signed_prekey,
            "opk": self.onetime_prekey
        })

class KeyExchangeInitiatorResponse:
    def __init__(self, data):
        self._identity_key = data.get('ik')
        self._signed_prekey = data.get('spk')
        self._onetime_prekey = data.get('opk')

        self._source = data.get('source')
        self._dest = data.get('dest')
        self._session = data.get('session')

    def __repr__(self):
        return f"KeyExchangeInitiatorResponse(source={self.source}, dest={self.dest})"

    @property
    def type(self):
        return EventType.KEY_EXCHANGE_INITIATE_REQUEST

    @property
    def identity_key(self):
        return b64decode(self._identity_key)

    @property
    def signed_prekey(self):
        return b64decode(self._signed_prekey)

    @property
    def onetime_prekey(self):
        return b64decode(self._onetime_prekey)

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
    def __init__(self, source, dest, session, identity_key, epheremal_key):
        self._identity_key = identity_key
        self._epheremal_key = epheremal_key

        self._source = source
        self._dest = dest
        self._session = session

    def __repr__(self):
        return f"KeyExchangeResponderRequest(source={self.source}, dest={self.dest})"

    @property
    def type(self):
        return EventType.KEY_EXCHANGE_RESPONDER_REQUEST

    @property
    def identity_key(self):
        return b64encode(self._identity_key).decode()

    @property
    def epheremal_key(self):
        return b64encode(self._epheremal_key).decode()

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
    def data(self):
        return json.dumps({
            "type": EventType.KEY_EXCHANGE_RESPONDER_REQUEST,
            "session": self.session,
            "source": self.source,
            "dest": self.dest,

            "ik": self.identity_key,
            "epk": self.epheremal_key
        })

class KeyExchangeResponderResponse:
    def __init__(self, data):
        self._identity_key = data.get('ik')
        self._epheremal_key = data.get('epk')

        self._source = data.get('source')
        self._dest = data.get('dest')
        self._session = data.get('session')

    def __repr__(self):
        return f"KeyExchangeResponderResponse(source={self.source}, dest={self.dest})"

    @property
    def type(self):
        return EventType.KEY_EXCHANGE_RESPONDER_REQUEST

    @property
    def identity_key(self):
        return b64decode(self._identity_key)

    @property
    def epheremal_key(self):
        return b64decode(self._epheremal_key)

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

    def __init__(self, source, dest, message, nonce, session):
        self._source = source
        self._dest = dest
        self._session = session
        self._message = message
        self._nonce = nonce

    def __repr__(self):
        return f"MessageRequest(source={self.source}, dest={self.dest})"

    @property
    def message(self):
        return b64encode(self._message).decode()

    @property
    def nonce(self):
        return b64encode(self._nonce).decode()

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
    def data(self):
        return json.dumps({
            "type": EventType.MESSAGE_REQUEST,
            "session": self.session,
            "source": self.source,
            "dest": self.dest,

            "nonce": self.nonce,
            "message": self.message
        })

class MessageResponse:

    def __init__(self, data):
        self._source = data.get('source')
        self._dest = data.get('dest')
        self._session = data.get('session')
        self._message = data.get('message')
        self._nonce = data.get('nonce')

    def __repr__(self):
        return f"MessageResponse(source={self.source}, dest={self.dest})"

    @property
    def message(self):
        return b64decode(self._message)

    @property
    def nonce(self):
        return b64decode(self._nonce)

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

    @property
    def session(self):
        return self._session
