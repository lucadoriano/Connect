"""

This WebSocket server is part of my Computer Networks (Reti di Calcolatori) project.
It is implemented using low-level networking and it provides a basic WebSocket
server that follows the most important features of RFC 6455 - The WebSocket Protocol. 

The server is designed to handle WebSocket handshakes, manage client connections,
and facilitate bidirectional communication between clients and the server.

Authored: Luca D'Oriano
Project: Reti di Calcolatori
University of Naples Parthenope

"""
import socket
import struct
import threading
import json

from hashlib import sha1
from base64 import b64encode

from typing import Callable

# Constants 
FIN = 0x80
OPCODE_TEXT = 0x1
OPCODE_CLOSE = 0x8


class WebSocket(object):
   def __init__(self, host="localhost", port=9999, certs=None):
      self.host = host
      self.port = port
      self.certs = certs
      self.clients = set()
   
   
   def start(self):
      try:
         # Creating and setting up the socket
         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.socket = sock

            # Allowing reuse of the socket address
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Binding the socket to the specified host and port
            sock.bind((self.host, self.port))
            # Listening for incoming connections.
            # 5 is the numberof unaccepted connections that the system will allow before refusing new connections.
            sock.listen(5)

            print(
               "WebSocket server started at "
               f"{'wss' if self.certs else 'ws'}://{self.host}:{self.port}"
            )

            # Accepting and handling client connections
            while True:
               client, address = sock.accept()
               print(f'Connection incoming from: {address}')
               threading.Thread(
                  target=self._handler, args=(address, client), daemon=True
               ).start()

      except KeyboardInterrupt:
         # Closing all client connections and the server socket upon keyboard interrupt
         [client.close() for client in self.clients]
         sock.close()

   def _generate_accept_key(self, key: str):
      # Generating the accept key for the WebSocket handshake
      GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
      hash = sha1((key + GUID).encode("utf-8")).digest()
      return b64encode(hash).decode("utf-8")

   def _handshake(self, data: bytes, client: socket.socket):
      # Handling WebSocket handshake
      data = data.decode("utf-8")
      if data.startswith("GET"):
         headers = data.split("\r\n")
         for header in headers:
            if "Sec-WebSocket-Key" in header:
               key = header.replace("Sec-WebSocket-Key:", "").strip()
               accept_key = self._generate_accept_key(key)
               response = (
                  "HTTP/1.1 101 Switching Protocols\r\n"
                  "Upgrade: websocket\r\n"
                  "Connection: Upgrade\r\n"
                  f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
               )
               client.send(response.encode("utf-8"))

   def _receive(self, client: socket.socket, size=1024) -> bytes:
      # Receiving data from the client
      message = bytearray()
      while True:
         chunk = client.recv(size)
         message += chunk
         if not chunk or len(chunk) < size:
               break
      return message


   def _handler(self, address, client: socket.socket):
    # Handling client connection
    while True:
        data = self._receive(client, 2048)
        if data:
            if client in self.clients:
                data, opcode = self._decode_frames(frame=data)

                if opcode == OPCODE_TEXT:
                    # Handling text data
                    self._onmessage(client, message=data.encode("utf8"))

                if opcode == OPCODE_CLOSE:
                    # Handling close frame
                    self.clients.remove(client)
                    self._onclose(client)
                    return

            else:
                # Performing handshake for new connections
                self._handshake(data, client)
                self.clients.add(client)
                # Notifying about successful handshake
                self.send(client, message=json.dumps({
                  "type": "handshake",
                  "status": "complete"
                }))

            

   def send(self, client: socket.socket, message: str):
      # Sending data to the client
      length = len(message.encode("utf8"))
      header = struct.pack("!B", FIN + OPCODE_TEXT)

      if length <= 125:
         payload_length = struct.pack("!B", length)
      elif 126 <= length <= 65535:
         payload_length = struct.pack("!BH", 126, length)
      else:
         payload_length = struct.pack("!BQ", 127, length)

      response = header + payload_length + message.encode("utf8")
      client.send(response)


   def _decode_frames(self, frame: bytearray):
      # Decoding WebSocket frames
      # check if fin is not 0 (if not 0 then is valid)
      fin = bool(frame[0] & 128)
      #check true or false to verify if data is unmasked
      masked = bool(frame[0] & 128)

      opcode = frame[0] & 127 #   (127=1111111)
      payload_length = frame[1] & 127 # unmasks data

      # if payload len is between 0 and 125 
      if payload_length <= 125: # (125=1111101)
         mask = frame[2:6]
         payload = frame[6:]

      if payload_length == 126: # (126=1111110)
         mask = frame[4:8]
         payload = frame[8:]

      if payload_length == 127:
         mask = frame[10:4]
         payload = frame[14:]
      
      message = bytearray()
      if payload is not None:
         try:
            for byte in range(len(payload)):
               message.append(payload[byte] ^ mask[byte % 4]) # xor to unmask the data
            message = message.decode("utf-8")
         except UnicodeDecodeError as e:
            message = None

      return message, opcode
   
   def onmessage(self, callback: Callable[[socket.socket, str, str], None]):
      # Callback function for receiving messages
      self._onmessage = callback


   def onopen(self, callback: Callable[[socket.socket], None]):
      # Callback function for new client connections
      self._onopen = callback


   def onclose(self, callback: Callable[[socket.socket], None]):
      # Callback function for client disconnections
      self._onclose = callback


   def _onmessage(self, client: socket.socket, message: str):
      # Default message handling function
      pass


   def _onopen(self, client: socket.socket, message: str):
      # Default function for new connections
      pass


   def _onclose(self, client: socket.socket, message: str):
      # Default function for client disconnections
      pass
