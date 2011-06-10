#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#~ Copyright (C) 2011 by Gabriel Shahzad
#~ 
#~ Permission is hereby granted, free of charge, to any person obtaining a copy
#~ of this software and associated documentation files (the "Software"), to deal
#~ in the Software without restriction, including without limitation the rights
#~ to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#~ copies of the Software, and to permit persons to whom the Software is
#~ furnished to do so, subject to the following conditions:
#~ 
#~ The above copyright notice and this permission notice shall be included in
#~ all copies or substantial portions of the Software.
#~ 
#~ THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#~ IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#~ FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#~ AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#~ LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#~ OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#~ THE SOFTWARE.


import pygtk, gtk, subprocess, os, sys, webbrowser
pygtk.require('2.0')

class lamp:
	
	def destroy(self, widget, data=None):
		gtk.main_quit()
		
	def on_window_destroy(self, widget, data=None):
		gtk.main_quit()
	

	def error_message(self, message):
		print message
		dialog = gtk.MessageDialog(None,
									gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
									gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
		dialog.run()
		dialog.destroy()
		
	def push_msg(self, widget, data):
		buff = "Item %d" % self.count
		self.count = self.count + 1
		self.statusbar.push(data, buff)
		return
	
	#starts the servers
	def start(self, widget, data=None):
		#self.statusbar.push(1, "Starte server...")
		subprocess.call(["gksu service apache2 start"], shell=True)
		subprocess.call(["gksu service mysql start"], shell=True)
		self.statusbar.push(2, "Server sind online!")
	
	# stops the servers
	def stop(self, widget, data=None):
		#self.statusbar.push(3, "Stoppe server...")
		subprocess.call(["gksu service apache2 stop"], shell=True)
		subprocess.call(["gksu service mysql stop"], shell=True)
		self.statusbar.push(4, "Server sind offline!")
		
	# opens the currently set default webbrowser with the url corresponding to /var/www/welcome
	def browser_o(self, widget, data=None):
		#self.statusbar.push(5, "Öffne Startseite...")
		webbrowser.open("http://localhost/")
		self.statusbar.push(6, "http://localhost/ geladen!")
	
	# opens apache.conf
	def apache_conf(self, widget, data=None):
		subprocess.call(["gksu gedit /etc/apache2/apache2.conf"], shell=True)
		self.statusbar.push(7, "Öffne Apache Konfiguration...")
	
	# opens mysql.conf
	def mysql_conf(self, widget, data=None):
		subprocess.call(["gksu gedit /etc/mysql/my.cnf"], shell=True)
		self.statusbar.push(8, "Öffne MySql Konfiguration...")
	
	# about dialog
	def about(self, widget, data=None):
		about = gtk.AboutDialog()
		about.set_version("0.1")
		about.set_copyright("(c) Gabriel Shahzad")
		about.set_name("LAMP")
		about.set_comments("LAMP ist eine grafische Benutzeroberfläche für die Linux Apache MySql PHP Umgebung.")
		about.set_license("Copyright (C) 2011 by Gabriel Shahzad\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the \"Software\"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.")
		about.set_website("http://herr-gabriel.de/")
		about.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.abspath("/opt/lamp/"), "icon.svg")))
		def close(w, res):
				if res == gtk.RESPONSE_CANCEL:
					w.hide()
		about.connect("response", close)
		about.show()	
		
	def __init__(self):
		
		try:
			builder = gtk.Builder()
			builder.add_from_file(os.path.join(os.path.abspath("/opt/lamp/"), "lamp.xml"))
			builder.connect_signals({ "on_window_destroy" : gtk.main_quit })
		except:
			self.error_message("Konnte die UI XML Datei nicht laden.")
			sys.exit(1)
		
		self.count = 1
		
		self.window = builder.get_object("lamp_main_window")
		self.statusbar = builder.get_object("statusbar1")
		self.online = builder.get_object("start")
		self.online.connect("clicked", self.start)
		self.offline = builder.get_object("stop")
		self.offline.connect("clicked", self.stop)
		self.browser = builder.get_object("browser")
		self.browser.connect("clicked", self.browser_o)
		self.quit = builder.get_object("quit")
		self.quit.connect("clicked", self.destroy)
		self.about2 = builder.get_object("about")
		self.about2.connect("activate", self.about)	
		self.menu_quit = builder.get_object("menu_quit")
		self.menu_quit.connect("activate", self.destroy)
		self.edit_apache = builder.get_object("menu_apache")
		self.edit_apache.connect("activate", self.apache_conf)
		self.edit_mysql = builder.get_object("menu_mysql")
		self.edit_mysql.connect("activate", self.mysql_conf)
			
	def main(self):
	 	self.window.show()
		gtk.main()
		
if __name__ == '__main__':
	app = lamp()
	app.main()
