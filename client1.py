import sys
import socket
import threading


def receive(s):
    while True:
        r_msg = s.recv(1024)
        if not r_msg:
            break
        if r_msg == ' ':
            pass
        elif r_msg.decode()=='exit':
            print('You been have disconnected from Server. You many need to end the program by typing \'exit\'')
            try:
                s.sendall(r_msg)
            except:
                pass
            finally:
                break
        else:
            print(r_msg.decode())

def sendMsg(s):
    while True:
        s_msg = input().replace('b', '').encode('utf-8')
        if s_msg == '':
            pass
        if s_msg.decode() == 'exit':
            try:
                s.sendall(s_msg)
            except:
                pass
            break
        else:
            try:
                s.sendall(s_msg)
            except:
                if s_msg.decode()=='i dont wanna':
                    print('Well, you have to')
                else:
                    print('Please exit the program by typing \'exit\'')


if __name__ == '__main__':
    '''
    if len(sys.argv) is not 3:
        print("usage: %s [ip adress][port] " % sys.argv[0] )
        sys.exit(0)
    '''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.connect((sys.argv[1], int(sys.argv[2])))
    s.connect(('127.0.0.1', 11111))
    thread1 = threading.Thread(target = receive, args = ([s]))
    thread2 = threading.Thread(target = sendMsg, args = ([s]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()