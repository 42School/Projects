#!/usr/bin/python
"""NetDog, just another network tool.

Usage:
    netdogChat.py [-t <threads>] <port>
    netdogChat.py -h | --help | --version

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
    self.SOCK.send("Please, choose a name ! : ")
    self.name = self.SOCK.recv(1024).rstrip()
    with lock:
      clients.append(self)
    print "[*] Connected to", self.ADDR[0], 'as', self.name, "!"
    while True:
      data = self.SOCK.recv(1024)
      if not data or data == '\n': #Stop client on newline or EOF
        break #EOF
      print "["+self.name+"]:",data.rstrip()
      for bro in clients:
        if bro != self:
          bro.SOCK.send('['+self.name + ']: ' + data)
    self.SOCK.close()
    with lock:
      clients.remove(self)
    print "[*] End of transmission !"


arg = docopt(__doc__, version = '0.1')
limit = int(arg['-t'])
assert limit > 0, "Threads number must be positive." # assert TEST, ERRMSG
try :
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(('', int(arg['<port>'])))
  sock.listen(limit)
  lock = threading.Lock()
  clients = []
  print "[*] Started"
  while True:
      listener(sock.accept()).start()
except:
  print "An error occured"
print "[*] Shutting down"
