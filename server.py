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
