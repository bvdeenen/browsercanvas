#!/usr/bin/python
# vim:tw=0

import string,cgi,time, mimetypes, json , threading
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
#import pri

class MyHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith(".dyn"):   #our dynamic content
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				message={"messages": [  "$('div1').innerHTML='live'"]}
				self.wfile.write(json.dumps(message))
				return

			f = open(curdir + sep + self.path) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet

			self.send_response(200)
			self.send_header('Content-type', mimetypes.guess_type(curdir+sep+self.path))
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
			return
				
				
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	 

	def do_POST(self):
		global rootnode
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				query=cgi.parse_multipart(self.rfile, pdict)
			self.send_response(301)
			
			self.end_headers()
			upfilecontent = query.get('upfile')
			print "filecontent", upfilecontent[0]
			self.wfile.write("<HTML>POST OK.<BR><BR>");
			self.wfile.write(upfilecontent[0]);
			
		except :
			pass

class MultiThreadedHttpServer(ThreadingMixIn, HTTPServer):
	pass

def main():
	try:
		server = MultiThreadedHttpServer(('', 8000), MyHandler)
		server_thread=threading.Thread(target=server.serve_forever)
		server_thread.setDaemon(True)
		server_thread.start()
		
		while True:
			print "hoi"
			time.sleep (1)

	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()

