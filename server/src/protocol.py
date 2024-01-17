from enum import StrEnum, IntEnum


class EventType(StrEnum):
    IDENTIFICATION          = "identification"
    PROTOCOL_STANDARD       = "protocol.standard"

    USER_SIGNUP             = "signup"
    USER_SIGNIN             = "signin"

    SUBSCRIBE               = "subscribe"

    INVITE_REQUEST          = "invite.request"
    INVITE_ACCEPT           = "invite.accept"
    INVITE_REJECT           = "invite.reject"

    KEY_EXCHANGE_INITIATE_REQUEST   = "key_exchange.initiate",
    KEY_EXCHANGE_RESPONDER_REQUEST   = "key_exchange.responder",

    MESSAGE_REQUEST                 = "message"

class EventCodes(IntEnum):
    SUCCESS                 = 0
    BAD_TOKEN               = 1
    USER_IN_USE             = 2
    HASH_NOT_AVAILABLE      = 3
    CIPHER_NOT_AVAILABLE    = 4
    USER_NOT_IN_USE         = 5
    INVALID_PASSWORD        = 6
