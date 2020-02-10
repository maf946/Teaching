import socket
message = ""

while 1:
	if message == "" or message == "123":	
		serverIP = raw_input("Input server IP: ")
		serverPort = int(raw_input("Input server port: "))
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((serverIP, serverPort))
	print "I'm configured to send TCP packets to " + serverIP + " on port " + str(serverPort)		
	message = raw_input("Input lowercase sentence (or Ctrl-Z to quit, or 123 to configure): ")	
	clientSocket.send(message)
	modifiedMessage = clientSocket.recv(1024)
	print modifiedMessage
	clientSocket.close()