###############################################################################
#
# Filename: mds_db.py
# Author: Jose R. Ortiz and ... (hopefully some students contribution)
#
# Description:
# 	Copy client for the DFS
#
#

import socket
import sys
import os.path

from Packet import *

def usage():
	print """Usage:\n\tFrom DFS: python %s <server>:<port>:<dfs file path> <destination file>\n\tTo   DFS: python %s <source file> <server>:<port>:<dfs file path>""" % (sys.argv[0], sys.argv[0])
	sys.exit(0)

def copyToDFS(address, fname, path):
	""" Contact the metadata server to ask to copy file fname,
	    get a list of data nodes. Open the file in path to read,
	    divide in blocks and send to the data nodes. 
	"""

	# Create a connection to the data server
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(address)


	# Read file
	f = open(path, 'rb')
	fdata = f.read()
	f.close()

	fsize = len(fdata)


	# Create a Put packet with the fname and the length of the data,
	# and sends it to the metadata server 
	p = Packet()
	p.BuildPutPacket(fname, fsize)
	sock.sendall(p.getEncodedPacket())


	# If no error or file exists
	r = sock.recv(1024)
	if r == "DUP":
		print "Duplicate File"
		return


	# Get the list of data nodes.
	else:
		p.DecodePacket(r)
		dnodes = p.getDataNodes()
		# print "Data Nodes list:", dnodes

	# Divide the file in blocks
		blist = []

		dnsize = len(dnodes)
		bsize = (fsize/dnsize)
		# counter = 1
		# dsize = fsize/dnsize
		# tmp = dsize

	# Verify if the data block size is greater than the buffer size	
		# while(tmp > 1024):
		# 	counter += 1
		# 	tmp = dsize / counter

		# chunks = counter * dnsize
		# bsize = (fsize / chunks)

		# print "Chunks: ", chunks, "bsize: ", bsize

		for i in range(0, fsize, bsize):
			if (i/bsize) + 1 == dnsize:
				blist.append(fdata[i:])
				break

			else:
				blist.append(fdata[i:i + bsize])

		# print "data blocks: ", blist


	# Send the blocks to the data servers


	for i in dnodes:
		sockdn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sockdn.connect((i[0], i[1]))

		p.BuildPutPacket(fname, fsize)
		sockdn.sendall(p.getEncodedPacket())
		r = sockdn.recv(1024)

		data = blist.pop(0)

		if r == "OK":
			size = len(data)

			sockdn.sendall(str(size))
			r = sockdn.recv(1024)

			while len(data) > 0:
				print data
				if data > 1024:
					a = data[0:1024]
					data = data[1024:]
					print a

					sockdn.sendall(a)
					r = sockdn.recv(1024)

			#Adding the chunk id to the data nodes list 
			r = sockdn.recv(1024)
			i.append(r)
	
		sockdn.close()

	# Notify the metadata server where the blocks are saved.
	p.BuildDataBlockPacket(fname, dnodes)

	# We have to create a new socket to send the blocks and 
	# we don't know why
	sockBlks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sockBlks.connect(address)
	sockBlks.sendall(p.getEncodedPacket())

def copyFromDFS(address, fname, path):
	""" Contact the metadata server to ask for the file blocks of
	    the file fname.  Get the data blocks from the data nodes.
	    Saves the data in path.
	"""

   	# Contact the metadata server to ask for information of fname
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(address)

	p = Packet()
	p.BuildGetPacket(fname)
	sock.sendall(p.getEncodedPacket())

	
	# If there is no error response Retreive the data blocks
	r = sock.recv(1024)
	p.DecodePacket(r)
	dnList = p.getDataNodes()

	print dnList
	f = open(path, 'a')

	# Connect to each data node to retrieve 
	for dnode in dnList:
		sockdn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sockdn.connect((dnode[0], dnode[1]))

		p.BuildGetDataBlockPacket(dnode[2])
		sockdn.sendall(p.getEncodedPacket())
		dsize = sockdn.recv(1024)
		print dsize
		dsize = int(dsize)

		sockdn.sendall("OK")

		# Save the file
		print "antes de"
		data = ""
		while(len(data) < dsize):
			res = sockdn.recv(1024)
			data = data + res
			sockdn.sendall("OK")

		f.write(data)
		sockdn.close()


	f.close()

if __name__ == "__main__":
#	client("localhost", 8000)
	if len(sys.argv) < 3:
		usage()

	file_from = sys.argv[1].split(":")
	file_to = sys.argv[2].split(":")

	if len(file_from) > 1:
		ip = file_from[0]
		port = int(file_from[1])
		from_path = file_from[2]
		to_path = sys.argv[2]

		if os.path.isdir(to_path):
			print "Error: path %s is a directory.  Please name the file." % to_path
			usage()

		copyFromDFS((ip, port), from_path, to_path)

	elif len(file_to) > 2:
		ip = file_to[0]
		port = int(file_to[1])
		to_path = file_to[2]
		from_path = sys.argv[1]

		if os.path.isdir(from_path):
			print "Error: path %s is a directory.  Please name the file." % from_path
			usage()

		copyToDFS((ip, port), to_path, from_path)


