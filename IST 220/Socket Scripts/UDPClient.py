import socket
message = ""

while 1:	
	if message == "" or message == "123":	
		serverName = input("Input serverName: ")
		serverPort = int(input("Input serverPort: "))
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		
	print("I'm configured to send UDP packets to " + serverName + " on port " + str(serverPort))
	message = input("Input lowercase sentence (or Ctrl-Z to quit, or 123 to configure): ")
	clientSocket.sendto(message, (serverName, serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print (modifiedMessage)
	clientSocket.close()