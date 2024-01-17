import uuid

class Client:

    def __init__(self, ws, name, session):
        self.subscribed = False

        self._session = session
        self._name = name
        self._ws = ws

    @property
    def name(self):
        return self._name

    @property
    def session(self):
        return self._session

    @property
    def ws(self):
        return self._ws

    def connect(self, ws):
        self._ws = ws
        self.subscribed = True

class Clients:
    
    def __init__(self):
        self.clients = []

    def get_from_username(self, name):
        for client in self.clients:
            if client.name == name:
                return client
        return None

    def get_from_session(self, session):
        for client in self.clients:
            if client.session == session:
                return client
        return None

    def create(self, ws, name, session):
        client = Client(
            ws = ws,
            name = name,
            session = session
        )

        self.add(client)

    def get(self, name):
        for client in self.clients:
            if client.name == name:
                return client

    def add(self, client):
        self.clients.append(client)

    def remove(self, client):
        if client in self.clients:
            self.clients.remove(client)
