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
    s,num = struct.unpack("!50si",data)
    s = s.decode("utf-8").replace("\0","")
    print("Receive:%s,num:%d" % (s,num))
    return s,num

def make_ptk(ANonce, SNonce):
    return ANonce + SNonce


num = 1
while True:
    ANonce, num = recv()
    SNonce = '1'
    send(SNonce, num + 1)
    ptk = make_ptk(int(ANonce), int(SNonce))
    check_ptk, num = recv()
    if ptk == int(check_ptk):
        use_ptk = ptk
    a = str(ptk)
    send(a , num + 1)

    break
    # if str == "d":
    #     break
    # str = chr(ord(str)+1)
    # num = num + 1

print("Client done.")
server_socket.close()


