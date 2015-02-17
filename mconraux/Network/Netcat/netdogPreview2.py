#!/usr/bin/python
"""NetDog, just another network tool.

Usage:
    netdogPreview2.py [-t <threads>] <port>
    netdogPreview2.py -h | --help | --version

Options:
    -t <threads>        specify a number of threads to be used [default: 5]
"""

__author__ = 'huehue'

from docopt import docopt
import socket, threading

class listener(threading.Thread):
  def __init__(self, (socket, address)):
    threading.Thread.__init__(self)
    self.SOCK = socket
    self.ADDR = address
  def run(self):
    print "[*] Connected to", self.ADDR[0], 'on', self.ADDR[1], "!"
    while True:
      data = self.SOCK.recv(1024)
      if not data or data == '\n': #Stop client on newline or EOF
        break #EOF
      print '=> ',data.rstrip()
      self.SOCK.send(data)
    self.SOCK.close()
    print "[*] End of transmission !"
  def listen(self, port):
    print "[*] Server started"


arg = docopt(__doc__, version = '0.1')
limit = int(arg['-t'])
assert limit > 0, "Threads number must be positive." # assert TEST, ERRMSG
try :
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(('', int(arg['<port>'])))
  sock.listen(limit)
  print "[*] Started"
  while True:
      listener(sock.accept()).start()
except:
  print "An error occured"
print "[*] Shutting down"
