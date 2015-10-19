#!/usr/bin/python
"""NetDog, just another network tool.

Usage:
    netdogPreview1.py <port>
    netdogPreview1.py -h | --help | --version
"""

__author__ = 'huehue'

from docopt import docopt
import socket as s

class server:
  def __init__(self):
    self.SOCK = s.socket(s.AF_INET, s.SOCK_STREAM)
  def connect(self, (socket, address)):
    print "[*] Connected to", address[0], 'on', address[1], "!"
    while True:
      data = socket.recv(1024) #Gather data
      if not data or data == '\n':
        break #EOF
      print '=> ',data.rstrip()
      socket.send(data)
    socket.close()
    print "[*] End of transmission !"
  def listen(self, port):
    print "[*] Server started"
    try :
      self.SOCK.bind(('', port))
      self.SOCK.listen(1)
      while True:
        self.connect(self.SOCK.accept())
    except:
      print "An error occured !"
    print "[*] Shutting down"

arg = docopt(__doc__, version = '0.1')
listener = server()
listener.listen(eval(arg['<port>']))
