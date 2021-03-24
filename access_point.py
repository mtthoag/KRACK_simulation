import socket
import sys
import struct
import random 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 19990))


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

def decrypt(ptk, e_msg):
	#msg in asci

	
	#xor packet key and msg
	decrypted_msg = ptk ^ int(e_msg)
	sd_msg = str(decrypted_msg)

	msg = ''.join(chr(int(sd_msg[i:i+3])) for i in range(0,len(sd_msg), 3))

	print(msg)
	return msg
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
	ptk = int(check_ptk)

	#recieve data
	msg, num = recv()
	decrypt(ptk, int(msg))
	break


print("Server Done.")
server_socket.close()
