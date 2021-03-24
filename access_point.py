import socket
import sys
import struct
import random 
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
    s,num = struct.unpack("!50si",data)
    s = s.decode("utf-8").replace("\0","")
    print("Receive:%s,num:%d" % (s,num))
    return s,num

def make_ptk(ANonce, SNonce):
    return ANonce + SNonce

while True:
	ANonce = '0'
	num = 1
	send(ANonce, num)
	SNonce, num = recv()
	ptk = make_ptk(int(ANonce), int(SNonce))
	a = str(ptk)
	send(a, num+1)
	check_ptk, num = recv()
	if  ptk == int(check_ptk):
		use_ptk = ptk
	break
    # str,num = recv()
    # num = num + 1
    # str = chr(ord(str)+1)
    # send(str,num)
    # if str == "d":
    #     break

print("Server Done.")
server_socket.close()
