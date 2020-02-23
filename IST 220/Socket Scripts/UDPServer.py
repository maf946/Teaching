import socket

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]
	
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', 0))

serverIP = get_ip_address()
serverPort = serverSocket.getsockname()[1]

print ("serverIP: " + serverIP)
print ("serverPort:     " + str(serverPort))
print ("Press Ctrl+Z to quit. Listening...")

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	clientIP = str(clientAddress[0])
	clientPort = str(clientAddress[1])
	print ("Received from " + clientIP + "#" + clientPort + ": " + message.decode())
	modifiedMessage = message.upper()
	serverSocket.sendto(modifiedMessage, clientAddress)
