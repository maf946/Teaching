## Socket Programming: Creating Network Applications

*Note: This document is based heavily on Chapter 2.7 of our textbook. I have updated it to provide some new features, as well as compatibility with the latest version of Python, but the principles are the same as those in the textbook.*

Now that we’ve looked at a number of important network applications, let’s explore how network application programs are actually created. Recall from Section 2.1 that a typical network application consists of a pair of programs—a client program and a server program—residing in two different end systems. When these two programs are executed, a client process and a server process are created, and these processes communicate with each other by reading from, and writing to, sockets. When creating a network application, the developer’s main task is therefore to write the code for both the client and server programs.

There are two types of network applications. One type is an implementation whose operation is specified in a protocol standard, such as an RFC or some other standards document; such an application is sometimes referred to as “open,” since the rules specifying its operation are known to all. For such an implementation, the client and server programs must conform to the rules dictated by the RFC. For example, the client program could be an implementation of the client side of the HTTP protocol, described in Section 2.2 and precisely defined in RFC 2616; similarly, the server program could be an implementation of the HTTP server protocol, also precisely defined in RFC 2616. If one developer writes code for the client program and another developer writes code for the server program, and both developers carefully follow the rules of the RFC, then the two programs will be able to interoperate. Indeed, many of today’s network applications involve communication between client and server programs that have been created by independent developers—for example, a Google Chrome browser communicating with an Apache Web server, or a BitTorrent client communicating with BitTorrent tracker.

The other type of network application is a proprietary network application. In this case the client and server programs employ an application-layer protocol that has not been openly published in an RFC or elsewhere. A single developer (or development team) creates both the client and server programs, and the developer has complete control over what goes in the code. But because the code does not implement an open protocol, other independent developers will not be able to develop code that interoperates with the application.

In this section, we’ll examine the key issues in developing a client-server application, and we’ll “get our hands dirty” by looking at code that implements a very simple client-server application. During the development phase, one of the first decisions the developer must make is whether the application is to run over TCP or over UDP. Recall that TCP is connection oriented and provides a reliable byte-stream channel through which data flows between two end systems. UDP is connectionless and sends independent packets of data from one end system to the other, without any guarantees about delivery. Recall also that when a client or server program implements a protocol defined by an RFC, it should use the well-known port number associated with the protocol; conversely, when developing a proprietary application, the developer must be careful to avoid using such well-known port numbers. (Port numbers were briefly discussed in Section 2.1. They are covered in more detail in Chapter 3.)

We introduce UDP and TCP socket programming by way of a simple UDP application and a simple TCP application. We present the simple UDP and TCP applications in Python 3. We could have written the code in Java, C, or C++, but we chose Python mostly because Python clearly exposes the key socket concepts. With Python there are fewer lines of code, and each line can be explained to the novice programmer without difficulty. But there’s no need to be frightened if you are not familiar with Python. You should be able to easily follow the code if you have experience programming in Java, C, or C++.

If you are interested in client-server programming with Java, you are encouraged to see the Companion Website for this textbook; in fact, you can find there all the examples in this section (and associated labs) in Java. For readers who are interested in client-server programming in C, there are several good references available [Donahoo 2001; Stevens 1997; Frost 1994; Kurose 1996]; our Python examples below have a similar look and feel to C.

### Socket Programming with UDP

In this subsection, we’ll write simple client-server programs that use UDP; in the following section, we’ll write similar programs that use TCP.

Recall from Section 2.1 that processes running on different machines communicate with each other by sending messages into sockets. We said that each process is analogous to a house and the process’s socket is analogous to a door. The application resides on one side of the door in the house; the transport-layer protocol resides on the other side of the door in the outside world. The application developer has control of everything on the application-layer side of the socket; however, it has little control of the transport-layer side.

Now let’s take a closer look at the interaction between two communicating processes that use UDP sockets. Before the sending process can push a packet of data out the socket door, when using UDP, it must first attach a destination address to the packet. After the packet passes through the sender’s socket, the Internet will use this destination address to route the packet through the Internet to the socket in the receiving process. When the packet arrives at the receiving socket, the receiving process will retrieve the packet through the socket, and then inspect the packet’s contents and take appropriate action.

So you may be now wondering, what goes into the destination address that is attached to the packet? As you might expect, the destination host’s IP address is part of the destination address. By including the destination IP address in the packet, the routers in the Internet will be able to route the packet through the Internet to the destination host. But because a host may be running many network application processes, each with one or more sockets, it is also necessary to identify the particular socket in the destination host. When a socket is created, an identifier, called a port number, is assigned to it. So, as you might expect, the packet’s destination address also includes the socket’s port number. In summary, the sending process attaches to the packet a destination address, which consists of the destination host’s IP address and the destination socket’s port number. Moreover, as we shall soon see, the sender’s source address—consisting of the IP address of the source host and the port number of the source socket—are also attached to the packet. However, attaching the source address to the packet is typically not done by the UDP application code; instead it is automatically done by the underlying operating system.

We’ll use the following simple client-server application to demonstrate socket programming for both UDP and TCP:

1. The client reads a line of characters (data) from its keyboard and sends the data to the server.
2. The server receives the data and converts the characters to uppercase.
3. The server sends the modified data to the client.
4. The client receives the modified data and displays the line on its screen.

**Figure 1** highlights the main socket-related activity of the client and server that communicate over the UDP transport service.

![Figure 1: The client-server application using UDP](https://github.com/maf946/Teaching/raw/master/IST%20220/Socket%20Scripts/Figure1.png)

Now let’s get our hands dirty and take a look at the client-server program pair for a UDP implementation of this simple application. We also provide a detailed, line-by-line analysis after each program. We’ll begin with the UDP client, which will send a simple application-level message to the server. In order for the server to be able to receive and reply to the client’s message, it must be ready and running—that is, it must be running as a process before the client sends its message.

The client program is called UDPClient.py, and the server program is called UDPServer.py. In order to emphasize the key issues, we intentionally provide code that is minimal. “Good code” would certainly have a few more auxiliary lines, in particular for handling error cases. For this application, the server port number will be automatically selected each time the server is started.

#### Interaction Model

We will run the client and server as follows.

1. Open a terminal window and run `python3 UDPServer.py`. You should see something like the following as the output (you will almost certainly have a different IP address and port number):

	serverIP: 192.168.0.118
	Port:     49957
	Press Ctrl+Z to quit. Listening...

Make note of the serverIP and serverPort values.

2. Next, either open a second terminal window on your own machine; alternatively, work with a friend or classmate and have them run this on their machine, instead. This is designed to work on the Internet so any two Internet-connected machines should work!

On the second terminal window, run `python3 UDPClient.py -ip [IP address] -p [port number]`, making sure to include the values provided by UDPServer.py. Based on the example from the prior step, the command to run would be `python3 UDPClient.py -ip 192.168.0.118 -p 49957`. You should see something like the following as the output:

	I'm configured to send UDP packets to 192.168.0.118 on port 49957
	Press Ctrl+Z to quit.
	Input lowercase text: 

Once you enter some lowercase text, such as "udp is lazy", press Return and you should see the following outputs:

From the client side: 

	Returned from server: UDP IS LAZY
	Input lowercase text: 
	
From the server side:

	Received from 192.168.67.1#56855: udp is lazy

You can continue to run the client and server for as long as you wish. Press Ctrl+Z to quit either one.

#### UDPClient.py

Here is the code for the client side of the application:

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
		
Now let’s take a look at the various lines of code in UDPClient.py.

	import socket

The socket module forms the basis of all network communications in Python. By including this line, we will be able to create sockets within our program. 

	import argparse
	
The argparse module makes it easy for us to accept **arguments** when we launch our program. An argument is a parameter supplied to the program when it is invoked. For example, when we want to run a traceroute to ucla.edu, we run it by entering `traceroute ucla.edu`. In this case, `traceroute` is the command, and `ucla.edu` is the argument. As we write and test (and almost certainly debug) our code, it will be convenient for us to not have to manually enter the IP address and port number information each time we run the program. _Remember that from within the terminal you can re-run the last command simply by pressing the up arrow on your keyboard, then pressing Return._ This is also much better than hard-coding the IP address and port number into the script itself, for a variety of reasons. To see the documentation for our client, run `python3 UDPClient.py --help`.	

	parser = argparse.ArgumentParser(description='Run a simple UDP client.')
	parser.add_argument("--ipaddress", "-ip", help='IP address for UDP server')
	parser.add_argument("--port", "-p", type=int, help='Port number on which server is running')

Don't worry too much about the details of these lines. Basically, they set up the documentation and structure of the arguments our program can accept. Most importantly, they establish that you can specify the `ipaddress` with `-ip` and `port` with `-p`.

	args = parser.parse_args()
	serverIP = args.ipaddress
	serverPort = args.port
	
These lines take the `ipaddress` and `port` the user entered at the command line, and stores them in variables called `serverIP` and `serverPort`, respectively.

	print("I'm configured to send UDP packets to " + str(serverIP) + " on port " + serverPort)
	print ("Press Ctrl+Z to quit.")
	
Print messages to the user. Note that we use the `str()` function to convert the serverPort value to be a string, rather than an integer (earlier, we specified that the port number must be an integer; we do not want to specify that for the IP address, since it contains `.` characters, which are not integers).

	while 1:
	
This line, and everything below it which is indented by a tab, is part of an infinite loop. Once the client is configured correctly, we want to continually prompt the user for input, then communicate over the network (recall that the user can quit by pressing Ctrl+Z, or just closing the terminal window). Note that **indentation in Python is very important**. Use tab characters with care, when warranted, and only when warranted.

		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	

This line creates the client’s socket, called `clientSocket`. The first parameter indicates the address family; in particular, `AF_INET` indicates that the underlying network is using IPv4. (Do not worry about this now; we will discuss IPv4 in Chapter 4.) The second parameter indicates that the socket is of type `SOCK_DGRAM`, which means it is a UDP socket (rather than a TCP socket). Note that we are not specifying the port number of the client socket when we create it; we are instead letting the operating system do this for us. Now that the client process’s door has been created, we will want to create a message to send through the door.

		message = input("Input lowercase text: ")
		
`input()` is a built-in function in Python. When this command is executed, the user at the client is prompted with the words “Input lowercase text: ” The user then uses her keyboard to input a line, which is put into the variable `message`. Now that we have a socket and a message, we will want to send the message through the socket to the destination host.

		clientSocket.sendto(message.encode(), (serverIP, serverPort))

In the above line, we first convert the message from string type to byte type, as we need to send bytes into a socket; this is done with the `encode()` method. The method `sendto()` attaches the destination address (`serverName`, `serverPort`) to the message and sends the resulting packet into the process’s socket, `clientSocket`. (As mentioned earlier, the source address is also attached to the packet, although this is done automatically rather than explicitly by the code.) Sending a client-to-server message via a UDP socket is that simple! After sending the packet, the client waits to receive data from the server.

		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		
With the above line, when a packet arrives from the Internet at the client’s socket, the packet’s data is put into the variable `modifiedMessage` and the packet’s source address is put into the variable `serverAddress`. The variable `serverAddress` contains both the server’s IP address and the server’s port number. The program UDPClient doesn’t actually need this server address information, since it already knows the server address from the outset; but this line of Python provides the server address nevertheless. The method `recvfrom` also takes the buffer size 2048 as input. (This buffer size works for most purposes.)

		print ("Returned from server: " + modifiedMessage.decode())
		
This line prints out the text "Returned from server: " and then `modifiedMessage` on the user’s display, after converting the message from bytes to string. It should be the original line that the user typed, but now capitalized. 

		clientSocket.close()
		
This line closes the socket. Since we are at the end of the `While 1` block, we will loop back up to the top and create a new `clientSocket`. Thus, a new socket is being created each time the user enters input into UDPClient.py.
