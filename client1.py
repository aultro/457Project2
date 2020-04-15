import sys
import socket
import threading
import tkinter as tk



#methods for chat

def receive(s):
    while True:
        r_msg = s.recv(1024)
        if not r_msg:
            break
        if r_msg == ' ':
            pass
        elif r_msg.decode()=='exit':
            print('You been have disconnected from Server. You may need to end the program by typing \'exit\'')
            try:
                s.sendall(r_msg)
            except:
                pass
            finally:
                break
        else:
            greeting['text']=r_msg

'''
def sendMsg(s):
    #while True:
    s_msg = text_box.get("1.0", tk.END)
    if s_msg == '':
        pass
    if s_msg == 'exit':
        try:
            s.sendall(s_msg)
        except:
            pass
        
    else:
        try:
            s.sendall(s_msg)
        except:
            if s_msg=='i dont wanna':
                print('Well, you have to')
            else:
                print('Please exit the program by typing \'exit\'')
'''

#methods for GUI
def send_message(event):

    mess = text_box.get("1.0", tk.END)
    s.sendall(mess.encode())
    text_box.delete(1.0, tk.END)







if __name__ == '__main__':
    
    #if len(sys.argv) is not 3:
    #    print("usage: %s [ip adress][port] " % sys.argv[0] )
    #    sys.exit(0)
    

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.connect((sys.argv[1], int(sys.argv[2])))
    s.connect(('127.0.0.1', 11111))
    thread1 = threading.Thread(target = receive, args = ([s]))
    #thread2 = threading.Thread(target = sendMsg, args = ([s]))
    thread1.start()
    #thread2.start()

    
    window = tk.Tk()
    window.title('CHATTER')
    buttons_frame = tk.Frame(master=window, width=400, height=100, bg='lightcoral')
    
    window.rowconfigure(0, minsize=800, weight=1)
    window.columnconfigure(1, minsize=800, weight=1)

    text_box = tk.Text(master=window)

    greeting = tk.Label(master=buttons_frame, 
        text="Hello world", 
        width=75,
        height=10,
        wraplength=60,
        justify='left',
        fg="white",  
        bg="mediumslateblue")

    button = tk.Button(buttons_frame,
        text="Click me!",
        width=20,
        height=2,
        bg="blue",
        fg="yellow",)
    button.bind("<Button-1>", send_message)



    greeting.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    text_box.grid(row=0, column=1, sticky="nsew")
    buttons_frame.grid(row=0, column=0, sticky="ns")

    window.mainloop()

    thread1.join()
    #thread2.join()
        