###############################################################################
#
# Filename: data-node.py
# Author: Jose R. Ortiz, Julio J. De la Cruz and Jessica Pagan
# Course: CCOM4017
#
# Department of Computer Science
# University of Puerto Rico, Rio Piedras Campus
#
# Description:
# 	data node server for the DFS
#	It will be register with the data node
#	Connect to copy client to storage or retrieve data from its directory
#

from Packet import *
import sys
import socket
import SocketServer
import uuid
import os.path

def usage():
	print """Usage: python %s <server> <port> <data path> <metadata port,default=8000>""" % sys.argv[0] 
	sys.exit(0)


def register(meta_ip, meta_port, data_ip, data_port):
	"""Creates a connection with the metadata server and
	   register as data node
	"""

	# Establish connection
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((meta_ip, meta_port))
		

	# Register data_node to meta_data
	try:
		response = "NAK"
		sp = Packet()
		while response == "NAK":
			sp.BuildRegPacket(data_ip, data_port)
			sock.sendall(sp.getEncodedPacket())
			response = sock.recv(1024)

			if response == "DUP":
				print "Duplicate Registration"

		 	if response == "NAK":
				print "Registratation ERROR"


	finally:
		sock.close()
	

class DataNodeTCPHandler(SocketServer.BaseRequestHandler):

	def handle_put(self, p):
		"""Receives a block of data from a copy client, and 
		   saves it with an unique ID.  The ID is sent back to the
		   copy client.
		"""

		self.request.send("OK")

		# Generates an unique block id.
		blockid = str(uuid.uuid1())

		# Open the file for the new data block.
		f = open(DATA_PATH + blockid, 'w')

		# Receive the data block.
		bsize = self.request.recv(1024)
		self.request.send("OK")
		
		# Convert the socket response in integers
		# and create the data list that storage the data that will be receive
		bsize = int(bsize)
		data = ""


		# Send data in 1024 size parts
		while (len(data) < bsize):
			r = self.request.recv(1024)
			data = data + r
			self.request.send("OK")

		# Save received data to file
		f.write(data)
		r = self.request.recv(1024)


		# Send the block id back
		print "Block id:", blockid

		self.request.sendall(blockid)
		self.request.close()


	def handle_get(self, p):
		# Get the block id from the packet
		blockid = p.getBlockID()

		# Read the file with the block_id
		f = open(DATA_PATH + blockid, 'rb')
		data = f.read()
		f.close()

		# Retrieve and send data size to copy client
		dsize = len(data)

		self.request.sendall(str(dsize))
		r = self.request.recv(1024)

		# Send it back to the copy client.
		while len(data) > 0:
			chunk = data[0:1024]
			data = data[1024:]

			self.request.sendall(chunk)
			r = self.request.recv(1024)

		self.request.close()


	def handle(self):
		# Receive a msg from the copy client
		msg = self.request.recv(1024)

		# Define a packet object and decode it
		p = Packet()
		p.DecodePacket(msg)

		# Copy client asking for data node to put data
		cmd = p.getCommand()
		if cmd == "put":
			self.handle_put(p)

		# Copy client asking for data node to get data
		elif cmd == "get":
			self.handle_get(p)
		

if __name__ == "__main__":

	META_PORT = 8000
	if len(sys.argv) < 4:
		usage()

	try:
		HOST = sys.argv[1]
		PORT = int(sys.argv[2])
		DATA_PATH = sys.argv[3]

		if len(sys.argv) > 4:
			META_PORT = int(sys.argv[4])

		if not os.path.isdir(DATA_PATH):
			print "Error: Data path %s is not a directory." % DATA_PATH
			usage()

	except:
		usage()


	register("localhost", META_PORT, HOST, PORT)
	server = SocketServer.TCPServer((HOST, PORT), DataNodeTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
 	server.serve_forever()
