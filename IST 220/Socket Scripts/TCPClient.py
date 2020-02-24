import socket
import argparse

parser = argparse.ArgumentParser(description='Run a simple TCP client.')
parser.add_argument("--ipaddress", "-ip", help='IP address for TCP server')
parser.add_argument("--port", "-p", type=int, help='Port number on which server is running')
args = parser.parse_args()
serverIP = args.ipaddress
serverPort = args.port

print("I'm configured to send TCP packets to " + serverIP + " on port " + str(serverPort))
print ("Press Ctrl+Z to quit.")

while 1:
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((serverIP, serverPort))
	message = input("Input lowercase text: ")
	clientSocket.send(message.encode())
	modifiedMessage = clientSocket.recv(1024)
	print("Returned from server: " + modifiedMessage.decode())
	clientSocket.close()