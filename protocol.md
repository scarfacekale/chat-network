# Protocol Specification
First the protocol will declare success and error codes respectively.

### Protocol Status Codes
- (0) `SUCCESS`
- (1) `BAD_TOKEN`
- (2) `USER_IN_USE`
- (3) `HASH_NOT_AVAILABLE`
- (4) `CIPHER_NOT_AVAILABLE`

The protocol exchange initiates with an identification request from the client to the server which specifies the protocol version and the client software name optionally.

### Client
```
{
    "type": "identification",
    "version": "1.0.0",
    "client": "<optional>"
}
```

After the identification request is initiated by the client, the server replies with the version of the protocol, the server software name optionally and if it is open for invitations.

### Server
```
{
    "type": "identification",
    "version": "1.0.0",
    "server": "<optional>",
    "invitations": true,
    "resp_code": 0
}
```

After the identification request is approved by both the client and the server, the client will proceed to request the available protocol standard. Including or excluding the available ciphers and or hashing algorithms. This will include the approved ciphers for communication between server and client and the hashing standard the server uses to hash client information in their database respectively.

Once the client decides to sign up to the server or proceed to communicate with the server, this information becomes crucial. The server has to comply with the demands of the user of which hashing algorithm to use in their database and for communication.

### Client
```
{
    "type": "protocol.standard",
    "standards": "ciphers,hashes"
}
```

### Server

```
{
    "type": "protocol.standard",
    "ciphers": ["xchacha-poly1305", "aes256-gcm"],
    "hashes": ["argon2id", "sha256"],
    "resp_code": 0
}
```

Once the client decides they want to sign up to the server and create an account, the client will request an account creation on the server by specifying a username, password, and the hashing algorithm to store their credentials respectively.

### Client
```
{
    "type": "signup",
    "username": "john doe",
    "password": "secretpassword",

    "hash": "sha256"
}
```

After the request is made, the server will either decline or accept the proposal of the client. The server will decide if it has the available hashing algorithm and username available respectively.

If the server decides to accept the negotiation it will reply with the newly created session token respectively.

### Server

```
{
    "type": "signup",
    "resp_code": 0,
    "session": "31dccf07-a1be-432a-af62-d5eabea2e71b"
}
```

The request can also result in an error, the user can already be in use. or the hashing algorithm is not supported by the server.

```
{
    "type": "signup",
    "resp_code": 2,
    "session": ""
}
```

```
{
    "type": "signup",
    "resp_code": 3,
    "session": ""
}
```

When the client successfully signed up to the server and saves its session token. It can request any action of a signed in user using its session token, such as messaging, inviting a person, accepting an invite or placing a voice call.

The client can also sign in if they already signed up to the server.

### Client
```
{
    "type": "signin",
    "username": "john doe",
    "password": "secretpassword",
}
```

After the request is made, the server will either decline or accept the proposal of the client.
If the server decides to accept the negotiation it will reply with the newly created session token respectively.

### Server

```
{
    "type": "signin",
    "resp_code": 0,
    "session": "31dccf07-a1be-432a-af62-d5eabea2e71b"
}
```

The request can also result in an error, the user does not exist, or the password is invalid.

```
{
    "type": "signin",
    "resp_code": 5,
    "session": ""
}
```

```
{
    "type": "signin",
    "resp_code": 6,
    "session": ""
}
```

After logging in or signing up, the client will however have to subscribe to receive events from like messages, voice calls and contact syncing.

### Client
```
{
    "type": "subscribe",
    "session": "31dccf07-a1be-432a-af62-d5eabea2e71b"
}
```

The server will validate the supplied session token and if it is correct, it will confirm the subscribe request and send the client events.

### Server
```
{
    "type": "subscribe",
    "resp_code": 0
}
```

If the session token is not correct, the server will throw an error and disconnect the client

### Server
```
{
    "type": "subscribe",
    "resp_code": 1
}
```

After the client subscribed to the events the server will supply, there is a number of events the client can receive.
The server can give an invite event from another user, a message event, or status update event.

### Client
```
{
    "type": "invite.request",
    "session": "31dccf07-a1be-432a-af62-d5eabea2e71b",
    "source": "bob",
    "dest": "alice",
}
```

After a user sends out the invite request, the user with the corresponding username will receive this request and can decide whether to accept this request to further finish the key negotiation

### Client2
```
{
    "type": "invite.accept",
    "session": "66cdbf18-a1be-432a-af62-d5eabea2e71b",
    "source": "alice",
    "dest": "bob",
}
```

The user can also reject the request

### Client2
```
{
    "type": "invite.reject",
    "session": "66cdbf18-a1be-432a-af62-d5eabea2e71b",
    "source": "alice",
    "dest": "bob",
}
```

If a client decides to send a message to a client, the following request will look like this

### Client2
```
{
    "type": "message",
    "session": "66cdbf18-a1be-432a-af62-d5eabea2e71b",
    "source": "alice",
    "dest": "bob",

    "nonce": "<nonce>",
    "message": "<message>"
}
```