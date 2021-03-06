###############################################################################
#
# Filename: meta-data.py
# Author: Jose R. Ortiz, Julio J. De la Cruz and Jessica Pagan
# Course: CCOM4017
#
# Department of Computer Science
# University of Puerto Rico, Rio Piedras Campus
#
# Description:
#	Link between clients and data base.
# 	Communicates with mds_db.py and request to run queries on data base.
#	

from mds_db import *
from Packet import *
import sys
import SocketServer

def usage():
	print """Usage: python %s <port, default=8000>""" % sys.argv[0] 
	sys.exit(0)


class MetadataTCPHandler(SocketServer.BaseRequestHandler):

	def handle_reg(self, db, p):
		"""Register a new client to the DFS  ACK if successfully REGISTERED
			NAK if problem, DUP if the IP and port already registered
		"""

		try:
			# If data node registration was successfull, send acknowledge
			if db.AddDataNode(p.getAddr(), p.getPort()) != 0:
				self.request.sendall("ACK") 

			# If data node is duplicate, send duplicated
			else:
				self.request.sendall("DUP")


		# If something went wrong, send no acknowledge
		except:
			self.request.sendall("NAK")


	def handle_list(self, db):
		"""Get the file list from the database and send list to client"""

		try:
			# Search files information from data base
			dbfiles = db.GetFiles()

			# Create packet for sending to client
			p = Packet()
			p.BuildListResponse(dbfiles)

			# Sending encoded packet to list client
			self.request.sendall(p.getEncodedPacket())


		except:
			self.request.sendall("NAK")	


	def handle_put(self, db, p):
		"""Insert new file into the database and send data nodes to save
		   the file.
		"""
	       
		info = p.getFileInfo()

		# If file inserted successfully, 
		# send data nodes available in data base.
		if db.InsertFile(info[0], info[1]):
			dnodes = db.GetDataNodes()
			p.BuildPutResponse(dnodes)
			self.request.sendall(p.getEncodedPacket())
			
		else:
			self.request.sendall("DUP")

	
	def handle_get(self, db, p):
		"""Check if file is in database and return list of
			server nodes that contain the file.
		"""

		# Get the file name from packet and then 
		# get the file size and array of metadata server
		fname = p.getFileName()
		fsize, MetaArray = db.GetFileInode(fname)


		if fsize:
			p.BuildGetResponse(MetaArray, fsize)
			self.request.sendall(p.getEncodedPacket())

		else:
			self.request.sendall("NFOUND")


	def handle_blocks(self, db, p):
		"""Add the data blocks to the file inode"""

		# Get file name and blocks from packet
		fname = p.getFileName()
		blocks = p.getDataBlocks()
		
		# Add blocks to file inode
		db.AddBlockToInode(fname, blocks)
		

	def handle(self):

		# Establish a connection with the local database
		db = mds_db("dfs.db")
		db.Connect()

		# Define a packet object to decode packet messages
		p = Packet()

		# Receive a msg from the list, data-node, or copy clients
		msg = self.request.recv(1024)
		
		# Decode the packet received
		p.DecodePacket(msg)

		# Extract the command part of the received packet
		cmd = p.getCommand()


		# Invoke the proper action 
		if   cmd == "reg":
			# Registration client
			self.handle_reg(db, p)

		elif cmd == "list":
			# Client asking for a list of files
			self.handle_list(db)
		
		elif cmd == "put":
			# Client asking for servers to put data
			self.handle_put(db, p)
		
		elif cmd == "get":
			# Client asking for servers to get data
			self.handle_get(db, p)

		elif cmd == "dblks":
			# Client sending data blocks for file
			self.handle_blocks(db, p)


		db.Close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    if len(sys.argv) > 1:
    	try:
    		PORT = int(sys.argv[1])
    	except:
    		usage()

    server = SocketServer.TCPServer((HOST, PORT), MetadataTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
