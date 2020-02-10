import socket

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))

print ("IP:        " + socket.gethostbyname(socket.gethostname()))
print ("Hostname:  " + socket.gethostname())
print ("Port:      " + str(serverPort))
print ("Press Ctrl+Z to quit. Listening...")

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	print ("Received a message from " + clientAddress[0] + " on port " + str(clientAddress[1]) + ".")
	modifiedMessage = message.upper()
	serverSocket.sendto(modifiedMessage, clientAddress)
