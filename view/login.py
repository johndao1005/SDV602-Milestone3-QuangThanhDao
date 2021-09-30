import tkinter as tk 
from tkinter import ttk
import view.setup as setup
from controller.login.auth import authentication
from controller.login.register import makeUser

class Login(tk.Tk):
    """Start an instance of login screen which allow user to sign up with top level window or login directly
        When users login, the class would open to menu which is another class which handle the data view, update, delete while
        destroy the current login to prevent multiple login.
        """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(setup.app_name)
        self.iconbitmap(setup.icon)
        options = setup.pad10
        option2 = setup.pad5
        self.resizable(0,0)
        label = ttk.Label(self, text="Login").grid(
            column=0, row=0, sticky="N", **options, columnspan=3)
        self.geometry("280x250+500+300")
        self.check = False
        # ANCHOR data input
        lf = ttk.Frame(
            self,
        ).grid(column=0, row=0, padx=10, pady=0)
        password = tk.StringVar()
        username = tk.StringVar()
        label = ttk.Label(lf, text="Username").grid(
            column=0, row=1, **options, ipadx=5, ipady=5)
        username_entry = ttk.Entry(lf, textvariable=username)
        username_entry.grid(
            column=1, row=1, **options, columnspan=2)
        label = ttk.Label(lf, text="Password").grid(
            column=0, row=2, **options, ipadx=5, ipady=5)
        password_entry = ttk.Entry(
            lf, textvariable=password, show="*")
        password_entry.grid(column=1, row=2, **options, columnspan=2)
        # ANCHOR Buttons for main window
        button_frame = ttk.Frame(
            self,
        ).grid(column=1, row=1, padx=10, pady=10)
        login_btn = ttk.Button(button_frame,
                               text="Login",
                               command=lambda: authentication(
                                    self, username, password)
                               ).grid(column=1, row=3, **option2)
        signup_btn = ttk.Button(button_frame,
                                text="Sign Up",
                                command=lambda: self.callSignup()
                                ).grid(column=2, row=3, **option2)
        quit_btn = ttk.Button(self,
                              text="Quit",
                              command=lambda: self.destroy()
                              ).grid(column=2, row=4, **options)

    def callSignup(self):
        """The function check for any instance of signup and only create a sign up window if there is none
        """
        if self.check == False:
            self.signupWindow()

    def signupWindow(self):
        self.check = True
        self.signup = tk.Toplevel()
        self.signup.title(setup.app_name)
        self.signup.iconbitmap(setup.icon)
        options = {'padx': 10, 'pady': 5}
        label = ttk.Label(self.signup, text="Sign up").grid(
            column=0, row=0, **options, columnspan=2)
        self.signup.geometry("310x360+100+100")
        self.signup.protocol("WM_DELETE_WINDOW", self.closeSignup)
        # Create placeholder to store data
        username = tk.StringVar()
        password = tk.StringVar()
        confirmPassword = tk.StringVar()
        email = tk.StringVar()

        lf = ttk.LabelFrame(self.signup, text="Login details")
        lf.grid(column=0, row=1, padx=20, pady=20)
        label = ttk.Label(lf, text="Username").grid(
            column=0, row=3, **options)
        username_entry = ttk.Entry(lf, textvariable=username).grid(
            column=1, row=3, **options)
        username_check = ttk.Label(lf, text="").grid(column=1, row=4)
        label = ttk.Label(lf, text="Pass word").grid(
            column=0, row=5, **options)
        password_entry = ttk.Entry(lf, textvariable=password).grid(
            column=1, row=5, **options)
        password_check = ttk.Label(lf, text="").grid(column=1, row=6)
        label = ttk.Label(lf, text="Confirm Password").grid(
            column=0, row=7, **options)
        confirmpassword_entry = ttk.Entry(
            lf, textvariable=confirmPassword).grid(column=1, row=7, **options)
        confirm_password_check = ttk.Label(
            lf, text="").grid(column=1, row=8)
        label = ttk.Label(lf, text="Email").grid(
            column=0, row=9, **options)
        email_entry = ttk.Entry(lf, textvariable=email).grid(
            column=1, row=9, **options)
        email_check = ttk.Label(lf, text="").grid(column=1, row=10)
        button = ttk.Button(lf,
                            text="Sign Up",
                            command=lambda: makeUser(
                                username, password, confirmPassword, email)
                            ).grid(column=0, row=11, **options, columnspan=2)
        button = ttk.Button(self.signup,
                            text="Cancel",
                            command=lambda: self.closeSignup()
                            ).grid(column=0, row=3, **options, sticky="SE")

    def closeSignup(self):
        """This function make sure that the window is closed and allow to create new instance of Sign up window
        """
        self.check = False
        self.signup.destroy()
