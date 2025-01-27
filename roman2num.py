import tkinter as tk
from tkinter import messagebox
import socket
import json
import threading
from chat_utils import *
import client_state_machine as csm

class Client:
    def __init__(self, args):
        # Initialize client attributes
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args

        # Initialize GUI elements
        self.root = tk.Tk()
        self.root.title("Chat Application")

        self.message_box = tk.Text(self.root)
        self.message_box.pack()

        self.input_field = tk.Entry(self.root)
        self.input_field.pack()

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        # Initialize chat client
        self.init_chat()

    def init_chat(self):
        # Initialize socket and chat state machine
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = SERVER if self.args.d is None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

    def send_message(self):
        # Send message from GUI input field
        message = self.input_field.get()
        self.send(message)
        self.input_field.delete(0, tk.END)

    def send(self, msg):
        # Send message over socket
        mysend(self.socket, msg)

    def recv(self):
        # Receive message from socket
        return myrecv(self.socket)

    def get_msgs(self):
        # Get messages from console input and socket
        read, _, _ = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def output(self):
        # Display messages in message box
        if len(self.system_msg) > 0:
            self.message_box.insert(tk.END, self.system_msg + "\n")
            self.system_msg = ''

    def login(self, username, password):
        # Perform login action
        msg = json.dumps({"action": "login", "name": username, "password": password})
        self.send(msg)
        response = json.loads(self.recv())
        if response["status"] == "ok":
            self.state = S_LOGGEDIN
            self.sm.set_state(S_LOGGEDIN)
            self.sm.set_myname(username)
            self.print_instructions()
            return True
        elif response["status"] == "duplicate":
            self.system_msg += 'Duplicate username, try again'
            return False
        else:
            self.system_msg += 'Login failed, try again'
            return False

    def read_input(self):
        # Continuously read input from GUI
        while True:
            text = self.input_field.get()
            self.console_input.append(text)
            self.input_field.delete(0, tk.END)

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        # Main chat loop
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while True:
            my_msg, peer_msg = self.get_msgs()
            self.system_msg += self.sm.proc(my_msg, peer_msg)
            self.output()

if __name__ == "__main__":
    client = Client()
    client.root.mainloop()  # Ensure the GUI mainloop is invoked after initializing all elements
    client.run_chat()  # Call the chat client's main loop
