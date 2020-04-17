import sys
import socket
import threading
import tkinter as tk

#TODO



def receive(s):
    while True:
        try:
            message = s.recv(1024)
        except:
            print("Unable to recieve")
            break
        if not message:
            break
        if message == ' ':
            pass
        elif message.decode()=='exit':
            log.configure(state=tk.NORMAL)
            log.insert(tk.END, 'Your Buddy has disconnected')
            log.configure(state=tk.DISABLED)
            try:
                s.sendall(message)
            except:
                break
            finally:
                break
        else:
            log.configure(state=tk.NORMAL)
            log.insert(tk.END, '\nBuddy: ')
            log.insert(tk.END, message.decode())
            log.yview_pickplace("end")
            log.configure(state=tk.DISABLED)


#methods for GUI

def clear_log(event):
    log.configure(state=tk.NORMAL)
    log.delete(1.0, tk.END)
    log.insert(tk.END, "--Log--") 
    log.tag_configure("center", justify='center')
    log.tag_add("center", 1.0)
    log.configure(cursor="sailboat")
    log.configure(state=tk.DISABLED)


def send_message(event):

    mess = text_box.get("1.0", tk.END)
    s.sendall(mess.encode())
    text_box.delete(1.0, tk.END)
    log.configure(state=tk.NORMAL)
    log.insert(tk.END, '\nMe: ')
    log.insert(tk.END, mess) 
    log.yview_pickplace("end")
    log.configure(state=tk.DISABLED)




if __name__ == '__main__':
    
    if len(sys.argv) ==3:
        ip_val = sys.argv[1]
        port_val = sys.argv[2]

    
    if len(sys.argv) == 2:
        ip_val='127.0.0.1'
        port_val = sys.argv[1]
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((ip_val, int(port_val)))
    thread1 = threading.Thread(target = receive, args = ([s]))

    #GUI-----------------------------------------------------

    window = tk.Tk()
    window_title = 'Client CHATTER WINDOW'
    window.title(window_title)
    
    
    window.rowconfigure(3, minsize=300, weight=1)
    window.columnconfigure(3, minsize=100, weight=1)

    buttons_frame = tk.Frame(master=window, width=100, height=500, bg='lightcoral')
    type_frame = tk.Frame(master=window, width=100, height=100, bg='yellow')


    clear_button = tk.Button(buttons_frame,
        text="Clear",
        width=20,
        height=2,
        bg="mediumslateblue",
        fg="yellow")
    clear_button.bind("<Button-1>", clear_log)

    ip_label = tk.Label(buttons_frame, text="IP", anchor="w", bg='lightcoral')
    port_label = tk.Label(buttons_frame, text='PORT', anchor="w", bg='lightcoral')
    
    ip_label['text']=ip_val
    port_label['text']=port_val

    #grid button frame
    buttons_frame.rowconfigure(5, minsize=100, weight=1)
    buttons_frame.columnconfigure(0, minsize=100, weight=1)
    clear_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    ip_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    port_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)


    log = tk.Text(master=window, 
        width=75,
        height=10,
        wrap='word',
        fg="white",  
        bg="mediumslateblue")

   
    log.insert(tk.END, "--Log--") 
    log.tag_configure("center", justify='center')
    log.tag_add("center", 1.0)
    log.configure(cursor="sailboat")
    log.configure(state=tk.DISABLED)
    
    

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

#-------------------------------------------------------------------------------


    thread1.start()


    window.mainloop()
    try:
        s.sendall("exit".encode())
    except:
        pass
    s.close()
    thread1.join()
   
        