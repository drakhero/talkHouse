from socket import *
import os,sys

def do_login(s,talkers,name,addr):
    if (name in talkers) or name == '管理员':
        s.sendto('用户已存在'.encode(),addr)
        return
    s.sendto('OK'.encode(),addr)

    for i in talkers:
        msg = '欢迎%s进入聊天室' % name
        s.sendto(msg.encode(),talkers[i])

    talkers[name] = addr


def do_chat(s,talkers,name,text):
    msg = "%s: %s" % (name, text)
    if name != '管理员':
        print("\r%s"%msg + "\n管理员发言: ",end='')
    for talker in talkers:
        if talker != name:
            s.sendto(msg.encode(),talkers[talker])


def do_quit(s,talkers,addr,name):
    s.sendto('Q'.encode(), addr)
    del talkers[name]
    for talker in talkers:
        msg = '%s已退出聊天' % name
        s.sendto(msg.encode(),talkers[talker])

def do_child(s,addr):
    while True:
        text = input("管理员发言: ")
        msg = 'C 管理员 ' + text
        s.sendto(msg.encode(),addr)

def do_parent(s):
    talkers = {}
    while True:
        data,addr = s.recvfrom(1024)
        data_list = data.decode().split()
        if data_list[0] == 'L':
            do_login(s,talkers,data_list[1],addr)
        elif data_list[0] == 'C':
            do_chat(s,talkers,data_list[1],' '.join(data_list[2::]))
        elif data_list[0] == 'Q':
            do_quit(s,talkers,addr,data_list[1])



def main():
    s = socket(AF_INET,SOCK_DGRAM)
    ADDR = ('127.0.0.1',9999)
    s.bind(ADDR)

    pid = os.fork()
    if pid<0:
        sys.exit("创建子进程失败")
    elif pid == 0:
        do_child(s,ADDR)
    else:
        do_parent(s)


    s.close()

if __name__ == '__main__':
    main()