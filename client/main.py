import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

from src.gtk import ChatMessaging

chat = ChatMessaging()
Gtk.main()
