from customtkinter import *
from PIL import Image
from tkinter import messagebox
import database

class LoginWindow():
    def __init__(self, master=None)-> None:
        self.master = CTkToplevel()
        self.master.geometry('530x400')
        self.master.resizable(0, 0)
        self.master.title('Login Page')

        # Background image
        loginCover = CTkImage(Image.open('./loginCover.png'), size=(930, 478))
        loginCoverLabel = CTkLabel(self.master, image=loginCover, text='')
        loginCoverLabel.place(x=0, y=0)

        # Heading label
        headingLabel = CTkLabel(self.master, text='Teacher Login Panel', bg_color='#ffffff', font=('Cascadia Code', 20, 'bold'), text_color='dark blue')
        headingLabel.place(x=20, y=100)

        # Username entry
        self.usernameEntry = CTkEntry(self.master, placeholder_text='Enter your username', width=180)
        self.usernameEntry.place(x=50, y=150)

        # Password entry
        self.passwordEntry = CTkEntry(self.master, placeholder_text='Enter your password', width=180, show='*')
        self.passwordEntry.place(x=50, y=200)

        # Login button
        loginBTN = CTkButton(self.master, text='Login', cursor='hand2', fg_color='#605678', hover_color='#3A6D8C', text_color='#ffffff', corner_radius=20, command=self.login)
        loginBTN.place(x=50, y=250)

        # Result flag to track login status
        self.result = False

    def login(self):
        # Validate input
        if self.usernameEntry.get() == '' or self.passwordEntry.get() == '':
            messagebox.showerror('Error', 'All Fields are required')
        else:
            user = self.usernameEntry.get()
            password = self.passwordEntry.get()

            # Fetch teacher info from database
            teacher_info = database.teacher_login_database(user)

            # Check if teacher info exists
            if teacher_info:
                try:
                    ((name, pawd),) = teacher_info  # Unpack the tuple
                    if password == pawd:
                        self.result = True
                        messagebox.showinfo('Success', f'Hello, {name}! Welcome!')
                        self.master.destroy()  # Close the login window after successful login
                    else:
                        messagebox.showerror('Error', 'Incorrect password, please try again!')
                except ValueError:
                    messagebox.showerror('Error', 'Error unpacking teacher data. Please try again later.')
            else:
                messagebox.showerror('Error', 'Incorrect credentials, please try again.')

    def get_result(self):
        return self.result
