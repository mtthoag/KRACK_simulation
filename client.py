import socket
import sys
import struct
import random


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
    s,num = struct.unpack("!50si",data)
    s = s.decode("utf-8").replace("\0","")
    print("Receive:%s,num:%d" % (s,num))
    return s,num

def make_ptk(ANonce, SNonce):
    return ANonce + SNonce

def encrypt(ptk, msg):
	#msg in asci
	msg_ascii = ''.join(str(ord(c)) for c in msg)

	#xor packet key and msg
	encrypted_msg = ptk ^ int(msg_ascii)
	print(encrypted_msg)
	return encrypted_msg

num = 1
while True:
	#msg #1
	ANonce, num = recv()

	SNonce = '111111111111111'
	
	# msg #2
	send(SNonce, num + 1)

	ptk = make_ptk(int(ANonce), int(SNonce))
	#msg #3
	check_ptk, num = recv()

	
	if ptk == int(check_ptk):
		use_ptk = ptk
	a = str(ptk)
	
	#msg #4
	send(a , num + 1)

	msg = encrypt(ptk, "Hello!")
	#msg #4 again
	send(str(msg) , num + 1)
	break


print("Client done.")
server_socket.close()


