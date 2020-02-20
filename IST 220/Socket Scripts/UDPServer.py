import socket
import argparse

def handler(signum, frame):
	print("Closing socket and quitting…")
	serverSocket.close()
	quit()

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]
	
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', 0))

print ("IP:        " + get_ip_address())
print ("Hostname:  " + socket.gethostname())
print ("Port:      " + str(serverSocket.getsockname()[1]))
print ("Press Ctrl+Z to quit. Listening...")

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	clientIP = str(clientAddress[0])
	clientPort = str(clientAddress[1])
	print ("Received from " + clientIP + "#" + clientPort + ": " + message.decode())
	modifiedMessage = message.upper()
	serverSocket.sendto(modifiedMessage, clientAddress)
