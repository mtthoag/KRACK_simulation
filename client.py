import socket
import sys
import struct
import random


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 19991))


def send(c,num):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss = struct.pack("!50si",c.encode(),num)
    s.sendto(ss,("127.0.0.1",19992))
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
	#transform msg to hex
	msg_hex = msg.encode('utf-8').hex()
	
	#xor packet key and msg
	encrypted_msg = ptk ^ int(msg_hex, 16)
	print(encrypted_msg)
	return encrypted_msg

num = 1
while True:
	#msg #1
	ANonce, num = recv()

	SNonce = '111111111111'
	
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

	#if msg3 is retransmitted reset the ptk to zero
	check_ptk, num = recv()
	if num == 3:
		ptk = 0
		send(str(ptk), 4)


	msg = encrypt(ptk, "hello")
	#send data to AP
	send(str(msg) , 5)
	break


print("Client done.")
server_socket.close()


