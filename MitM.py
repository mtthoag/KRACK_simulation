import socket
import sys
import struct
import random 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 19992))


def send_client(p, num):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(p,("127.0.0.1",19991))
    s.close()
    print("Send: %d to client" % (num))

def send_ap(p, num):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(p,("127.0.0.1",19990))
    s.close()
    print("Send:%d to AP" % (num))


def recv():
    global server_socket
    data, addr = server_socket.recvfrom(1024)
    s,num = struct.unpack("!50si",data)
 
    print("Receive num:%d" % (num))
    return data,num

def make_ptk(ANonce, SNonce):
    return ANonce + SNonce

def decrypt(ptk, msg):
	#msg in asci

	
	#xor packet key and msg
	decrypted_msg = ptk ^ int(msg)
	sd_msg = str(decrypted_msg)

	msg = ''.join(chr(int(sd_msg[i:i+3])) for i in range(0,len(sd_msg), 3))
	if msg == 'hello':
		print("haha we decrypted the msg ", msg)
	else:
		print('You have defeated KRACK')
	return decrypted_msg


blocked_four = 0
while True:

	p, num = recv()	
	#intercept msg1 and msg3 from the AP and send it to the client
	if num == 1:
		send_client(p, num)

	#intercept msg2 from client and send it to AP. if msg4 was already blocked send msg4 to AP
	elif num == 2:
		send_ap(p, num)
	elif num == 3:
		msg3 = p
		send_client(p, num)
	#intercept msg4 and resend 3 to the client
	elif num == 4:
		if blocked_four:
			send_ap(p, num)
		else:
			send_client(msg3, 3)
			blocked_four = 1


	#send the encrypted data from the client to the AP
	elif num == 5:
		print(1111)
		send_ap(p, num)
		print(33333)
		s,num = struct.unpack("!50si",p)
		s = s.decode("utf-8").replace("\0","")
		decrypt(0, s)
		break



print("MitM Done.")
server_socket.close()
