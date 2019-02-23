from socket import *
import os,sys

def send_msg(s,name,addr):
    while True:
        text = input("发言: ")
        if text == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(), addr)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name,text)
        s.sendto(msg.encode(),addr)


def recv_msg(s):
    while True:
        data,addr = s.recvfrom(1024)
        if data.decode() == 'Q':
            sys.exit(0)
        print("\r%s"%data.decode()+'\n发言: ',end='')

def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    host = sys.argv[1]
    port = int(sys.argv[2])
    ADDR = (host,port)

    s = socket(AF_INET,SOCK_DGRAM)

    while True:
        name = input("请输入姓名: ")
        msg = 'L '+name
        s.sendto(msg.encode(),ADDR)
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    pid = os.fork()
    if pid < 0 :
        print("子进程创建失败")
    elif pid == 0:
        recv_msg(s)
    else:
        send_msg(s, name, ADDR)



if __name__ == '__main__':
    main()

