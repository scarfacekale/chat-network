import gi, json

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GObject
from threading import Thread
from base64 import b64decode

from src.events import (
    EventHandler   
)

from src.communication import (
    Sender,
    Receiver,
)

from src.protocol import (
    EventCodes,
)

from src.database import (
    get_credentials,
    get_channels,
    log_channel,
)

from src.objects import (
    MessageChannel
)

from src.dialog import (
    message_dialog,
    message_error_dialog
)

class ChatMessage:

    def __init__(self, username, message):
        pass

class InviteMenu:
    def __init__(self, event_handler):
        self.builder = Gtk.Builder()
        self.event_handler = event_handler

        self.builder.add_from_file('ext/invite.glade')

        self.invite_username_entry = self.builder.get_object('invite_username_entry')
        self.invite_button = self.builder.get_object('invite_button')

        self.invite_button.connect('clicked', self.invite_username)

        self.window = self.builder.get_object('InviteWindow')

        GObject.threads_init()
        self.window.present()

    def invite_username(self, button):
        username = self.invite_username_entry.get_text()
        self.event_handler.dispatcher.invite_request(username)

class SignInMenu:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.event_handler = EventHandler(self)

        self.builder.add_from_file('ext/sign_in.glade')

        self.username = None
        self.password = None

        self.account_id_entry = self.builder.get_object('account_id_entry')
        self.sign_in_stack = self.builder.get_object('sign_in_stack')

        self.password_signin_entry = self.builder.get_object('password_signin_entry')
        self.password_signup_entry = self.builder.get_object('password_signup_entry')

        self.sign_in_child = self.builder.get_object('sign_in_continue_fixed')
        self.sign_up_child = self.builder.get_object('sign_up_continue_fixed')

        self.sign_up_button = self.builder.get_object('sign_up_button')
        self.sign_up_button.connect('clicked', self.on_sign_up)

        self.complete_sign_up_button = self.builder.get_object('complete_sign_up_button')
        self.complete_sign_up_button.connect('clicked', self.on_sign_up_password)

        self.sign_in_button = self.builder.get_object('sign_in_button')
        self.sign_in_button.connect('clicked', self.on_sign_in)

        self.sign_in_button = self.builder.get_object('complete_sig_in_button')
        self.sign_in_button.connect('clicked', self.on_sign_in_password)

        self.window = self.builder.get_object('SignInWindow')

        GObject.threads_init()
        self.window.present()

    def on_sign_in(self, button):
        userid = self.account_id_entry.get_text()
        #userid = "alice@localhost:6969"

        if len(userid) == 0:
            message_dialog(self.window, "Please specify a user and server: <user>@<server>")
            return

        if not "@" in userid:
            message_dialog(self.window, "Please specify a user and server: <user>@<server>")
            return

        self.username, self.server = userid.split('@')

        self.sign_in_stack.set_visible_child(self.sign_in_child)

        t = Thread(
            target=self.event_handler.connect, 
            args=(self.server, )
        )

        t.setDaemon(True)
        t.start()

    def on_sign_up(self, button):
        userid = self.account_id_entry.get_text()
        #userid = "alice@localhost:6969"

        if len(userid) == 0:
            message_dialog(self.window, "Please specify a user and server: <user>@<server>")
            return

        if not "@" in userid:
            message_dialog(self.window, "Please specify a user and server: <user>@<server>")
            return

        self.username, self.server = userid.split('@')

        self.sign_in_stack.set_visible_child(self.sign_up_child)

        t = Thread(
            target=self.event_handler.connect, 
            args=(self.server, )
        )

        t.setDaemon(True)
        t.start()

    def on_sign_in_password(self, button):
        self.password = self.password_signin_entry.get_text()

        self.event_handler.dispatcher.signin_request(
            username = self.username,
            password = self.password,
        )

        self.window.close()

    def on_sign_up_password(self, button):
        self.password = self.password_signup_entry.get_text()

        self.event_handler.dispatcher.signup_request(
            username = self.username,
            password = self.password,
            hash_algo = "argon2id"
        )

        self.window.close()

class ChatMessaging:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.event_handler = EventHandler(self)

        self.builder.add_from_file('ext/main.glade')

        self.sidebar = self.builder.get_object('person_chooser')
        self.message_stack = self.builder.get_object('messaging_stack')

        self.sign_in_button = self.builder.get_object('account_button')
        self.connect_button = self.builder.get_object('connect_button')
        self.invite_button = self.builder.get_object('invite_button')

        self.title_bar = self.builder.get_object('title_bar')

        #self.message_stack1 = self.create_message_box(self.message_stack, "John Doe")

        self.sign_in_button.connect('clicked', self.on_sign_in)
        self.connect_button.connect('clicked', self.on_connect)
        self.invite_button.connect('clicked', self.on_invite)

        self.window = self.builder.get_object('MainWindow')

        self.message_channels = []

        self.subscribed = False

        # load all channels that are saved
        self.load_channels()

        GObject.threads_init()
        self.window.show_all()

    def load_channels(self):
        for channel in get_channels():
            self.create_channel(
                channel['user']
            )

            gtk_channel = self.get_channel(channel['user'])
            print(channel['key'])
            gtk_channel.comm.shared_key = b64decode(channel['key'])

    def get_channel(self, username):
        for channel in self.message_channels:
            if channel.username == username:
                return channel

    def get_channel_from_entry(self, entry):
        for channel in self.message_channels:
            if channel.entry == entry:
                return channel

    def create_channel(self, username, comm=Sender):

        box, message_tree, message_entry = self.create_message_box(
            message_stack = self.message_stack,
            username = username
        )

        channel = MessageChannel(
            app = self,
            comm = comm,
            username = username,
            box = box,
            text_view = message_tree,
            entry = message_entry,
        )

        self.message_channels.append(channel)
        return False

    def create_message_box(self, message_stack, username):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_center_widget()
        box.set_spacing(0)

        message_tree = Gtk.TextView()
        message_tree.set_property('bottom-margin', 500)
        message_tree.set_editable(False)
        message_tree.set_cursor_visible(False)

        message_entry = Gtk.Entry()
        message_entry.set_property('show-emoji-icon', True)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        scrolled_window.add(message_tree)

        box.add(scrolled_window)
        box.add(message_entry)

        self.message_stack.add_titled(box, '20', username)
        self.message_stack.show_all()

        message_entry.connect('activate', self.on_message)

        return box, message_tree, message_entry

    def on_message(self, entry):
        try:
            message = entry.get_text()

            if len(message) == 0:
                return

            channel = self.get_channel_from_entry(
                entry = entry
            )

            channel.send_message("You", message)
        except AttributeError:
            message_dialog(self.window, "You are not connected.")

    def on_connect(self, button):
        # check if we signed in
        username, password, session, server = get_credentials()

        if self.subscribed:
            message_dialog(self.window, "You are already connected.")
            return

        if username and password and session:

            # do we need to connect and subscribe or just connect
            if not self.event_handler.ws:
                t = Thread(
                    target=self.event_handler.connect_and_subscribe, 
                    args=(server, session)
                )

                t.setDaemon(True)
                t.start()

            else:
                self.event_handler.dispatcher.subscribe_request()

    def on_sign_in(self, button):
        sign_in = SignInMenu()

    def on_invite(self, button):
        sign_in = InviteMenu(self.event_handler)
