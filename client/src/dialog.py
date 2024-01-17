import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk

from src.protocol import (
    EventCodes,
)

def dialog_notification(window, message):
    dlg = Gtk.MessageDialog(window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
    )
    dlg.run()
    dlg.destroy()

    return False

def message_dialog(window, message):
    dialog_notification(window, message)

def message_error_dialog(window, code):

    if code == EventCodes.BAD_TOKEN:
        GObject.idle_add(dialog_notification, window, "Bad login token, please login.")
    elif code == EventCodes.USER_IN_USE:
        GObject.idle_add(dialog_notification, window, "Supplied username is already in use on this server.")
    elif code == EventCodes.HASH_NOT_AVAILABLE:
        GObject.idle_add(dialog_notification, window, "Hashing algorithm is not available on this server.")
    elif code == EventCodes.CIPHER_NOT_AVAILABLE:
        GObject.idle_add(dialog_notification, window, "Cipher algorithm is not available on this server.")
    elif code == EventCodes.USER_NOT_IN_USE:
        GObject.idle_add(dialog_notification, window, "Supplied username is not in use on this server.")
    elif code == EventCodes.INVALID_PASSWORD:
        GObject.idle_add(dialog_notification, window, "Invalid password to account.")