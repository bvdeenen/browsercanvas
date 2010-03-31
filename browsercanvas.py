#!/usr/bin/python
# vim:tw=0


import sys,string,cgi,time, mimetypes, json , threading, Queue, subprocess, urlparse
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
#import pri

queue=Queue.Queue(0)

class MyHandler(BaseHTTPRequestHandler):

	def log_request(self, code='-', size='-'):
		pass
	def do_POST(self):
		try:
			if self.path.endswith(".dyn"):   #our dynamic content
				clen = self.headers.getheader('content-length')
				if clen:
					clen = int(clen)
				else:
					print 'POST ERROR: missing content-length'
					return

				d=self.rfile.read(clen)
				print d


				global queue
				message=queue.get()
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(json.dumps(message))
				return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	 
		except :
			pass
	def do_GET(self):
		try:
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
	
class BrowserThread(threading.Thread):	
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		a=['firefox', '-no-remote', 'http://localhost:8000/testpage.html']
		p=subprocess.Popen(a)
		print "p=",p

		
	

def main():
	try:
		server = MultiThreadedHttpServer(('', 8000), MyHandler)
		server_thread=threading.Thread(target=server.serve_forever)
		server_thread.setDaemon(True)
		server_thread.start()
		a=['firefox', '-no-remote', 'http://localhost:8000/testpage.html']
		a=['google-chrome', '--user-dir=googlechrome', '--app=http://localhost:8000/testpage.html']
		p=subprocess.Popen(a)
		dataproducer() # endless loop
		

	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()
		p.terminate()
		p.kill()

if __name__ == '__main__':
	main()

