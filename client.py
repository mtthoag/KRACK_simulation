import socket
import sys
import struct



server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 19991))


def send(c,num):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss = struct.pack("!50si",c.encode(),num)
    s.sendto(ss,("127.0.0.1",19990))
    s.close()
    print("Send:%s,%d" % (c,num))

def recv():
    global server_socket
    data, addr = server_socket.recvfrom(1024)
    str,num = struct.unpack("!50si",data)
    str = str.decode("utf-8").replace("\0","")
    print("Receive:%s,num:%d" % (str,num))
    return str,num


str = 'a'
num = 1
while True:
    send(str,num)
    str,num = recv()
    if str == "d":
        break
    str = chr(ord(str)+1)
    num = num + 1

print("Client done.")
server_socket.close()


