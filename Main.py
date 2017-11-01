# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import View

def main():
	win = View.CMainWindow()
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()

if __name__ == "__main__":
	main()
