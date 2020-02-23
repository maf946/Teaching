import socket
import argparse

parser = argparse.ArgumentParser(description='Run a simple UDP client.')
parser.add_argument("--ipaddress", "-ip", help='IP address for UDP server')
parser.add_argument("--port", "-p", type=int, help='Port number on which server is running')
args = parser.parse_args()
serverIP = args.ipaddress
serverPort = args.port

message = ""
print("I'm configured to send UDP packets to " + str(ip) + " on port " + str(port))

while 1:	
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		
	message = input("Input lowercase text: ")
	clientSocket.sendto(message.encode(), (serverIP, serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print (modifiedMessage.decode())
	clientSocket.close()