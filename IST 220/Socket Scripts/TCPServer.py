import socket
import signal

def handler(signum, frame):
    	print " Quitting."
	serverSocket.close()
	quit()

signal.signal(signal.SIGTSTP, handler)

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print "IP:        " + get_ip_address()
print "Hostname:  " + socket.gethostname()
print "Port:      " + str(serverPort)
print "Press Ctrl+Z to quit. Listening..."
while 1:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)
	capitalizedSentence = sentence.upper()
	connectionSocket.send(capitalizedSentence)
	connectionSocket.close()
