from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector as mycon
mydb = mycon.connect(host="localhost", user="root", password="", database="apollodb")
mycur = mydb.cursor()

auth = [] # To save users credentials such as user ID

# Value returning/middleman functions           
def userExists(email, password, loginType):
	if(loginType == 'buyer'):
		sql = ("SELECT * FROM users WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res != []):
			return True
		else:
			return False
	elif(loginType == 'seller'):
		sql = ("SELECT * FROM sellers WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res != []):
			return True
		else:
			return False

class Main:
    def getAuth(email, password, authType):
        if(authType == 'buyer'):
            try:
                mycur.execute("SELECT userId from users WHERE email=%s AND password=%s", (email, password))

                res = mycur.fetchall()
                print(res)
            except Exception as e:
                messagebox.showerror("Error", "Error!")

    def __init__(self, root):
        self.root = root
        self.root.title("Appolo Marketplace")
        self.root.geometry("1138x640")
        self.root.config(bg="black")

        self.bg = ImageTk.PhotoImage(file="images/main_bg.jpg")
        bg = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        frame1=Frame(self.root, bg="light gray")
        frame1.place(x=0, y=0, width=1138, height=70)

        title = Label(frame1, text="Appolo Marketplace", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)

        email = Label(frame1, text="Email", font=("calibri", 14), bg="light gray").place(x=600, y=18)
        txt_email = Entry(frame1, font=("calibri", 12), bg="gray").place(x=650, y=18, width=150)

        password = Label(frame1, text="Password", font=("calibri", 14), bg="light gray").place(x=820, y=18)
        txt_pass = Entry(frame1, font=("calibri", 12), bg="gray").place(x=906, y=18, width=150)

        login_btn = Button(frame1, text="Login").place(x=1070, y=18, width=60)

        frame2=Frame(self.root, bg="light gray")
        frame2.place(x=680, y=100, width=400, height=330)

        title = Label(frame2, text="Register", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)
        
        fname = Label(frame2, text="First Name", font=("calibri", 14), bg="light gray").place(x=10, y=80)
        self.txt_fname = Entry(frame2, font=("calibri", 12), bg="gray")
        self.txt_fname.place(x=110, y=80, width=150)

        lname = Label(frame2, text="Last Name", font=("calibri", 14), bg="light gray").place(x=10, y=120)
        self.txt_lname = Entry(frame2, font=("calibri", 12), bg="gray")
        self.txt_lname.place(x=110, y=120, width=150)

        email = Label(frame2, text="Email", font=("calibri", 14), bg="light gray").place(x=10, y=160)
        self.txt_email = Entry(frame2, font=("calibri", 12), bg="gray")
        self.txt_email.place(x=110, y=160, width=150)

        password = Label(frame2, text="Password", font=("calibri", 14), bg="light gray").place(x=10, y=200)
        self.txt_pass = Entry(frame2, font=("calibri", 12), bg="gray")
        self.txt_pass.place(x=110, y=200, width=150)

        self.var_chk = IntVar()
        self.check = Checkbutton(frame2, text="I agree to the Terms & Conditions", variable=self.var_chk, onvalue=1, offvalue=0, font=("calibri", 14), bg="light gray")
        self.check.place(x=10, y=240)

        signup_btn = Button(frame2, text="Create Account", command=self.register_data).place(x=10, y=280, width=120)

    def register_data(self):
        if self.txt_fname.get()=="" or self.txt_lname.get()=="" or self.txt_email.get()=="" or self.txt_pass.get()=="":
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
        elif self.var_chk.get()==0:
            messagebox.showerror("Error", "You have not agreed to the terms and conditions.", parent=self.root)
        else:
            name = self.txt_fname.get() + " " + self.txt_lname.get()
            email = self.txt_email.get()
            password = self.txt_pass.get()

            question = messagebox.askquestion("Signup Type", "Signup as Buyer(Yes) or Signup as Buyer(No)")
            if(question=="yes"): 
                #Buyer
                try:
                    mycur.execute("INSERT into users(name, email, password) values(%s, %s, %s)", (name, email, password))
                    mydb.commit()

                    signupType = "buyer"
                    getAuth(email, password, signupType)
                except Exception as es:
                    messagebox.showerror("Error", "Error!")
            elif(question=="no"):
                #Seller
                try:
                    mycur.execute("INSERT into sellers(name, email, password) values(%s, %s, %s)", (name, email, password))
                    mydb.commit()

                    signupType = "seller"
                    getAuth(email, password, signupType)
                except Exception as es:
                    messagebox.showerror("Error", "Error!")

root = Tk()
obj = Main(root)
root.mainloop()
