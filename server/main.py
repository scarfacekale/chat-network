from src.database import DatabaseHandler
from src.server import ChatServer

server = ChatServer(
    host='0.0.0.0',
    port=6969
)

server.run()
