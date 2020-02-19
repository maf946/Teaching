import socket
import argparse

parser = argparse.ArgumentParser(description='Run a simple UDP server.')
parser.add_argument("--port", "-p", type=int,
                   help='Port number on which server should run')
args = parser.parse_args()
print("The command line port number is " + str(args.port))

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

if args.port:
	serverPort = args.port
else:
	serverPort = 12000
	
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))

print ("IP:        " + get_ip_address())
print ("Hostname:  " + socket.gethostname())
print ("Port:      " + str(serverPort))
print ("Press Ctrl+Z to quit. Listening...")

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	print ("Received a message from " + clientAddress[0] + " on port " + str(clientAddress[1]) + ".")
	modifiedMessage = message.upper()
	serverSocket.sendto(modifiedMessage, clientAddress)
