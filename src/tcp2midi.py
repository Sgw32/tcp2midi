#!/bin/env python3
#$Id:$

"""
forwards tcp packets to midi-out
"""

import sys
import rtmidi
import socketserver

#global 
midiout = None
midiMsg = None

class MidiMessage:
  data=[0]
  posWrite = 0
  def __init__(self):
    d0=0
  def status(self):
    return (d[0]>>4) & 0b111
  def channel(self):
    return d[0] & 0xf
  def valid(self):
    return d[0] & 0x80 >0
  def feed(self, byte):
    if self.valid:
      data.append(byte)
    else:
      if byte & 0x80:
        data=[byte]
      else:
        data=[]
    return len(data)
  def reset(self):
    self.data=[]
        
        
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    # midiMsg = None
    # midiout = None
    
    def handle(self):
        global midiout, midiMsg
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        r = midiMsg.feed(self.data)
        if r >= 4:
          midiout.send_message(midiMsg.data)
        
        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())

    def __init__(self):
      print("init...")

    
def usage():
  print("use with param -p to get list of ports.") 
  print("else: tcp2midi midiport [tcp-port [tcp-hostname]]") 
    
def main():
    global midiout, midiMsg
    host,port = "localhost", 9999

    midiMsg = MidiMessage()
    midiobj = rtmidi.MidiOut()
    midiports = midiobj.get_ports()
    midiportnum = 0
    
    le=len(sys.argv)
    if le <=1:
      usage()
      return
    try:
      if le >1:
        midiportnum = int(sys.argv[1])
      if le >2:
        port = int(sys.argv[2])
      if le >3:
        host = sys.argv[3]
    except:
      print("List of Midi Ports")
    #if sys.argv[1]=="-p":
      n=0
      for p in midiports:
        print("%d. %s"%(n, p.title()))
      return
    midiout=midiports[midiportnum]
    
      
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((host, port), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

if __name__ == "__main__":
  main()
#eof