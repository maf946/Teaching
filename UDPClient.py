import socket
message = ""

while 1:	
	if message == "" or message == "123":	
		serverName = raw_input("Input serverName: ")
		serverPort = int(raw_input("Input serverPort: "))
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		
	print "I'm configured to send UDP packets to " + serverName + " on port " + str(serverPort)		
	message = raw_input("Input lowercase sentence (or Ctrl-Z to quit, or 123 to configure): ")	
	clientSocket.sendto(message, (serverName, serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print modifiedMessage
	clientSocket.close()