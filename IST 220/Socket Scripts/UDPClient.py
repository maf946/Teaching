import socket
import argparse

parser = argparse.ArgumentParser(description='Run a simple UDP client.')
parser.add_argument("--ipaddress", "-ip", help='IP address for UDP server')
parser.add_argument("--port", "-p", type=int, help='Port number on which server is running')
args = parser.parse_args()
serverIP = args.ipaddress
serverPort = args.port

print("I'm configured to send UDP packets to " + serverIP + " on port " + str(serverPort))
print ("Press Ctrl+Z to quit.")

while 1:	
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		
	message = input("Input lowercase text: ")
	clientSocket.sendto(message.encode(), (serverIP, serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print ("Returned from server: " + modifiedMessage.decode())
	clientSocket.close()