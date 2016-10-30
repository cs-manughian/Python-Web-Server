#######################################################
#													
# Author:      Cosima Manughian-Peter
# Date:        September 21, 2015
# Purpose:     Develop a web server that handles one 
#		   HTTP request at a time. The web server 
#		   will accept and parse an HTTP request
# 		   message, get the requested file from
#		   the server's file system, create an HTTP
# 		   response message, and send the response
# 		   directly to the client.
# File name:   server.py
#
#######################################################
from socket import *
import os

# Specify host and port
server_host = "127.0.0.1"
server_port = 8080

# Create TCP socket:
# -SOCK_STREAM specifies TCP
# -AF_INET specifies address family
server_socket = socket( AF_INET, SOCK_STREAM )


# Bind the socket to host, port
server_socket.bind( (server_host, server_port) )

# Start listening on socket
# Enable server to accept one connection
server_socket.listen(1)

# Wait for incoming requests
while 1:

    # Accept a connection.
    # Socket must be bound to an address and listening.
    # Accept() returns a pair (conn, address) where conn
    # is a new socket obj usable to send and receive data
    # on the connection, and address is the address bound
    # to the socket on the other end of the connection
    conn_socket, addr = server_socket.accept()

    # Read bytes from socket
    # The return value is a bytes object
    # representing the data received
    data = conn_socket.recv(1024)

    # The parse the request message (requested file).
    # split() will parse each thing into a list.
    # Index 0 will show the type of request (GET)
    # and index 1 will show the requested file name.
    file_name  = data.split()[1]

    # Open the file but ignore first char in the
    # name because it is a '/'
    if os.path.isfile( file_name[1:] ):
       file = open( file_name[1:] )

       # Read the contents of the file to send to
       # client
       file_contents = str(file.read()).encode()

       # Send response message, header + file to client
       conn_socket.send(('HTTP/1.1 200 OK\n text/html\n\n').encode())
       conn_socket.send( file_contents )

    else:
       # File cannot be opened.
       # Generate a file not found error by sending
       # header + 404 file to client.
       pnf_file = open( '404.html' )
       conn_socket.send(('HTTP/1.1 404 File Not Found\n\n').encode())
       conn_socket.send( pnf_file.read().encode() )

    # Close connection to client but not welcoming socket
    conn_socket.close()
