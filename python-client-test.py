import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8080)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    # send data
    message = 'atom-semtype? i.pro'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(bytes(message))

    # look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print >>sys.stderr, 'Received "%s"' % data

finally:
    print >>sys.stderr, 'Closing socket!'
    sock.close()