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
    print("Send:%s, msg%d\n" % (c,num))


def recv():
    global server_socket
    data, addr = server_socket.recvfrom(1024)
    s,num = struct.unpack("!50si",data)
    s = s.decode("utf-8").replace("\0","")
    print("Receive:%s, msg%d\n" % (s,num))
    return s,num

def make_ptk(ANonce, SNonce):
    return ANonce + SNonce

def decrypt(ptk, e_msg):
	#msg in asci

	
	#xor packet key and msg
	decrypted_msg = ptk ^ int(e_msg)
	sd_msg = hex(decrypted_msg)[2:]

	msg = bytes.fromhex(sd_msg).decode('utf-8')
	print("Decrypted msg ", msg, '\n')
	return msg


num = 1
while True:
	ANonce = str(random.randint(100000000000,500000000000))
	
	#msg #1
	print('Sending the ANonce to supplicant ')
	send(ANonce, num)
	
	#msg #2

	print('Received SNonce from supplicant')
	SNonce, num = recv()
	
	ptk = make_ptk(int(ANonce), int(SNonce))
	a = str(ptk)

	#msg #3
	print("Sending ptk to supplicant ")
	send(a, num+1)
	
	#msg #4
	print("Receiving ptk from supplicant")
	check_ptk, num = recv()
	ptk = int(check_ptk)

	#recieve data
	print("Receiving data from supplicant")
	msg, num = recv()
	decrypt(ptk, int(msg))
	break


print("Server Done.")
server_socket.close()
