import asyncio, json
import websockets
 
async def test():
    async with websockets.connect('ws://localhost:6969') as ws:
        identification = {
            "type": "identification",
            "version": "1.0.0",
            "client": "None"
        }

        await ws.send(json.dumps(identification))

        data = await ws.recv()
        print(data)
 
        standards = {
            "type": "protocol.standard",
            "standards": "ciphers,hashes"
        }

        await ws.send(json.dumps(standards))

        data = await ws.recv()
        print(data)

        signup = {
            "type": "signup",
            "username": "john doe",
            "password": "secretpassword",

            "hash": "argon2id"
        }

        await ws.send(json.dumps(signup))

        data = await ws.recv()
        print(data)



asyncio.run(test())