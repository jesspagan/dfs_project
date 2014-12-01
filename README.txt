-----------------------------
Contact Information
-----------------------------
Author:		                  Student Number:
   Julio De La Cruz Natera       801-12-2090
   Jessica Pagan Sanchez         801-06-5651

Email:	jjcnatera@gmail.com
        jessica.pagan3@upr.edu

Project:		CCOM4017 - Distributed File System (Final Project)

-----------------------------
Description
-----------------------------
The purpose of this project is to implement the main components of a file system by implementing a Distributed File System (DFS). These components are a metadata server, the data servers, a list client and a copy client. 

-----------------------------
Components
-----------------------------
The metadata server will manage all the functions related to the database and will serve as an intermediary between the clients and the database. Also this server maintains registry of the data node servers that are connected the DFS and the inodes of the available files in the file system.   

The data servers will be the directory or the disk space where the data blocks of a file are stored. When this servers are launched the first thing they have to do is register with the metadata server such that it can be aware of its existence. Also these data servers must receive the data blocks of a file and return them when they are asked.   

The list client is for what its name suggest. This client will ask the metadata server a list with the names and sizes of the available files in the DFS and then will display the result. 

Last but not least, the copy client. This client will manage two operations, copy files to and from the DFS. In the first operation the client will write files in the DFS by writing the data blocks of a file into the available data nodes, provided by the metadata server. In the second operation the client will be in charge of read and retrieve a file from the DFS. It has to ask the metadata server for the data blocks of an specific file and then retrieve the information from the data servers. 

---------------------------------------
How to execute the system
---------------------------------------


First of all we have to create an empty database that will contain all the information of our DFS. To do this we have to execute the following instructions: 
	1. Open the terminal
	2. Go to the directory where all the DFS files reside
	3. Enter the following command:
		python createdb.py

As simple as that we have created our empty database. Now to run the metadata server we have to execute the following instructions (assuming that we already have the terminal open and that we are in the DFS directory):
	1. Open a new tab or window in the terminal
	2. Verify if we still in the same directory, the DFS directory, if this is not the case we will have to go again to the directory where all the DFS files reside
	2. Enter the following command:
		python meta-data.py <port, default=8000>
	   (we can specify a port or use the default one). 

The next thing we have to do is to run the data node server where our data blocks of a file will be stored. To do this we have to execute the following command (assuming that we already have the terminal open and that we are in the DFS directory):
	1. Open a new tab or window in the terminal
	2. Verify if we still in the same directory, the DFS directory, if this is not the case we will have to go again to the directory where all the DFS files reside
	3. Enter the following command: 
		python data-node.py <server address> <port> <data path> <metadata port,default=8000>
	   where:
		- server address can be “localhost”
		- port can be any port we want, different of our metadata server port
		- data path is the path where the data node we are launching is located. Note that the blocks of the files stored in this data node will be in the path provided. 
		- metadata port is the port that we assign to the metadata server in the previous instructions or the default one if we use it instead. 	
	PD: We can launch as many data nodes we want by repeating 1-3 instructions, just make sure we give a different port and if we want a different path. 

Having the database, the metadata server and the data nodes running we can now execute the clients. To execute the list client we have to follow the following instructions (assuming that we already have the terminal open and that we are in the DFS directory):
	1. Open a new tab or window in the terminal 
	2. Verify if we still in the same directory, the DFS directory, if this is not the case we will have to go again to the directory where all the DFS files reside
	3. Enter the following command: 
		python ls.py <server>:<port, default=8000>
	   where:
		- server is localhost 
		- port is the port that we assign to the metadata server in the previous instructions or the default one if we use it instead.
	   Note: ’:’ character is not necessary.

If is our first time running the DFS we may not have any files in it, so we have to copy files to the DFS. We copy files running the copy client with the copy to operation. To execute this operation we need to follow this instructions (assuming that we already have the terminal open and that we are in the DFS directory):
	1. Open a new tab or window in the terminal 
	2. Verify if we still in the same directory, the DFS directory, if this is not the case we will have to go again to the directory where all the DFS files reside
	3. Enter the following command: 
		python copy.py <source file> <server>:<port>:<dfs file path>
	   where:
		- source file is the path of the file to be copy to the DFS
		- server is localhost
		- port is the port that we assign to the metadata server in the previous instructions or the default one if we use it instead.
		- dfs file path is the path or name that the file will have in the DFS

	4. To copy other files to the DFS, repeat the second instruction

Now that we have files in the DFS we can copy them to our computer. To execute the copy from operation we need to follow this instructions (assuming that we already have the terminal open and that we are in the DFS directory):
	1. Open a new tab or window in the terminal 
	2. Verify if we still in the same directory, the DFS directory, if this is not the case we will have to go again to the directory where all the DFS files reside
	3. Enter the following command: 
		python copy.py <server>:<port>:<dfs file path> <destination file>
	   where: 
		- serves ir localhost
		- port is the port that we assign to the metadata server in the previous instructions or the default one if we use it instead.
		- dfs file path is the name that the file have in the DFS
		- destination file is the name or path that the file will have once we copy it from the DFS


---------------------------------------
Who helped
---------------------------------------
Instructor: 			Jose Ortiz
Email: 					cheo@hpcf.upr.edu

Graduate Student:		Rafael Esparra
Email: 					rafael.esparra1@upr.edu

