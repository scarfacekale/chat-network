import json
from base64 import b64encode

database = "opt/credentials.json"
channels = "opt/channels.json"

def log_credentials(server, username, password, session):
    with open(database, "w") as fp:
        fp.write(json.dumps({
            "server": server,
            "username": username,
            "password": password,
            "session": session,
        }, indent=4))

def get_username():
    try:
        data = json.load(open(database, "r"))
        return data.get('username')
    except Exception:
        return None

def log_channel(channel):
    data = json.load(open(channels, "r"))

    key = b64encode(channel.comm.shared_key).decode()

    with open(channels, "w") as fp:
        data.append({
            "user": channel.username,
            "key": key,
        })

        fp.write(json.dumps(data, indent=4))

def get_credentials():
    data = json.load(open(database, "r"))
    return data.get('username'), data.get('password'), data.get('session'), data.get('server')

def get_channels():
    return json.load(open(channels, "r"))
