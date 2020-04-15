import sys
import socket
import threading
import tkinter as tk


def receive(conn):
    while True:
        received = conn.recv(1024)
        if received =='':
            break
        elif received.decode() =='exit':
            print('You have been disconnected from Client. You many need to end the program by typing \'exit\'')
            try:
                conn.sendall(received)
            except:
                pass
            finally:
                break
        else:
            print(received.decode())

def sendMsg(conn):
    while True:
        message = input().encode()
        if message == '':
            pass
        if message.decode() == 'exit':
            try:
                conn.sendall(message)
            except:
                pass
            break
        else:
            try:
                conn.sendall(message)
            except:
                if message.decode()=='i dont wanna':
                    print('Well, you have to')
                else:
                    print('Please exit the program by typing \'exit\'')



#methods for GUI
def send_message(event):

    mess = text_box.get("1.0", tk.END)
    print(mess)
    conn.sendall(mess.encode())
    text_box.delete(1.0, tk.END)
    log.configure(state=tk.NORMAL)
    log.insert(tk.END, '\n')
    log.insert(tk.END, '\nMe: ')
    log.insert(tk.END, mess) 
    log.configure(state=tk.DISABLED)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 11111))
    s.listen()
    (conn, addr) = s.accept() 
    print("running on: ", addr)
    thread1 = threading.Thread(target = receive, args = ([conn]))
    thread2 = threading.Thread(target = sendMsg, args = ([conn]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
