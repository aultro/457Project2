import sys
import socket
import threading
import tkinter as tk

#TODO

#clear button
#

global yourname

#methods for chat

def receive(s):
    while True:
        message = s.recv(1024)
        if not message:
            break
        if message == ' ':
            pass
        elif message.decode()=='exit':
            log.insert(tk.END, 'Your Buddy has disconnected')
            try:
                s.sendall(message)
            except:
                pass
            finally:
                break
        else:
            log.configure(state=tk.NORMAL)
            log.insert(tk.END, '\nBuddy: ')
            log.insert(tk.END, message.decode())
            log.insert(tk.END, '\n') 
            log.yview_pickplace("end")
            log.configure(state=tk.DISABLED)

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
    print(mess)
    s.sendall(mess.encode())
    text_box.delete(1.0, tk.END)
    log.configure(state=tk.NORMAL)
    log.insert(tk.END, '\nMe: ')
    log.insert(tk.END, mess) 
    log.yview_pickplace("end")
    log.configure(state=tk.DISABLED)




if __name__ == '__main__':
    
    window_title = 'CHATTER WINDOW'
    yourname = ""
    if len(sys.argv) is 2:
        yourname = sys.argv[1]
        window_format = "\'s CHATTER WINDOW"
        window_title = yourname + window_format
    

    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.connect((sys.argv[1], int(sys.argv[2])))
    s.connect(('127.0.0.1', 11111))
    thread1 = threading.Thread(target = receive, args = ([s]))
    #thread2 = threading.Thread(target = sendMsg, args = ([s]))
    thread1.start()
    #thread2.start()

    
    window = tk.Tk()
    window.title(window_title)
    
    
    window.rowconfigure(3, minsize=300, weight=1)
    window.columnconfigure(3, minsize=100, weight=1)

    buttons_frame = tk.Frame(master=window, width=100, height=500, bg='lightcoral')
    type_frame = tk.Frame(master=window, width=100, height=100, bg='yellow')


    connect_button = tk.Button(buttons_frame,
        text="Connect",
        width=20,
        height=2,
        bg="mediumslateblue",
        fg="yellow")
    #connect_button.bind("<Button-1>", send_message)

    ip_label = tk.Label(buttons_frame, text="IP", anchor="w", bg='lightcoral')
    port_label = tk.Label(buttons_frame, text='PORT', anchor="w", bg='lightcoral')
    ip_entry = tk.Entry(buttons_frame)
    port_entry = tk.Entry(buttons_frame)

    #grid button frame
    buttons_frame.rowconfigure(5, minsize=100, weight=1)
    buttons_frame.columnconfigure(0, minsize=100, weight=1)
    connect_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    ip_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    ip_entry.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    port_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    port_entry.grid(row=4, column=0, sticky="ew", padx=5, pady=5)


    log = tk.Text(master=window, 
        width=75,
        height=10,
        wrap='word',
        fg="white",  
        bg="mediumslateblue")

   
    log.insert(tk.END, "--Log--") 
    log.tag_configure("center", justify='center')
    log.tag_add("center", 1.0)
    
    

    text_box = tk.Text(master=type_frame,
        width=60,
        height=4,)

    send_button = tk.Button(type_frame,
        text="SEND",
        width=20,
        height=2,
        bg="mediumslateblue",
        fg="yellow",)
    send_button.bind("<Button-1>", send_message)

    #grid type_frame
    type_frame.rowconfigure(1, minsize=50, weight=1)
    type_frame.columnconfigure(2, minsize=50, weight=1)
    text_box.grid(row=0, column=0, sticky="nsew", columnspan=4, padx=5, pady=5)
    send_button.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    #grid window
    log.grid(row=0, column=1, sticky = "nsew", padx=5, pady=5, rowspan=4, columnspan=3)
    buttons_frame.grid(row=0, column=0, sticky="nsew", rowspan=4)
    type_frame.grid(row=4, column=0, sticky="nsew", columnspan=4)

    window.mainloop()

    thread1.join()
    #thread2.join()
        