#!/usr/bin/python
# vim:tw=0


import sys,string,cgi,time, mimetypes, json , threading, Queue
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
#import pri

queue=Queue.Queue(0)

class MyHandler(BaseHTTPRequestHandler):

	def log_request(self, code='-', size='-'):
		pass
	def do_GET(self):
		try:
			if self.path.endswith(".dyn"):   #our dynamic content
				global queue
				message=queue.get()
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
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
	 
		except :
			pass

class MultiThreadedHttpServer(ThreadingMixIn, HTTPServer):
	pass

def dataproducer():
	global queue
	i=1
	while True:
		
		# for example:
		# $('div1').innerHTML='pietje'
		m=sys.stdin.readline().strip()

		message={"messages": [ m ]}
		i+=1
		queue.put(message)
		time.sleep (1)
	

def main():
	try:
		server = MultiThreadedHttpServer(('', 8000), MyHandler)
		server_thread=threading.Thread(target=server.serve_forever)
		server_thread.setDaemon(True)
		server_thread.start()
		dataproducer() # endless loop
		

	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()

