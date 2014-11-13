###############################################################################
#
# Filename: ls.py
# Author: Jose R. Ortiz, Julio J. De la Cruz and Jessica Pagan
# Course: CCOM4017
#
# Department of Computer Science
# University of Puerto Rico, Rio Piedras Campus
#
# Description:
# 	List client for the DFS.
#	Display all the files that are storaged in the data base.
#



import socket
import sys
from Packet import *

def usage():
	print """Usage: python %s <server>:<port, default=8000>""" % sys.argv[0] 
	sys.exit(0)

def client(ip, port):

	# Contacts the metadata server and ask for list of files.
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, port))

	# Creates a packet to ask the metadata to send the file list
	p = Packet()
	p.BuildListPacket()
	sock.sendall(p.getEncodedPacket())

	# Received the list of files and display the information
	r = sock.recv(1024)
	# print r, type(r)

	p.DecodePacket(r)
	filelist = p.getFileArray()

	for item in filelist:
		print item[0], item[1], "bytes"
	# print filelist[0][0], "este es el 0 de filelist"


if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		usage()

	ip = None
	port = None 
	server = sys.argv[1].split(":")
	if len(server) == 1:
		ip = server[0]
		port = 8000
	elif len(server) == 2:
		ip = server[0]
		port = int(server[1])

	if not ip:
		usage()

	client(ip, port)
