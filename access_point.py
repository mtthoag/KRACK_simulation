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

def decrypt(ptk, msg):
	#msg in asci

	
	#xor packet key and msg
	decrypted_msg = ptk ^ int(msg)
	print(decrypted_msg)
	return decrypted_msg
num = 1
while True:
	ANonce = '000000000000000'
	
	#msg #1
	send(ANonce, num)
	
	#msg #2
	SNonce, num = recv()
	
	ptk = make_ptk(int(ANonce), int(SNonce))
	a = str(ptk)

	#msg #3
	send(a, num+1)
	
	#msg #4
	check_ptk, num = recv()
	if  ptk == int(check_ptk):
		use_ptk = ptk

	#msg #4 again
	msg, num = recv()
	decrypt(ptk, int(msg))
	break


print("Server Done.")
server_socket.close()
