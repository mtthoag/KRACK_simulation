

So I am working on a project that requires me to simulate a TCP three handshake protocol using UDP. I want to divided the project into two parts: the first is to establish and close connection; the second is to implement the flow control protocol without any package loss. Since the client and server will be interacting with each other, so I need two sockets, which means I also need two ports - 19990 and 19991 - to send and receive data between client and server.

I am having trouble with the three way handshake

    Client -> (Send SYN)
    Sever -> (Receive SYN and Send SYN ACK)
    Client -> Receives SYN ACK and Sends ACK with Data
    Server then establishes a connection and says that data has been received
    Client -> Server ACK the connection & received data. So send FIN to close the connection
    Server -> Receives FIN and closes the connection (with server_socket.close)

output on the client side:

    Send: a,1
    Receive: b, num:2
    Send: c,3
    Receive: d, num:4
    Client done

output on server side:

    Receive: a, num:1
    Send: b,2
    Receive c, num:3
    Send: d,4
    Server done.

However, what I am hoping for them to look like is like so:

client.py

    Send SYN
    Send: ,1
    Receive: num,2
    Received SYN-ACK. Send ACK & Data
    Send: I love ABC University in New York City.,3
    Receive: ,num:4
    Received ACK for data. Send FIN. Connection closed.
    Send: ,4

server.py

    Receive: ,num: 1
    Received SYN. Send SYN-ACK
    Send: ,2
    Receive: I love ABC University in New York City.,num:3
    Receive ACK. Connection Established. Received Data. Send ACK
    Send: ,4
    Receive: ,num:4
    Connection Closed

Here is the code I have for server.py:

import socket
import sys
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 19990))


def send(c,num):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss = struct.pack("!50si",c.encode(),num)
    s.sendto(ss,("127.0.0.1",19991))
    s.close()
    print("Send:%s,%d" % (c,num))


def recv():
    global server_socket
    data, addr = server_socket.recvfrom(1024)
    str,num = struct.unpack("!50si",data)
    str = str.decode("utf-8").replace("\0","")
    print("Receive:%s,num:%d" % (str,num))
    return str,num

while True:
    str,num = recv()
    num = num + 1
    str = chr(ord(str)+1)
    send(str,num)
    if str == "d":
        break

print("Server Done.")
server_socket.close()
