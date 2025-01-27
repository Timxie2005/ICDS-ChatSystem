#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from pygame import mixer
import json
import re
import subprocess
# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        #Login_window
        self.login = tk.Tk()
        self.login.title("Chatify")
        self.login.configure(bg="white") #Color
        frame = tk.Frame(self.login, bg="white") 
        frame.pack(padx=50, pady=100) #Size

        #Fonts
        font_style = ("Arial", 14, "bold")  
        username_font_style = ("Arial", 18)  
        password_font_style = ("Arial", 18)  

        #Entries
        self.usernameEntry = ctk.CTkEntry(frame, 
            placeholder_text="Username",
            font=username_font_style,
            width=280,
            height=50,
            border_color= "#666666",
            corner_radius=5,
            state="normal",
        )
        self.usernameEntry.grid(row=0, column=1, sticky="w", pady=(0, 20)) #Username_entry

        self.passwordEntry = ctk.CTkEntry(frame, 
                    placeholder_text="Password",
                    font=password_font_style,
                    show="*",
                    width=280,
                    height=50,
                    border_color= "#666666",
                    corner_radius=5,
                    state="normal",
                )
        self.passwordEntry.grid(row=1, column=1, sticky="w",pady=(0, 20)) #Password_entry
        

        #Buttons
        self.register_button = ctk.CTkButton(
            master= frame,
            command= self.register_user,
            text= "Regsiter",
            font= font_style,
            text_color="black",
            hover= True,
            hover_color= "#F3F3F3",
            height=50,
            width= 120,
            border_width=2,
            corner_radius=20,
            border_color= "#616161", 
            bg_color="#ffffff",
            fg_color= "#ffffff")
        self.register_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="we") #Register_button

        self.login_button = ctk.CTkButton(
            master= frame,
            command= self.login_user,
            text= "Login",
            font= font_style,
            text_color="white",
            hover= True,
            hover_color= "#004182",
            height=50,
            width= 120,
            border_width=2,
            corner_radius=20,
            border_color= "#2d6f9e", 
            bg_color="#ffffff",
            fg_color= "#0a66c2")
        self.login_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="we") #Login_button

        self.forgot_button = ctk.CTkButton(
            master= frame,
            command= self.forgot_password_window,
            text= "Forgot password",
            font= ("Arial", 10),
            text_color="black",
            hover= True,
            hover_color= "#ffffff",
            height=20,
            width= 120,
            border_width=2,
            corner_radius=20,
            border_color= "#ffffff", 
            bg_color="#ffffff",
            fg_color= "#ffffff")
        self.forgot_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="we") #Forgot_button

        #Run window
        self.Window.mainloop()
    


    
    def forgot_password_window(self):
        #Reset_password_window
        self.forgot_password_window = tk.Toplevel()
        self.forgot_password_window.title("Forgot Password")
        self.forgot_password_window.configure(bg="white")
        frame = tk.Frame(self.forgot_password_window, bg="white")
        frame.pack(padx=50, pady=50)

        #Fonts
        font_style = ("Arial", 14, "bold")
        entry_font_style = ("Arial", 18)

        #Entries
        self.adminPasswordEntry = ctk.CTkEntry(frame,
                                                placeholder_text="Admin Password",
                                                font=entry_font_style,
                                                show="*",
                                                width=280,
                                                height=50,
                                                border_color="#666666",
                                                corner_radius=5,
                                                state="normal")
        self.adminPasswordEntry.grid(row=0, column=1, sticky="w", pady=(0, 20))

        self.usernameEntry = ctk.CTkEntry(frame,
                                           placeholder_text="Username",
                                           font=entry_font_style,
                                           width=280,
                                           height=50,
                                           border_color="#666666",
                                           corner_radius=5,
                                           state="normal")
        self.usernameEntry.grid(row=1, column=1, sticky="w", pady=(0, 20))

        self.newPasswordEntry = ctk.CTkEntry(frame,
                                              placeholder_text="New Password",
                                              font=entry_font_style,
                                              width=280,
                                              height=50,
                                              border_color="#666666",
                                              corner_radius=5,
                                              state="normal")
        self.newPasswordEntry.grid(row=2, column=1, sticky="w", pady=(0, 20))

        #Buttons
        submit_button = ctk.CTkButton(master=frame,
                                      command=self.reset_password,
                                      text="Submit",
                                      font=font_style,
                                      text_color="white",
                                      hover=True,
                                      hover_color="#004182",
                                      height=50,
                                      width=120,
                                      border_width=2,
                                      corner_radius=20,
                                      border_color="#2d6f9e",
                                      bg_color="#ffffff",
                                      fg_color="#0a66c2")
        submit_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")

    
    
    def load_users():
        global users
        users = []
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    users.append(eval(line.strip()))
        except FileNotFoundError:
            pass
    users = []
    load_users()


    def reset_password(self):
        admin_password = self.adminPasswordEntry.get()
        username = self.usernameEntry.get()
        new_password = self.newPasswordEntry.get()

        #Check if admin password is correct
        if admin_password != "admin":
            messagebox.showerror("Error", "Incorrect admin password")
            return

        #Load user data
        users = []
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    users.append(eval(line.strip()))
        except FileNotFoundError:
            pass
       

        #Find the user and update password
        user_found = False
        for user in users:
            if user['username'] == username:
                user_found = True
                user['password'] = new_password
                break

        if not user_found:
            messagebox.showerror("Error", "Username not found")
            return

        #Write updated data back to file
        with open("users.txt", "w") as file:
            for user in users:
                file.write(str(user) + "\n")

        messagebox.showinfo("Success", "Password reset successful")
        self.forgot_password_window.destroy()
        
        self.goAhead(username)

    def register_user(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        if username == "" or password == "":
            messagebox.showerror("Error", "Please enter a username and password!")
            return
        
        for user in users:
            if user['username'] == username:
                messagebox.showerror("Error", "Username already exists!")
                return

        users.append({'username': username, 'password': password})
        messagebox.showinfo("Success", "Registration successful!")
        with open("users.txt", "w") as file:
            for user in users:
                file.write(str(user) + "\n")


    def login_user(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        for user in users:
            if user['username'] == username and user['password'] == password:
                
                self.goAhead(self.usernameEntry.get())  # Call goAhead method with the username
                return
        messagebox.showerror("Error", "Invalid username or password!")


    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()



    # The main layout of the chat

    def layout(self, name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.geometry("510x510")  # Background color changed to white
        
        self.label_title = ctk.CTkLabel(self.Window, text=name, font=("Helvetica", 16, "bold"))
        self.label_title.place(relwidth=0.73, relx=0.01, rely=0.005)

        self.label_title = ctk.CTkLabel(self.Window, text="Tools", font=("Helvetica", 16, "bold"))
        self.label_title.place(relwidth=0.23, relx=0.76, rely=0.005) 

        self.textCons = Text(self.Window,
                            width=20,
                            height=2,
                            bg="#ffffff",  # Background color changed to white
                            fg="#003254",  # Text color changed to blue
                            font="Helvetica 14",
                            padx=5,
                            pady=5)  # Adjusted height to 10
        self.textCons.place(relheight=0.850, relwidth=0.73, relx=0.01, rely=0.06)


        self.entryMsg = ctk.CTkEntry(self.Window)
        self.entryMsg.place(relwidth=0.47, relheight=0.06, rely=0.92, relx=0.01)
        self.entryMsg.focus()

        # send button
        self.buttonMsg = ctk.CTkButton(self.Window, text="Send", command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.49, rely=0.92, relheight=0.06, relwidth=0.12)

        self.buttonMsg = ctk.CTkButton(self.Window, text="Game", command=self.game)
        self.buttonMsg.place(relx=0.62, rely=0.92, relheight=0.06, relwidth=0.12)

        self.right_space = ctk.CTkFrame(self.Window)
        self.right_space.place(relx=0.76, rely=0.06, relheight=0.925, relwidth=0.23)  # Adjusted relwidth to 0.24

        online_users = self.get_online_users()

        self.combobox_users = ctk.CTkComboBox(self.right_space,
                                     values=online_users)
        self.combobox_users.place(rely=0.01, relx = 0.05, relwidth=0.9)
        
        self.buttonMsg = ctk.CTkButton(self.right_space, text="connect", command=self.connect_to_user)
        self.buttonMsg.place(rely=0.1, relx= 0.05, relwidth=0.9)

        switch_var = ctk.StringVar(value="OFF")
        self.switch = ctk.CTkSwitch(self.right_space, text="music", command=self.switcher, variable=switch_var, onvalue="ON", offvalue="OFF")
        self.switch.place(relx=0.5, rely=0.21, anchor="center")

        self.entryMsg.bind('<Return>', lambda event: self.sendButton(msg=self.entryMsg.get()))


    def game(self):
        process = subprocess.Popen(["python", "snake.py"], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Wait for the game to finish
        process.wait()

        #send the score to the user and the peer
        file = open('score_pipe', 'r')
        score = file.readline()
        file.close()
        self.sendButton("My score is: " + score)


    def get_online_users(self):
        # Fetch online users from the server
        mysend(self.socket, json.dumps({"action": "list"}))
        response = json.loads(myrecv(self.socket))["results"]
        names = re.findall(r"'([^']+)':", response)
        return names 

    def switcher(self):
        val = self.switch.get()    
          
        if val == "ON":
            mixer.init()
            mixer.music.load("your_music_file.mp3")
            mixer.music.play()
        else:
            mixer.music.pause()
            
    def connect_to_user(self):
        # Connect to selected user
        to_name = self.combobox_users.get()
        self.sendButton("c " + to_name)


    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
    

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)



    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()