import time
from datetime import datetime

from src.communication import (
    Sender,
    Receiver
)

from src.database import (
    log_channel
)

class MessageChannel:

    def __init__(self, app, username, box, text_view, entry, comm=Sender):
        self.app = app
        self.username = username
        self.box = box
        self.text_view = text_view
        self.entry = entry

        self.buffer = self.text_view.get_buffer()

        self.comm = comm()
        self.messages = []

    def receive_message(self, message):

        message_format = f"[{datetime.now()}] [{self.username}]: {message}"

        self.messages.append(message_format)
        self.buffer.insert_at_cursor(message_format + '\n')
        self.entry.set_text("")

        mark = self.buffer.create_mark("end", self.buffer.get_end_iter(), False)
        self.text_view.scroll_mark_onscreen(mark)

        if self.comm.shared_key is None:

            self.app.event_handler.dispatcher.key_exchange_request(
                channel = self,
                username = self.username
            )

            # primitive lock until key is calculated
            while self.comm.shared_key is None:
                time.sleep(1)

            log_channel(
                channel = self
            )

    def send_message(self, username, message):

        message_format = f"[{datetime.now()}] [{username}]: {message}"

        self.messages.append(message_format)
        self.buffer.insert_at_cursor(message_format + '\n')
        self.entry.set_text("")

        mark = self.buffer.create_mark("end", self.buffer.get_end_iter(), False)
        self.text_view.scroll_mark_onscreen(mark)

        if self.comm.shared_key is None:
            self.app.event_handler.dispatcher.key_exchange_request(
                channel = self,
                username = self.username
            )

            # primitive lock until key is calculated
            while self.comm.shared_key is None:
                time.sleep(1)

            log_channel(
                channel = self
            )

        self.app.event_handler.dispatcher.send_message(
            username = self.username, 
            message = message,
            comm = self.comm
        )
