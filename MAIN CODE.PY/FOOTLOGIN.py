from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3



def connec():
    conn = sqlite3.connect('AppData.db')
    cur = conn.cursor()

    cur.executescript('''
    CREATE TABLE IF NOT EXISTS team_bar (
        TEAM_ID INT PRIMARY KEY,
        TEAM_NAME CHAR(20)
    );

    UPDATE  team_bar SET  TEAM_NAME = 'PRS' WHERE  TEAM_ID=3;
    UPDATE  team_bar SET  TEAM_NAME = 'REAL MADRID' WHERE  TEAM_ID=2;
    UPDATE  team_bar SET  TEAM_NAME = 'BARCELONA' WHERE  TEAM_ID=1;

    CREATE TABLE IF NOT EXISTS players (
        player_id INT PRIMARY KEY,
        team_id INT,
        fname CHAR(20),
        lname CHAR(20),
        position CHAR(20),
        jerseyno INT,
        FOREIGN KEY (team_id) REFERENCES team_bar(TEAM_ID)
    );

    INSERT OR IGNORE INTO players (player_id, team_id, fname, lname, position, jerseyno)
    VALUES (17, 3, 'Zlatan', 'Ibrahimović', 'CENTER FORWARD', 17);

    CREATE TABLE IF NOT EXISTS team_rank (
        TEAM_ID INT PRIMARY KEY,
        win INT, 
        draw INT,
        lose INT,
        points INT
    );

    CREATE TABLE IF NOT EXISTS Register (
        fname VARCHAR(255),
        lname VARCHAR(255),
        pswd VARCHAR(255),
        Confirms_pswd VARCHAR(255),
        email VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS matches (
        match_id INT PRIMARY KEY,
        date_ CHAR(20), 
        venue CHAR(20),
        result CHAR(20),
        hometeam_id INT,
        awayteam_id INT
    );
    ''')
   
    conn.commit()
    conn.close()


def fetch_data():
    conn = sqlite3.connect('AppData.db')
    cur = conn.cursor()

    tables = ['team_bar', 'players', 'team_rank', 'Register', 'matches']
    for table in tables:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        print(f"Data from {table}:")
        for row in rows:
            print(row)
        print()

    conn.close()
    
    

# Call the functions to create tables, insert data, and fetch data
connec()
fetch_data()

def main():
    win=Tk()
    app=login_window(win)
    win.mainloop()

class login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("login")
        self.root.geometry("1550x800+0+0")

        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        original_frame_image = Image.open(r"../images/loginbg1.jpg")
        resized_frame_image = original_frame_image.resize((400, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_frame_image)

        original_frame_image1 = Image.open(r"../images/FFF.png")
        resized_frame_image1 = original_frame_image1.resize((100, 100), Image.BICUBIC)
        self.bg2 = ImageTk.PhotoImage(resized_frame_image1)

        # # Add a light border to the frame
        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="NAVY blue")
        self.frame_border.place(x=300, y=70, width=800, height=560)

        left_lbl = Label(self.root, image=self.bg1, bd=0)
        left_lbl.place(x=305, y=75, width=400, height=550)

        CEN_lbl = Label(self.root, image=self.bg2, bd=0)
        CEN_lbl.place(x=850, y=70, width=100, height=100)

        get_str=Label(self.frame_border,text="COPY RIGHT OWNER MUHAMMAD TALHA ",font=("times new roman",10,"bold"),fg="RED",bg='NAVY blue')
        get_str.place(x=470,y=535)

        # # label
        username=Label(self.frame_border,text="Username:",font=("times new roman",15,"bold"),fg="white",bg='NAVY blue')
        username.place(x=420,y=120)

        self.txtuser=ttk.Entry(self.frame_border,font=("times new roman",15,"bold"))
        self.txtuser.place(x=420,y=150,width=350)

        password = Label(self.frame_border, text="Password:", font=("times new roman", 15, "bold"),fg="white",bg='NAVY blue')
        password.place(x=420, y=210)

        self.txtpass = ttk.Entry(self.frame_border, font=("times new roman", 15, "bold"), show='*')  # Use show="*" to hide the password
        self.txtpass.place(x=420, y=240, width=350)  # Adjust the y-coordinate to place it correctly

        ##############ICON IMAGES###########
        #LOGIN BUTTON
        loginbtn=Button(self.frame_border,command=self.login,text="Login",font=("times new roman", 15, "bold"),bd=3,relief=RIDGE,fg="white",bg="purple",activeforeground="white",activebackground="NAVY blue")
        loginbtn.place(x=540,y=335,width=120,height=35)

        # REGISTERBUTTON
        registerbtn=Button(self.frame_border,command=self.register_window,text="New User Register",font=("times new roman", 10, "bold"),borderwidth=0,fg="white",bg="NAVY blue",activeforeground="black",activebackground="dark blue")
        registerbtn.place(x=420,y=400,width=200,height=35)

        # FORGOT PASS BUTTON
        forgetpassbtn=Button(self.frame_border,command=self.forgot_password_window,text="Forget Password",font=("times new roman", 10, "bold"),borderwidth=0,fg="white",bg="NAVY blue",activeforeground="black",activebackground="dark blue")
        forgetpassbtn.place(x=580,y=400,width=200,height=35)

    def register_window(self):
        self.new_windown=Toplevel(self.root)
        self.app=Register(self.new_windown)

    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields required")
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor()
            my_cursor.execute("select * from register where email=? and pswd=?", (
                self.txtuser.get(),
                self.txtpass.get(),
            ))
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Username & Password")
            else:
                open_main = messagebox.askyesno("YesNo", "Access only admin")
                if open_main > 0:
                    self.new_windown = Toplevel(self.root)
                    self.app = AdminWindow(self.new_windown)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
    ###################### reset Password //////////
    def reset_pass(self):
        if self.txt_newpass.get()=="":
            messagebox.showerror("Error", "Please Enter password",parent=self.root2)
        elif self.txt_email.get()=="":
            messagebox.showerror("Error", "Please Enter Email",parent=self.root2)
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor()

            qury = "SELECT * FROM register WHERE email=?"
            vlu = (self.txt_email.get(),)
            my_cursor.execute(qury, vlu)
            row = my_cursor.fetchone()

            if row is None:
                messagebox.showerror("Error", "Please Enter all fields",parent=self.root2)
            else:
                # Correct the UPDATE query
                query = "UPDATE register SET pswd=? WHERE email=?"
                value = (self.txt_newpass.get(), self.txt_email.get())
                my_cursor.execute(query, value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Your Password has been reset, please login again",parent=self.root2)
                self.root2.destroy()

            


    ###################### forget Password //////////
    def forgot_password_window(self):
        if self.txtuser.get()=="":
           messagebox.showerror("Error","Please Enter the Email Address to Reset Password")
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor() 
            query=("select * from register where email=?")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            # print(row)

            if row==None:
                messagebox.showerror("My Error","Please Enter the Valid user name")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x300+375+65")  # Set the desired width and height
                self.root2.resizable(False, False)  # Disable resizing

                l = Label(self.root2, text="Forgot Password", font=("times new roman", 20, "bold"), fg="red", bg='white')
                l.place(x=0, y=10, relwidth=1)

                new_password = Label(self.root2, text="Enter New Password", font=("times new roman", 15, "bold"), fg="black")
                new_password.place(x=50, y=80)

                self.txt_newpass = ttk.Entry(self.root2, font=("times new roman", 15, "bold"))
                self.txt_newpass.place(x=50, y=110, width=250)

                email=Label(self.root2,text="Email",font=("times new roman",15,"bold"),fg="black")
                email.place(x=50,y=160)

                self.txt_email=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txt_email.place(x=50,y=190,width=250)

                btn = Button(self.root2, text="Reset",command=self.reset_pass, font=("times new roman", 15, "bold"), bg="white", fg="green")
                btn.place(x=140, y=230)  # Adjust the y-coordinate as needed


    


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1550x800+0+0")

        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_pswd = StringVar()
        self.var_Confirms_pswd = StringVar()
        self.var_email = StringVar()

        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/qnUbi9.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        #########bg image#####
        self.bg1 = ImageTk.PhotoImage(file=r"../images/CR7.png")
        left_lbl = Label(self.root, image=self.bg1)
        left_lbl.place(x=50, y=100, width=470, height=550)

    ################## MIAN_FRAME############
        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        ############### ROW 1 FIRST NAME & LAST NAME 
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        self.fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.fname_entry.place(x=50,y=130,width=250)

        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.txt_lname.place(x=370,y=130,width=250)

        ############# ROW 2 PASSWORD AND CONFIRM PASSWORD

        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        pswd.place(x=50,y=210)

        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pswd,font=("times new roman",15,"bold"))
        self.txt_pswd.place(x=50,y=240,width=250)

        Confirm_pswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        Confirm_pswd.place(x=370,y=210)

        self.txt_Confirm_pswd=ttk.Entry(frame,textvariable=self.var_Confirms_pswd,font=("times new roman",15,"bold"),show='*')
        self.txt_Confirm_pswd.place(x=370,y=240,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="I Agree The Terms & Conditions",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=350)

               ###################  EMAIL ------------------

        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black")
        email.place(x=370,y=320)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15,"bold"))
        self.txt_email.place(x=370,y=350,width=250)


        ########################button
        img=Image.open(r"../images/images.jpg")
        img=img.resize((100,50),Image.BICUBIC)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame,image=self.photoimage,command=self.register__data,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
        b1.place(x=300,y=420,width=85)

        
        img1=Image.open(r"../images/login-png-royalty-free_60202203531a5.png")
        img1=img1.resize((100,50),Image.BICUBIC)
        self.photoimage1=ImageTk.PhotoImage(img1)
       


        ############### FUNCTION DECLEARATION_____________
    def register__data(self):
        if self.var_fname.get() == "" or self.var_pswd.get()=="" or self.var_check.get()=="" or self.var_email.get()=="":
            messagebox.showerror("Error", "All fields are required",parent=self.root)
        elif self.var_pswd.get() != self.var_Confirms_pswd.get():
            messagebox.showerror("Error", "Password & confirm password must be the same",parent=self.root)
        elif not self.var_check.get():
            messagebox.showerror("Error", "Please agree to our terms and conditions",parent=self.root)
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor()
            query = "SELECT * FROM register WHERE email=?"
            value = (self.var_email.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "User already exists. Please try another name",parent=self.root)
            else:
                # Correct the typo here: 'Inser' should be 'INSERT'
                my_cursor.execute("INSERT INTO register (fname, lname, email ,pswd) VALUES (?, ?, ?,?)", (
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_email.get(),
                    self.var_pswd.get(),
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Registration Successfully",parent=self.root)

    def return_login(self):
            self.root.destroy()

                
class AdminWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Window")
        self.root.geometry("1550x800+0+0")

        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        original_frame_image = Image.open(r"../images/leftframe.jpg")
        resized_frame_image = original_frame_image.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_frame_image)

        # Add a light border to the frame
        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=300, y=70, width=800, height=560)

        left_lbl = Label(self.root, image=self.bg1, bd=0)
        left_lbl.place(x=305, y=75, width=470, height=550)

        # self.frame_border1 = Frame(self.root, bd=0, relief="ridge", bg="blue")
 
        get_str= Button(self.frame_border,command=self.dis_window, text="DISPLAY", font=("times new roman", 25, "bold"),bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white",activebackground="dark blue")
        get_str.place(x=480, y=5, width=315, height=135)

        insetbtn= Button(self.frame_border,command=self.ins_window, text="INSERT", font=("times new roman", 25, "bold"),bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white",activebackground="dark blue")
        insetbtn.place(x=480, y=143, width=315, height=135)

        deletebtn = Button(self.frame_border,command=self.del_window, text="DELETE", font=("times new roman", 25, "bold"),bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white",activebackground="dark blue")
        deletebtn.place(x=480, y=281, width=315, height=135)

        updatebtn = Button(self.frame_border,command=self.upt_window, text="UPDATE", font=("times new roman", 25, "bold"),bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white",activebackground="dark blue")
        updatebtn.place(x=480, y=420, width=315, height=135)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()           


    def ins_window(self):
        self.in_window=Toplevel(self.root)
        self.app=Insert_win(self.in_window)

    def del_window(self):
        self.de_window=Toplevel(self.root)
        self.app=Delete_win(self.de_window)   

    def upt_window(self):
        self.up_window=Toplevel(self.root)
        self.app=update_win(self.up_window)
    
    def dis_window(self):
        self.up_window=Toplevel(self.root)
        self.app=display_win(self.up_window)

    def return_login(self):
        self.root.destroy()                    


class Insert_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Insert Window")
        self.root.geometry("1550x800+0+0")

        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # ----------------------2-------------------------------------------

        original_frame_image = Image.open(r"../images/leftframe2.jpg")
        resized_frame_image = original_frame_image.resize((300, 500), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_frame_image)

        # Add a light border to the frame
        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=100, y=70, width=310, height=550)

        left_lbl = Label(self.frame_border, image=self.bg1, bd=0)
        left_lbl.place(x=5, y=5, width=300, height=400)

        del_plybtn= Button(self.frame_border,command=self.player_win, text="INSERT PLAYER", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plybtn.place(x=5, y=410, width=300, height=135)

        # --------------------------------------3-------------------------------

        original_frame_ima = Image.open(r"../images/matchesdis.jpg")
        resized_frame_ima = original_frame_ima.resize((300, 425), Image.BICUBIC)
        self.bg2 = ImageTk.PhotoImage(resized_frame_ima)

        # Add a light border to the frame
        self.frame_bord = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_bord.place(x=500, y=70, width=310, height=550)

        left_l = Label(self.frame_bord, image=self.bg2, bd=0)
        left_l.place(x=5, y=5, width=300, height=400)

        del_plyb= Button(self.frame_bord,command=self.match_win, text="INSERT MATCH", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plyb.place(x=5, y=410, width=300, height=135)

        #---------------------------------------4------------------------------------------------

        original_frame_ima = Image.open(r"../images/ranking.jpg")
        resized_frame_ima = original_frame_ima.resize((300, 400), Image.BICUBIC)
        self.bg3 = ImageTk.PhotoImage(resized_frame_ima)

        # Add a light border to the frame
        self.frame_bord = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_bord.place(x=900, y=70, width=310, height=550)

        left_l = Label(self.frame_bord, image=self.bg3, bd=0)
        left_l.place(x=5, y=5, width=300, height=400)

        del_plyb= Button(self.frame_bord,command=self.team_s, text="INSERT TEAM RANK", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plyb.place(x=5, y=410, width=300, height=135)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()  

    def player_win(self):
        self.ply_windown=Toplevel(self.root)
        self.app=player_info_window(self.ply_windown)

    def match_win(self):
        self.ply_windown=Toplevel(self.root)
        self.app=match_info_win(self.ply_windown)

    def team_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=team_stand(self.ply_windown)    

class Delete_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Insert Window")
        self.root.geometry("1550x800+0+0")

        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        original_frame_image = Image.open(r"../images/leftframe2.jpg")
        resized_frame_image = original_frame_image.resize((300, 500), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_frame_image)

        # Add a light border to the frame
        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=520, y=70, width=310, height=550)

        left_lbl = Label(self.root, image=self.bg1, bd=0)
        left_lbl.place(x=525, y=75, width=300, height=400)

        del_plybtn= Button(self.frame_border,command=self.del_player_info_s, text="DELETE PLAYER", font=("times new roman", 20, "bold"),bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white",activebackground="dark blue")
        del_plybtn.place(x=5, y=410, width=300, height=135)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

    def del_player_info_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=del_player_info_window(self.ply_windown)   

class update_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Insert Window")
        self.root.geometry("1550x800+0+0")

        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # ----------------------2-------------------------------------------

        original_frame_image = Image.open(r"../images/update_player.jpg")
        resized_frame_image = original_frame_image.resize((300, 400), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_frame_image)

        # Add a light border to the frame
        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=100, y=70, width=310, height=550)

        left_lbl = Label(self.frame_border, image=self.bg1, bd=0)
        left_lbl.place(x=5, y=5, width=300, height=400)

        del_plybtn= Button(self.frame_border,command=self.upd_player_info_s, text="UPDATE PLAYER", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plybtn.place(x=5, y=410, width=300, height=135)

        # --------------------------------------3-------------------------------

        original_frame_ima = Image.open(r"../images/update_match.jpg")
        resized_frame_ima = original_frame_ima.resize((300, 425), Image.BICUBIC)
        self.bg2 = ImageTk.PhotoImage(resized_frame_ima)

        # Add a light border to the frame
        self.frame_bord = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_bord.place(x=500, y=70, width=310, height=550)

        left_l = Label(self.frame_bord, image=self.bg2, bd=0)
        left_l.place(x=5, y=5, width=300, height=400)

        del_plyb= Button(self.frame_bord,command=self.upd_MATCH_s, text="UPDATE MATCH", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plyb.place(x=5, y=410, width=300, height=135)

        #---------------------------------------4------------------------------------------------

        original_frame_ima = Image.open(r"../images/ranking.jpg")
        resized_frame_ima = original_frame_ima.resize((300, 400), Image.BICUBIC)
        self.bg3 = ImageTk.PhotoImage(resized_frame_ima)

        # Add a light border to the frame
        self.frame_bord = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_bord.place(x=900, y=70, width=310, height=550)

        left_l = Label(self.frame_bord, image=self.bg3, bd=0)
        left_l.place(x=5, y=5, width=300, height=400)

        del_plyb= Button(self.frame_bord,command=self.upd_team_s, text="UPDATE TEAM RANK", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plyb.place(x=5, y=410, width=300, height=135)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

    def upd_team_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=upd_team_stand(self.ply_windown)

    def upd_MATCH_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=upd_match_info_win(self.ply_windown)

    def upd_player_info_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=upd_player_info_window(self.ply_windown)   


class display_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Display Window")
        self.root.geometry("1550x800+0+0")

        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # ----------------------2-------------------------------------------

        original_frame_image = Image.open(r"../images/dis_team.jpg")
        resized_frame_image = original_frame_image.resize((300, 400), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_frame_image)

        # Add a light border to the frame
        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=10, y=70, width=310, height=550)

        left_lbl = Label(self.frame_border, image=self.bg1, bd=0)
        left_lbl.place(x=5, y=5, width=300, height=400)

        del_plybtn= Button(self.frame_border,command=self.disteam_info_s, text="DISPLAY TEAM", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plybtn.place(x=5, y=410, width=300, height=135)

        # --------------------------------------3-------------------------------

        original_frame_ima = Image.open(r"../images/leftframe2.jpg")
        resized_frame_ima = original_frame_ima.resize((300, 500), Image.BICUBIC)
        self.bg2 = ImageTk.PhotoImage(resized_frame_ima)

        # Add a light border to the frame
        self.frame_bord = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_bord.place(x=350, y=70, width=310, height=550)

        left_l = Label(self.frame_bord, image=self.bg2, bd=0)
        left_l.place(x=5, y=5, width=300, height=400)

        del_plyb= Button(self.frame_bord,command=self.playerinfo_s, text="PLAYER INFO", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plyb.place(x=5, y=410, width=300, height=135)

        #---------------------------------------4------------------------------------------------

        original_frame_ima = Image.open(r"../images/matchesdis.jpg")
        resized_frame_ima = original_frame_ima.resize((300, 400), Image.BICUBIC)
        self.bg3 = ImageTk.PhotoImage(resized_frame_ima)

        # Add a light border to the frame
        self.frame_bord = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_bord.place(x=695, y=70, width=310, height=550)

        left_l = Label(self.frame_bord, image=self.bg3, bd=0)
        left_l.place(x=5, y=5, width=300, height=400)

        del_plyb= Button(self.frame_bord,command=self.MATCHES, text="DISPLAY MATCHES", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plyb.place(x=5, y=410, width=300, height=135)

        original_frame_ima = Image.open(r"../images/ranking.jpg")
        resized_frame_ima = original_frame_ima.resize((300, 400), Image.BICUBIC)
        self.bg5 = ImageTk.PhotoImage(resized_frame_ima)

        # Add a light border to the frame
        self.frame_bord = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_bord.place(x=1040, y=70, width=310, height=550)

        left_l = Label(self.frame_bord, image=self.bg5, bd=0)
        left_l.place(x=5, y=5, width=300, height=400)

        del_plyb= Button(self.frame_bord,command=self.RANKING_s, text="DISPLAY TEAM RANK", font=("times new roman", 20, "bold"), bd=3, relief=RIDGE, fg="white", bg="dark blue", activeforeground="white", activebackground="dark blue")
        del_plyb.place(x=5, y=410, width=300, height=135)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

    def disteam_info_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=display_TEAMS_win(self.ply_windown)

    def MATCHES(self):
        self.ply_windown=Toplevel(self.root)
        self.app=display_MATCHESSSS_win(self.ply_windown)

    def RANKING_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=display_RANK_win(self.ply_windown) 

    def playerinfo_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=display_playerinfo_win(self.ply_windown)                    

class player_info_window:
    def __init__(self, root):
        self.root = root
        self.root.title("player_info")
        self.root.geometry("1550x800+0+0")

        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_player_id = StringVar()
        self.var_jersey_no = StringVar()
        self.var_position = StringVar()
        self.var_Team_Id = StringVar()

        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=30, y=40, width=1290, height=570)

        original_bg1 = Image.open(r"../images/UPDATE PLAYER.jpg")
        resized_bg1 = original_bg1.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_bg1)
        left_lbl = Label(self.frame_border, image=self.bg1)
        left_lbl.place(x=10, y=10, width=470, height=550)

    ################## MIAN_FRAME############
        frame=Frame(self.frame_border,bg="white")
        frame.place(x=480,y=10,width=800,height=550)

        register_lbl=Label(frame,text="INSERT HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        ############### ROW 1 FIRST NAME & LAST NAME 
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=80)

        self.fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.fname_entry.place(x=50,y=110,width=250)

        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black")
        l_name.place(x=370,y=80)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.txt_lname.place(x=370,y=110,width=250)

        ############# ROW 2 playerid AND position 

        player_id=Label(frame,text="Player ID",font=("times new roman",15,"bold"),bg="white",fg="black")
        player_id.place(x=50,y=170)

        self.txt_player_id=ttk.Entry(frame,textvariable=self.var_player_id,font=("times new roman",15,"bold"))
        self.txt_player_id.place(x=50,y=200,width=250)

        position=Label(frame,text="Position",font=("times new roman",15,"bold"),bg="white",fg="black")
        position.place(x=370,y=170)

        self.txt_position=ttk.Entry(frame,textvariable=self.var_position,font=("times new roman",15,"bold"))
        self.txt_position.place(x=370,y=200,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="Are you sure",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=350)

               ###################  jerser number ------------------

        jersey_no=Label(frame,text="Jersey No",font=("times new roman",15,"bold"),bg="white",fg="black")
        jersey_no.place(x=370,y=260)

        self.txt_jersey_no=ttk.Entry(frame,textvariable=self.var_jersey_no,font=("times new roman",15,"bold"))
        self.txt_jersey_no.place(x=370,y=290,width=250)

        Team_Name=Label(frame,text="Team ID",font=("times new roman",15,"bold"),bg="white",fg="black")
        Team_Name.place(x=50,y=260)

        self.txt_Team_Name=ttk.Entry(frame,textvariable=self.var_Team_Id,font=("times new roman",15,"bold"))
        self.txt_Team_Name.place(x=50,y=290,width=250)

        


        ########################button
        donebtn = Button(self.root,command=self.Done, text="DONE", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        donebtn.place(x=1100, y=500, width=75, height=50)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()


            ############### FUNCTION DECLEARATION_____________
    def Done(self):
        if (
            self.var_fname.get() == ""
            or self.var_lname.get() == ""
            or self.var_player_id.get() == ""
            or self.var_jersey_no.get() == ""
            or self.var_position.get() == ""
            or self.var_Team_Id.get() == ""
        ):
            messagebox.showerror("Error", "All fields are required",parent=self.root)
        elif not self.var_check.get():
            messagebox.showerror("Error", "Please Make Sure",parent=self.root)
        else:
            try:
                conn = sqlite3.connect('AppData.db')
                my_cursor = conn.cursor()

                query = "INSERT INTO players (player_id, team_id, fname, lname, position, jerseyno) VALUES (?, ?, ?, ?, ?, ?)"
                values = (
                            self.var_player_id.get(),
                            self.var_Team_Id.get(),
                            self.var_fname.get(),
                            self.var_lname.get(),
                            self.var_position.get(),
                            self.var_jersey_no.get(),
                )

                my_cursor.execute(query, values)
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Player information added successfully",parent=self.root)

            except sqlite3.Error as err:
                if err.errno == 1644:
# --------------------------------
                    messagebox.showerror("Error", "Cannot insert more than 11 players with the same team_id",parent=self.root)
                else:
                    # Handle other MySQL errors
                    messagebox.showerror("MySQL Error", f"Error: {err}",parent=self.root)
            
class match_info_win:
    def __init__(self, root):
        self.root = root
        self.root.title("match_info")
        self.root.geometry("1550x800+0+0")

        self.var_match_id = StringVar()
        self.var_date_ = StringVar()
        self.var_venue = StringVar()
        self.var_result = StringVar()
        self.var_hometeam_id = StringVar()
        self.var_awayteam_id = StringVar()

        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=30, y=40, width=1290, height=570)

        original_bg1 = Image.open(r"../images/insert match.png")
        resized_bg1 = original_bg1.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_bg1)
        left_lbl = Label(self.frame_border, image=self.bg1)
        left_lbl.place(x=10, y=10, width=470, height=550)

    ################## MIAN_FRAME############
        frame=Frame(self.frame_border,bg="white")
        frame.place(x=480,y=10,width=800,height=550)

        register_lbl=Label(frame,text="INSERT HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        ############### ROW 1 FIRST NAME & LAST NAME 
        match_id=Label(frame,text="Match ID",font=("times new roman",15,"bold"),bg="white")
        match_id.place(x=50,y=80)

        self.match_id_entry=ttk.Entry(frame,textvariable=self.var_match_id,font=("times new roman",15,"bold"))
        self.match_id_entry.place(x=50,y=110,width=250)

        date_=Label(frame,text="Match Date",font=("times new roman",15,"bold"),bg="white",fg="black")
        date_.place(x=370,y=80)

        self.txt_date_=ttk.Entry(frame,textvariable=self.var_date_,font=("times new roman",15,"bold"))
        self.txt_date_.place(x=370,y=110,width=250)

        ############# ROW 2 playerid AND position 

        venue=Label(frame,text="Venue",font=("times new roman",15,"bold"),bg="white",fg="black")
        venue.place(x=50,y=170)

        self.txt_venue=ttk.Entry(frame,textvariable=self.var_venue,font=("times new roman",15,"bold"))
        self.txt_venue.place(x=50,y=200,width=250)

        result=Label(frame,text="Result",font=("times new roman",15,"bold"),bg="white",fg="black")
        result.place(x=370,y=170)

        self.txt_result=ttk.Entry(frame,textvariable=self.var_result,font=("times new roman",15,"bold"))
        self.txt_result.place(x=370,y=200,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="Are you sure",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=350)

               ###################  jerser number ------------------

        hometeam_id=Label(frame,text="Home Team_id",font=("times new roman",15,"bold"),bg="white",fg="black")
        hometeam_id.place(x=370,y=260)

        self.txt_hometeam_id=ttk.Entry(frame,textvariable=self.var_hometeam_id,font=("times new roman",15,"bold"))
        self.txt_hometeam_id.place(x=370,y=290,width=250)

        awayteam_id=Label(frame,text="Away Team_id ",font=("times new roman",15,"bold"),bg="white",fg="black")
        awayteam_id.place(x=50,y=260)

        self.txt_awayteam_id=ttk.Entry(frame,textvariable=self.var_awayteam_id,font=("times new roman",15,"bold"))
        self.txt_awayteam_id.place(x=50,y=290,width=250)


        ########################button
        donebtn = Button(self.root,command=self.Done_, text="DONE", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        donebtn.place(x=1100, y=500, width=75, height=50)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

        ############### FUNCTION DECLEARATION_____________
    def Done_(self):
        if (
            not self.var_match_id.get().isdigit()
            or not self.var_hometeam_id.get().isdigit()
            or not self.var_awayteam_id.get().isdigit()
            or self.var_date_.get() == ""
            or self.var_venue.get() == ""
            or self.var_result.get() == ""
        ):
            messagebox.showerror("Error", "Please enter valid numeric values for Match ID, HomeTeam ID, and AwayTeam ID",parent=self.root)
        elif not self.var_check.get():
            messagebox.showerror("Error", "Please Make Sure",parent=self.root)
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor()

            query = "INSERT INTO matches (match_id, date_, venue, result, hometeam_id, awayteam_id) VALUES (?, ?, ?, ?, ?, ?)"
            values = (
                self.var_match_id.get(),
                self.var_date_.get(),
                self.var_venue.get(),
                self.var_result.get(),
                self.var_hometeam_id.get(),
                self.var_awayteam_id.get(),
            )

            my_cursor.execute(query, values)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Match information added successfully",parent=self.root)

class team_stand:
    def __init__(self, root):
        self.root = root
        self.root.title("TEAM STATS")
        self.root.geometry("1550x800+0+0")

        self.var_TEAM_ID = StringVar()
        self.var_win = StringVar()
        self.var_draw = StringVar()
        self.var_lose = StringVar()
        self.var_points = StringVar()


        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=30, y=40, width=1290, height=570)

        original_bg1 = Image.open(r"../images/ranking.jpg")
        resized_bg1 = original_bg1.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_bg1)
        left_lbl = Label(self.frame_border, image=self.bg1)
        left_lbl.place(x=10, y=10, width=470, height=550)

    ################## MIAN_FRAME############
        frame=Frame(self.frame_border,bg="white")
        frame.place(x=480,y=10,width=800,height=550)

        register_lbl=Label(frame,text="INSERT HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        ############### ROW 1 FIRST NAME & LAST NAME 
        TEAM_ID=Label(frame,text="TEAM ID",font=("times new roman",15,"bold"),bg="white")
        TEAM_ID.place(x=50,y=80)

        self.TEAM_ID=ttk.Entry(frame,textvariable=self.var_TEAM_ID,font=("times new roman",15,"bold"))
        self.TEAM_ID.place(x=50,y=110,width=250)

        win=Label(frame,text="WIN",font=("times new roman",15,"bold"),bg="white",fg="black")
        win.place(x=370,y=80)

        self.txt_win=ttk.Entry(frame,textvariable=self.var_win,font=("times new roman",15,"bold"))
        self.txt_win.place(x=370,y=110,width=250)

        ############# ROW 2 playerid AND position 

        draw=Label(frame,text="LOSE",font=("times new roman",15,"bold"),bg="white",fg="black")
        draw.place(x=50,y=170)

        self.txt_draw=ttk.Entry(frame,textvariable=self.var_draw,font=("times new roman",15,"bold"))
        self.txt_draw.place(x=50,y=200,width=250)

        lose=Label(frame,text="DRAW",font=("times new roman",15,"bold"),bg="white",fg="black")
        lose.place(x=370,y=170)

        self.txt_lose=ttk.Entry(frame,textvariable=self.var_lose,font=("times new roman",15,"bold"))
        self.txt_lose.place(x=370,y=200,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="Are you sure",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=290)

               ###################  jerser number ------------------

        points=Label(frame,text="POINTS",font=("times new roman",15,"bold"),bg="white",fg="black")
        points.place(x=370,y=260)

        self.txt_points=ttk.Entry(frame,textvariable=self.var_points,font=("times new roman",15,"bold"))
        self.txt_points.place(x=370,y=290,width=250)


        ########################button
        donebtn = Button(self.root,command=self.Done__, text="DONE", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        donebtn.place(x=1100, y=500, width=75, height=50)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

        ############### FUNCTION DECLEARATION_____________
    def Done__(self):
        if (
            not self.var_TEAM_ID.get().isdigit()
            or not self.var_win.get().isdigit()
            or not self.var_draw.get().isdigit()
            or not self.var_lose.get().isdigit()
            or not self.var_points.get().isdigit()
            or not self.var_check.get()
        ):
            messagebox.showerror("Error", "Please enter valid numeric values and make sure to check the confirmation checkbox",parent=self.root)
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor()

            query = "INSERT INTO team_rank (TEAM_ID, win, draw, lose, points) VALUES (?, ?, ?, ?, ?)"
            values = (
                self.var_TEAM_ID.get(),
                self.var_win.get(),
                self.var_draw.get(),
                self.var_lose.get(),
                self.var_points.get(),
            )

            my_cursor.execute(query, values)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Team statistics added successfully",parent=self.root)

class upd_team_stand:
    def __init__(self, root):
        self.root = root
        self.root.title("UPDATE STATS")
        self.root.geometry("1550x800+0+0")

        self.var_TEAM_ID = StringVar()
        self.var_win = StringVar()
        self.var_draw = StringVar()
        self.var_lose = StringVar()
        self.var_points = StringVar()


        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=30, y=40, width=1290, height=570)

        original_bg1 = Image.open(r"../images/ranking.jpg")
        resized_bg1 = original_bg1.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_bg1)
        left_lbl = Label(self.frame_border, image=self.bg1)
        left_lbl.place(x=10, y=10, width=470, height=550)

    ################## MIAN_FRAME############
        frame=Frame(self.frame_border,bg="white")
        frame.place(x=480,y=10,width=800,height=550)

        register_lbl=Label(frame,text="UPDATE HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        ############### ROW 1 FIRST NAME & LAST NAME 
        TEAM_ID=Label(frame,text="TEAM ID",font=("times new roman",15,"bold"),bg="white")
        TEAM_ID.place(x=50,y=80)

        self.TEAM_ID=ttk.Entry(frame,textvariable=self.var_TEAM_ID,font=("times new roman",15,"bold"))
        self.TEAM_ID.place(x=50,y=110,width=250)

        win=Label(frame,text="WIN",font=("times new roman",15,"bold"),bg="white",fg="black")
        win.place(x=370,y=80)

        self.txt_win=ttk.Entry(frame,textvariable=self.var_win,font=("times new roman",15,"bold"))
        self.txt_win.place(x=370,y=110,width=250)

        ############# ROW 2 playerid AND position 

        draw=Label(frame,text="LOSE",font=("times new roman",15,"bold"),bg="white",fg="black")
        draw.place(x=50,y=170)

        self.txt_draw=ttk.Entry(frame,textvariable=self.var_draw,font=("times new roman",15,"bold"))
        self.txt_draw.place(x=50,y=200,width=250)

        lose=Label(frame,text="DRAW",font=("times new roman",15,"bold"),bg="white",fg="black")
        lose.place(x=370,y=170)

        self.txt_lose=ttk.Entry(frame,textvariable=self.var_lose,font=("times new roman",15,"bold"))
        self.txt_lose.place(x=370,y=200,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="Are you sure",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=290)

               ###################  jerser number ------------------

        points=Label(frame,text="POINTS",font=("times new roman",15,"bold"),bg="white",fg="black")
        points.place(x=370,y=260)

        self.txt_points=ttk.Entry(frame,textvariable=self.var_points,font=("times new roman",15,"bold"))
        self.txt_points.place(x=370,y=290,width=250)


        ########################button
        donebtn = Button(self.root,command=self.Done1, text="DONE", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        donebtn.place(x=1100, y=500, width=75, height=50)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

        ############### FUNCTION DECLEARATION_____________
    def Done1(self):
        if (
            not self.var_TEAM_ID.get().isdigit()
            or not self.var_win.get().isdigit()
            or not self.var_draw.get().isdigit()
            or not self.var_lose.get().isdigit()
            or not self.var_points.get().isdigit()
            or not self.var_check.get()
        ):
            messagebox.showerror("Error", "Please enter valid numeric values and make sure to check the confirmation checkbox",parent=self.root)
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor()

            # Use UPDATE query instead of INSERT
            query = "UPDATE team_rank SET win=?, draw=?, lose=?, points=? WHERE TEAM_ID=?"
            values = (
                self.var_win.get(),
                self.var_draw.get(),
                self.var_lose.get(),
                self.var_points.get(),
                self.var_TEAM_ID.get(),
            )

            my_cursor.execute(query, values)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Team statistics updated successfully",parent=self.root)

class upd_match_info_win:
    def __init__(self, root):
        self.root = root
        self.root.title("match_info")
        self.root.geometry("1550x800+0+0")

        self.var_match_id = StringVar()
        self.var_date_ = StringVar()
        self.var_venue = StringVar()
        self.var_result = StringVar()
        self.var_hometeam_id = StringVar()
        self.var_awayteam_id = StringVar()

        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=30, y=40, width=1290, height=570)

        original_bg1 = Image.open(r"../images/insert match.png")
        resized_bg1 = original_bg1.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_bg1)
        left_lbl = Label(self.frame_border, image=self.bg1)
        left_lbl.place(x=10, y=10, width=470, height=550)

    ################## MIAN_FRAME############
        frame=Frame(self.frame_border,bg="white")
        frame.place(x=480,y=10,width=800,height=550)

        register_lbl=Label(frame,text="UPDATE HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        ############### ROW 1 FIRST NAME & LAST NAME 
        match_id=Label(frame,text="Match ID",font=("times new roman",15,"bold"),bg="white")
        match_id.place(x=50,y=80)

        self.match_id_entry=ttk.Entry(frame,textvariable=self.var_match_id,font=("times new roman",15,"bold"))
        self.match_id_entry.place(x=50,y=110,width=250)

        date_=Label(frame,text="Match Date",font=("times new roman",15,"bold"),bg="white",fg="black")
        date_.place(x=370,y=80)

        self.txt_date_=ttk.Entry(frame,textvariable=self.var_date_,font=("times new roman",15,"bold"))
        self.txt_date_.place(x=370,y=110,width=250)

        ############# ROW 2 playerid AND position 

        venue=Label(frame,text="Venue",font=("times new roman",15,"bold"),bg="white",fg="black")
        venue.place(x=50,y=170)

        self.txt_venue=ttk.Entry(frame,textvariable=self.var_venue,font=("times new roman",15,"bold"))
        self.txt_venue.place(x=50,y=200,width=250)

        result=Label(frame,text="Result",font=("times new roman",15,"bold"),bg="white",fg="black")
        result.place(x=370,y=170)

        self.txt_result=ttk.Entry(frame,textvariable=self.var_result,font=("times new roman",15,"bold"))
        self.txt_result.place(x=370,y=200,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="Are you sure",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=350)

               ###################  jerser number ------------------

        hometeam_id=Label(frame,text="Home Team_id",font=("times new roman",15,"bold"),bg="white",fg="black")
        hometeam_id.place(x=370,y=260)

        self.txt_hometeam_id=ttk.Entry(frame,textvariable=self.var_hometeam_id,font=("times new roman",15,"bold"))
        self.txt_hometeam_id.place(x=370,y=290,width=250)

        awayteam_id=Label(frame,text="Away Team_id ",font=("times new roman",15,"bold"),bg="white",fg="black")
        awayteam_id.place(x=50,y=260)

        self.txt_awayteam_id=ttk.Entry(frame,textvariable=self.var_awayteam_id,font=("times new roman",15,"bold"))
        self.txt_awayteam_id.place(x=50,y=290,width=250)


        ########################button
        donebtn = Button(self.root,command=self.Done2, text="DONE", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        donebtn.place(x=1100, y=500, width=75, height=50)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

        ############### FUNCTION DECLEARATION_____________
    def Done2(self):
        if (
            not self.var_match_id.get().isdigit()
            or not self.var_hometeam_id.get().isdigit()
            or not self.var_awayteam_id.get().isdigit()
            or self.var_date_.get() == ""
            or self.var_venue.get() == ""
            or self.var_result.get() == ""
        ):
            messagebox.showerror("Error", "Please enter valid numeric values for Match ID, HomeTeam ID, and AwayTeam ID",parent=self.root)
        elif not self.var_check.get():
            messagebox.showerror("Error", "Please Make Sure",parent=self.root)
        else:
            conn = sqlite3.connect('AppData.db')
            my_cursor = conn.cursor()

            # Use UPDATE query instead of INSERT
            query = "UPDATE matches SET date_=?, venue=?, result=?, hometeam_id=?, awayteam_id=? WHERE match_id=?"
            values = (
                self.var_date_.get(),
                self.var_venue.get(),
                self.var_result.get(),
                self.var_hometeam_id.get(),
                self.var_awayteam_id.get(),
                self.var_match_id.get(),
            )

            my_cursor.execute(query, values)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Match information updated successfully",parent=self.root)

class upd_player_info_window:
    def __init__(self, root):
        self.root = root
        self.root.title("player_info")
        self.root.geometry("1550x800+0+0")

        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_player_id = StringVar()
        self.var_jersey_no = StringVar()
        self.var_position = StringVar()
        self.var_Team_Id = StringVar()

        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=30, y=40, width=1290, height=570)

        original_bg1 = Image.open(r"../images/UPDATE PLAYER.jpg")
        resized_bg1 = original_bg1.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_bg1)
        left_lbl = Label(self.frame_border, image=self.bg1)
        left_lbl.place(x=10, y=10, width=470, height=550)

    ################## MIAN_FRAME############
        frame=Frame(self.frame_border,bg="white")
        frame.place(x=480,y=10,width=800,height=550)

        register_lbl=Label(frame,text="UPDATE HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        ############### ROW 1 FIRST NAME & LAST NAME 
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=80)

        self.fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.fname_entry.place(x=50,y=110,width=250)

        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black")
        l_name.place(x=370,y=80)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.txt_lname.place(x=370,y=110,width=250)

        ############# ROW 2 playerid AND position 

        player_id=Label(frame,text="Player ID",font=("times new roman",15,"bold"),bg="white",fg="black")
        player_id.place(x=50,y=170)

        self.txt_player_id=ttk.Entry(frame,textvariable=self.var_player_id,font=("times new roman",15,"bold"))
        self.txt_player_id.place(x=50,y=200,width=250)

        position=Label(frame,text="Position",font=("times new roman",15,"bold"),bg="white",fg="black")
        position.place(x=370,y=170)

        self.txt_position=ttk.Entry(frame,textvariable=self.var_position,font=("times new roman",15,"bold"))
        self.txt_position.place(x=370,y=200,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="Are you sure",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,y=350)

               ###################  jerser number ------------------

        jersey_no=Label(frame,text="Jersey No",font=("times new roman",15,"bold"),bg="white",fg="black")
        jersey_no.place(x=370,y=260)

        self.txt_jersey_no=ttk.Entry(frame,textvariable=self.var_jersey_no,font=("times new roman",15,"bold"))
        self.txt_jersey_no.place(x=370,y=290,width=250)

        Team_Name=Label(frame,text="Team ID",font=("times new roman",15,"bold"),bg="white",fg="black")
        Team_Name.place(x=50,y=260)

        self.txt_Team_Name=ttk.Entry(frame,textvariable=self.var_Team_Id,font=("times new roman",15,"bold"))
        self.txt_Team_Name.place(x=50,y=290,width=250)


        ########################button
        donebtn = Button(self.root,command=self.Done5, text="DONE", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        donebtn.place(x=1100, y=500, width=75, height=50)


        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

        ############### FUNCTION DECLEARATION_____________
    def Done5(self):
        if (
            self.var_fname.get() == ""
            or self.var_lname.get() == ""
            or self.var_player_id.get() == ""
            or self.var_jersey_no.get() == ""
            or self.var_position.get() == ""
            or self.var_Team_Id.get() == ""
        ):
            messagebox.showerror("Error", "All fields are required",parent=self.root)
        elif not self.var_check.get():
            messagebox.showerror("Error", "Please Make Sure",parent=self.root)
        else:
            try:
                conn = sqlite3.connect('AppData.db')
                my_cursor = conn.cursor()

                query = "UPDATE players SET team_id=?, fname=?, lname=?, jerseyno=?, position=? WHERE player_id=?"
                values = (
                    self.var_Team_Id.get(),
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_jersey_no.get(),
                    self.var_position.get(),
                    self.var_player_id.get(),
                )

                my_cursor.execute(query, values)
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Player information updated successfully",parent=self.root)

            except sqlite3.Error as err:
                if err.errno == 1644:
                    # Error number 1644 corresponds to the error raised by the trigger
                    messagebox.showerror("Error", "Cannot update to more than 11 players with the same team_id",parent=self.root)
                else:
                    # Handle other MySQL errors
                    messagebox.showerror("MySQL Error", f"Error: {err}",parent=self.root)

            

class del_player_info_window:
    def __init__(self, root):
        self.root = root
        self.root.title("player_info")
        self.root.geometry("1550x800+0+0")

        self.var_player_id = StringVar()

        #########bg image#####
        self.bg = ImageTk.PhotoImage(file=r"../images/bg3.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=300, y=40, width=790, height=570)

        original_bg1 = Image.open(r"../images/CR7.png")
        resized_bg1 = original_bg1.resize((470, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_bg1)
        left_lbl = Label(self.frame_border, image=self.bg1)
        left_lbl.place(x=10, y=10, width=470, height=550)


    ################## MIAN_FRAME############
        frame=Frame(self.frame_border,bg="white")
        frame.place(x=480,y=10,width=300,height=550)

        register_lbl=Label(frame,text="DELETE HERE",font=("times new roman",20,"bold"),fg="dark red",bg="white")
        register_lbl.place(x=20,y=20)

        ########### label entry #######

        player_id=Label(frame,text="Player ID",font=("times new roman",15,"bold"),bg="white",fg="black")
        player_id.place(x=30,y=100)

        self.txt_player_id=ttk.Entry(frame,textvariable=self.var_player_id,font=("times new roman",15,"bold"))
        self.txt_player_id.place(x=30,y=150,width=250)

        ############ check button

        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame,variable=self.var_check,text="Are you sure",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=30,y=200)

        ########################button
        # img=Image.open(r"../images/images.jpg")
        # img=img.resize((100,50),Image.BICUBIC)
        # self.photoimage=ImageTk.PhotoImage(img)
        # b1=Button(frame,image=self.photoimage,command=self.Done6,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
        # b1.place(x=100,y=420,width=85)

        deletebtn2 = Button(frame,command=self.Done6, text="DELETE", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="RED", activeforeground="white",activebackground="dark blue")
        deletebtn2.place(x=100,y=420,width=85, height=50)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

    def Done6(self):
            if not self.var_player_id.get():
                messagebox.showerror("Error", "Player ID is required",parent=self.root)
            elif not self.var_check.get():
                messagebox.showerror("Error", "Please Make Sure",parent=self.root)
            else:
                confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this player's information?",parent=self.root)
                if confirmation:
                    conn = sqlite3.connect('AppData.db')
                    my_cursor = conn.cursor()

                    query = "DELETE FROM players WHERE player_id = ?"
                    player_id = self.var_player_id.get()
                    my_cursor.execute(query, (player_id,))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", f"Player with ID {player_id} deleted successfully",parent=self.root)

class display_TEAMS_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Insert Window")
        self.root.geometry("1550x800+0+0")

        # Load background image
        self.bg = ImageTk.PhotoImage(file=r"../images/uefa-champions-league-star-bowl-rlsrfh81jsb88ed1.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        ######### Resize and display the frame image #####
        original_frame_image = Image.open(r"../images/frame display.png")
        resized_frame_image = original_frame_image.resize((900, 550), Image.BICUBIC)
        self.bg1 = ImageTk.PhotoImage(resized_frame_image)

        # Add a light border to the frame
        self.frame_border = Frame(self.root, bd=0, relief="ridge", bg="purple")
        self.frame_border.place(x=230, y=100, width=910, height=560)

        left_lbl = Label(self.frame_border, image=self.bg1, bd=0)
        left_lbl.place(x=5, y=5, width=900, height=550)

        # BARCELONA BUTTON
        bar_btn = Button(left_lbl, text="BARCELONA",command=self.barca_s, font=("times new roman", 20, "bold"), borderwidth=4, fg="dark blue",
                         bg="yellow", activeforeground="black", activebackground="red")
        bar_btn.place(x=43, y=30, width=205, height=35)

        # # REAL MADRID
        rea_btn = Button(left_lbl, text="REAL MADRID",command=self.real_madrid_s, font=("times new roman", 20, "bold"), borderwidth=4, fg="BLUE",
                         bg="yellow", activeforeground="black", activebackground="red")
        rea_btn.place(x=340, y=30, width=205, height=35)

        # PSG BUTTON
        psg_btn = Button(left_lbl, text="PSG",command=self.psg_s, font=("times new roman", 20, "bold"), borderwidth=4, fg="red",
                         bg="yellow", activeforeground="black", activebackground="red")
        psg_btn.place(x=640, y=30, width=205, height=35)

        backbtn = Button(self.root,command=self.return_login, text="BACK", font=("times new roman", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="PURPLE", activeforeground="white",activebackground="dark blue")
        backbtn.place(x=8, y=625, width=75, height=50)

    def return_login(self):
        self.root.destroy()

    def real_madrid_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=display_real_win(self.ply_windown)

    def barca_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=display_BARCA_win(self.ply_windown)

    def psg_s(self):
        self.ply_windown=Toplevel(self.root)
        self.app=display_psg_win(self.ply_windown)  

class display_real_win:
    def __init__(self, root):
        self.root = root
        self.root.title("REAL MADRID")
        self.root.geometry("1550x800+0+0")

        # Variables
        self.var_Teamid = StringVar()
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_position = StringVar()

        original_bg = Image.open(r"../images/bg2321.png")
        resized_bg = original_bg.resize((1400, 750), Image.BICUBIC)  # Set the desired width and height
        self.bg = ImageTk.PhotoImage(resized_bg)

        # Create a label and place the resized background image on it
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        # Frame and Treeview
        frame_border = Frame(self.root, bd=3, relief="ridge", bg="blue")         
        frame_border.place(x=230, y=250, width=910, height=280)

        # scroll_X = ttk.Scrollbar(frame_border, orient=VERTICAL)
        self.treeview = ttk.Treeview(frame_border, columns=('TEAM_ID', 'FIRST NAME', 'LAST NAME', 'POSITION'))

        # scroll_X.pack(side=RIGHT, fill=Y)
        # scroll_X.config(command=self.treeview.yview)

        # Configure column widths
        self.treeview.column('TEAM_ID', width=100, anchor='center')
        self.treeview.column('FIRST NAME', width=200, anchor='center')
        self.treeview.column('LAST NAME', width=200, anchor='center')
        self.treeview.column('POSITION', width=150, anchor='center')

        # Set the font for the entire Treeview
        font_size = 12  # Adjust the font size as needed
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', font_size, 'bold'))

        # Configure column headings
        for col in('TEAM_ID', 'FIRST NAME', 'LAST NAME', 'POSITION'):
            self.treeview.heading(col, text=col, command=lambda c=col: self.sort_treeview(c), anchor='center')

        self.treeview['show'] = 'headings'

        self.treeview.pack(fill=BOTH, expand=1)

        # Button to refresh data
        refresh_button = Button(self.root, text="Refresh", command=self.display_data,font=("times new roman", 20, "bold"), borderwidth=4, fg="white",
                         bg="red", activeforeground="black", activebackground="red")
        refresh_button.place(x=600, y=610)

        # Display initial data
        self.display_data()

    def display_data(self):
        # Connect to the MySQL database
        conn = sqlite3.connect('AppData.db')

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Execute the SQL query
            query = """SELECT tb.TEAM_ID, p.fname, p.lname, p.position
                   FROM team_bar tb
                   JOIN players p ON tb.TEAM_ID = p.team_id
                   WHERE tb.TEAM_ID = 2"""
            cursor.execute(query)

            # Clear existing data in the Treeview
            for row in self.treeview.get_children():
                self.treeview.delete(row)

            # Fetch all the rows
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                self.treeview.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def sort_treeview(self, col):
        data = [(self.treeview.set(child, col), child) for child in self.treeview.get_children('')]
        data.sort()
        for i, item in enumerate(data):
            self.treeview.move(item[1], '', i)



class display_BARCA_win:
    def __init__(self, root):
        self.root = root
        self.root.title("barca windows")
        self.root.geometry("1550x800+0+0")

        # Variables
        self.var_Teamid = StringVar()
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_position = StringVar()

        original_bg = Image.open(r"../images/new bg.png")
        resized_bg = original_bg.resize((1400, 750), Image.BICUBIC)  # Set the desired width and height
        self.bg = ImageTk.PhotoImage(resized_bg)

        # Create a label and place the resized background image on it
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame and Treeview
        frame_border = Frame(self.root, bd=3, relief="ridge", bg="blue")         
        frame_border.place(x=230, y=250, width=910, height=280)

        # scroll_X = ttk.Scrollbar(frame_border, orient=VERTICAL)
        self.treeview = ttk.Treeview(frame_border, columns=('TEAM_ID', 'FIRST NAME', 'LAST NAME', 'POSITION'))

        # scroll_X.pack(side=RIGHT, fill=Y)
        # scroll_X.config(command=self.treeview.yview)

        # Configure column widths
        self.treeview.column('TEAM_ID', width=100, anchor='center')
        self.treeview.column('FIRST NAME', width=200, anchor='center')
        self.treeview.column('LAST NAME', width=200, anchor='center')
        self.treeview.column('POSITION', width=150, anchor='center')

        # Set the font for the entire Treeview
        font_size = 12  # Adjust the font size as needed
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', font_size, 'bold'))

        # Configure column headings
        for col in('TEAM_ID', 'FIRST NAME', 'LAST NAME', 'POSITION'):
            self.treeview.heading(col, text=col, command=lambda c=col: self.sort_treeview(c), anchor='center')

        self.treeview['show'] = 'headings'

        self.treeview.pack(fill=BOTH, expand=1)

        # Button to refresh data
        refresh_button = Button(self.root, text="Refresh", command=self.display_data,font=("times new roman", 20, "bold"), borderwidth=4, fg="white",
                         bg="red", activeforeground="black", activebackground="red")
        refresh_button.place(x=600, y=610)

        # Display initial data
        self.display_data()

    def display_data(self):
        # Connect to the MySQL database
        conn = sqlite3.connect('AppData.db')

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Execute the SQL query
            query = """SELECT tb.TEAM_ID, p.fname, p.lname, p.position
                   FROM team_bar tb
                   JOIN players p ON tb.TEAM_ID = p.team_id
                   WHERE tb.TEAM_ID = 1"""
            cursor.execute(query)

            # Clear existing data in the Treeview
            for row in self.treeview.get_children():
                self.treeview.delete(row)

            # Fetch all the rows
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                self.treeview.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def sort_treeview(self, col):
        data = [(self.treeview.set(child, col), child) for child in self.treeview.get_children('')]
        data.sort()
        for i, item in enumerate(data):
            self.treeview.move(item[1], '', i)

class display_psg_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Insert Window")
        self.root.geometry("1550x800+0+0")

        # Variables
        self.var_Teamid = StringVar()
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_position = StringVar()

        original_bg = Image.open(r"../images/bgweq21.png")
        resized_bg = original_bg.resize((1400, 750), Image.BICUBIC)  # Set the desired width and height
        self.bg = ImageTk.PhotoImage(resized_bg)

        # Create a label and place the resized background image on it
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame and Treeview
        frame_border = Frame(self.root, bd=3, relief="ridge", bg="blue")         
        frame_border.place(x=230, y=250, width=910, height=280)

        # scroll_X = ttk.Scrollbar(frame_border, orient=VERTICAL)
        self.treeview = ttk.Treeview(frame_border, columns=('TEAM_ID', 'FIRST NAME', 'LAST NAME', 'POSITION'))
        # scroll_X.pack(side=RIGHT, fill=Y)
        # scroll_X.config(command=self.treeview.yview)

        # Configure column widths
        self.treeview.column('TEAM_ID', width=100, anchor='center')
        self.treeview.column('FIRST NAME', width=200, anchor='center')
        self.treeview.column('LAST NAME', width=200, anchor='center')
        self.treeview.column('POSITION', width=150, anchor='center')

        # Set the font for the entire Treeview
        font_size = 12  # Adjust the font size as needed
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', font_size, 'bold'))

        # Configure column headings
        for col in ('TEAM_ID', 'FIRST NAME', 'LAST NAME', 'POSITION'):
            self.treeview.heading(col, text=col, command=lambda c=col: self.sort_treeview(c), anchor='center')

        self.treeview['show'] = 'headings'

        self.treeview.pack(fill=BOTH, expand=1)

        # Button to refresh data
        refresh_button = Button(self.root, text="Refresh", command=self.display_data,font=("times new roman", 20, "bold"), borderwidth=4, fg="white",
                         bg="red", activeforeground="black", activebackground="red")
        refresh_button.place(x=600, y=610)
        # Display initial data
        self.display_data()

    def display_data(self):
        # Connect to the MySQL database
        conn = sqlite3.connect('AppData.db')

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Execute the SQL query
            query = """SELECT tb.TEAM_ID, p.fname, p.lname, p.position
                   FROM team_bar tb
                   JOIN players p ON tb.TEAM_ID = p.team_id
                   WHERE tb.TEAM_ID = 3"""
            cursor.execute(query)

            # Clear existing data in the Treeview
            for row in self.treeview.get_children():
                self.treeview.delete(row)

            # Fetch all the rows
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                self.treeview.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def sort_treeview(self, col):
        data = [(self.treeview.set(child, col), child) for child in self.treeview.get_children('')]
        data.sort()
        for i, item in enumerate(data):
            self.treeview.move(item[1], '', i)

class display_MATCHESSSS_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Insert Window")
        self.root.geometry("1550x800+0+0")

        # Variables
        self.var_Teamid = StringVar()
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_position = StringVar()

        # Load background image
        self.bg = ImageTk.PhotoImage(file=r"../images/MATCHES SCH.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame and Treeview
        frame_border = Frame(self.root, bd=3, relief="ridge", bg="blue")         
        frame_border.place(x=210, y=200, width=910, height=400)

        # scroll_X = ttk.Scrollbar(frame_border, orient=HORIZONTAL)
        self.treeview = ttk.Treeview(frame_border, columns=('MATCH_ID', 'DATE', 'VENUE', 'RESULT','HOMETEAM','AWAYTEAM'))

        # scroll_X.pack(side=BOTTOM, fill=X)
        # scroll_X.config(command=self.treeview.xview)

        # Configure column widths
        self.treeview.column('MATCH_ID', width=100, anchor='center')
        self.treeview.column('DATE', width=100, anchor='center')
        self.treeview.column('VENUE', width=100, anchor='center')
        self.treeview.column('RESULT', width=100, anchor='center')
        self.treeview.column('HOMETEAM', width=100, anchor='center')
        self.treeview.column('AWAYTEAM', width=100, anchor='center')

        # Set the font for the entire Treeview
        font_size = 12  # Adjust the font size as needed
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', font_size, 'bold'))

        # Configure column headings
        for col in ('MATCH_ID', 'DATE', 'VENUE','RESULT', 'HOMETEAM','AWAYTEAM'):
            self.treeview.heading(col, text=col, command=lambda c=col: self.sort_treeview(c), anchor='center')

        self.treeview['show'] = 'headings'

        self.treeview.pack(fill=BOTH, expand=1)

        # Button to refresh data
        refresh_button = Button(self.root, text="Refresh", command=self.display_data,font=("times new roman", 20, "bold"), borderwidth=4, fg="white",
                         bg="red", activeforeground="black", activebackground="red")
        refresh_button.place(x=600, y=610)
        # Display initial data
        self.display_data()

    def display_data(self):
        # Connect to the MySQL database
        conn = sqlite3.connect('AppData.db')

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Execute the SQL query
            query ="SELECT m.match_id, m.date_, m.venue, m.result, t1.team_name AS hometeam, t2.team_name AS awayteam FROM matches m JOIN team_bar t1 ON m.hometeam_id = t1.TEAM_ID JOIN team_bar t2 ON m.awayteam_id = t2.TEAM_ID ORDER BY m.match_id ";

            cursor.execute(query)

            # Clear existing data in the Treeview
            for row in self.treeview.get_children():
                self.treeview.delete(row)

            # Fetch all the rows
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                self.treeview.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def sort_treeview(self, col):
        data = [(self.treeview.set(child, col), child) for child in self.treeview.get_children('')]
        data.sort()
        for i, item in enumerate(data):
            self.treeview.move(item[1], '', i)

class display_RANK_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Insert Window")
        self.root.geometry("1550x800+0+0")

        # Variables
        self.var_Teamid = StringVar()
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_position = StringVar()

        # Load background image
        self.bg = ImageTk.PhotoImage(file=r"../images/STANDING.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)


        # Frame and Treeview
        frame_border = Frame(self.root, bd=3, relief="ridge", bg="blue")         
        frame_border.place(x=230, y=210, width=910, height=100)


        self.treeview = ttk.Treeview(frame_border, columns=('TEAM', 'WIN', 'DRAW', 'LOSE','POINTS'))

        # Configure column widths
        self.treeview.column('TEAM', width=100, anchor='center')
        self.treeview.column('WIN', width=100, anchor='center')
        self.treeview.column('DRAW', width=100, anchor='center')
        self.treeview.column('LOSE', width=100, anchor='center')
        self.treeview.column('POINTS', width=100, anchor='center')

        # Set the font for the entire Treeview
        font_size = 12  # Adjust the font size as needed
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', font_size, 'bold'))

        # Configure column headings
        for col in ('TEAM', 'WIN', 'DRAW','LOSE', 'POINTS'):
            self.treeview.heading(col, text=col, command=lambda c=col: self.sort_treeview(c), anchor='center')

        self.treeview['show'] = 'headings'

        self.treeview.pack(fill=BOTH, expand=1)

        # Button to refresh data
        refresh_button = Button(self.root, text="Refresh", command=self.display_data,font=("times new roman", 20, "bold"), borderwidth=4, fg="white",
                         bg="red", activeforeground="black", activebackground="red")
        refresh_button.place(x=610, y=390)

        # Display initial data
        self.display_data()

    def display_data(self):
        # Connect to the MySQL database
        conn = sqlite3.connect('AppData.db')

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Execute the SQL query
            query ='SELECT tb.TEAM_NAME, tr.win, tr.lose, tr.draw, tr.points FROM team_rank tr JOIN team_bar tb ON tr.TEAM_ID = tb.TEAM_ID ORDER BY tr.points DESC';
            cursor.execute(query)

            # Clear existing data in the Treeview
            for row in self.treeview.get_children():
                self.treeview.delete(row)

            # Fetch all the rows
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                self.treeview.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def sort_treeview(self, col):
        data = [(self.treeview.set(child, col), child) for child in self.treeview.get_children('')]
        data.sort()
        for i, item in enumerate(data):
            self.treeview.move(item[1], '', i)

class display_playerinfo_win:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Info")
        self.root.geometry("1550x800+0+0")

        # Variables
        self.var_Teamid = StringVar()
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_position = StringVar()

        # Load background image
        self.bg = ImageTk.PhotoImage(file=r"../images/PLAYER INFO.png")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)  # Set relwidth and relheight to cover the full window

        # Frame and Treeview
        frame_border = Frame(self.root, bd=3, relief="ridge", bg="blue")
        frame_border.place(x=170, y=200, width=1100, height=70)

        frame = Frame(self.root, bg='dark blue', bd=0, relief="solid", highlightbackground="blue", highlightthickness=3)
        frame.place(x=170, y=270, width=1100, height=200)

        self.treeview = ttk.Treeview(frame_border, columns=('PLAYER_ID', 'TEAM_ID', 'TEAM_NAME', 'FIRST_NAME','LAST_NAME','POSITON','JERSEY_NO'))

        # scroll_X.pack(side=BOTTOM, fill=X)
        # scroll_X.config(command=self.treeview.xview)

        # Configure column widths
        self.treeview.column('PLAYER_ID', width=100, anchor='center')
        self.treeview.column('TEAM_ID', width=100, anchor='center')
        self.treeview.column('TEAM_NAME', width=100, anchor='center')
        self.treeview.column('FIRST_NAME', width=100, anchor='center')
        self.treeview.column('LAST_NAME', width=100, anchor='center')
        self.treeview.column('POSITON', width=100, anchor='center')
        self.treeview.column('JERSEY_NO', width=100, anchor='center')

        # Set the font for the entire Treeview
        font_size = 10  # Adjust the font size as needed
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('arial', font_size),bg="red")

        # Configure column headings
        for rows in ('PLAYER_ID', 'TEAM_ID', 'TEAM_NAME','FIRST_NAME', 'LAST_NAME','POSITON','JERSEY_NO'):
            self.treeview.heading(rows, text=rows, command=lambda c=rows: self.sort_treeview(c), anchor='center')

        self.treeview['show'] = 'headings'

        self.treeview.pack(fill=BOTH, expand=1)

        # Button to refresh data
        # refresh_button = Button(frame, text="Refresh", command=self.search_data,font=("times new roman", 15, "bold"), borderwidth=4, fg="white",
        #                  bg="red", activeforeground="black", activebackground="red")
        # refresh_button.place(x=900, y=140)

        # Display initial data
        self.search_data()


        fname=Label(frame,text="FIRST NAME:-",font=("times new roman",15,"bold"),fg="yellow",bg='dark blue')
        fname.place(x=20,y=30)
        self.entry_fname = Entry(frame, textvariable=self.var_fname, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        self.entry_fname.place(x=20, y=60)

        lname=Label(frame,text="LAST NAME:-",font=("times new roman",15,"bold"),fg="yellow",bg='dark blue')
        lname.place(x=400,y=30)
        self.entry_lname = Entry(frame, textvariable=self.var_lname, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        self.entry_lname.place(x=400, y=60)


        Teamid=Label(frame,text="TEAM NAME:-",font=("times new roman",15,"bold"),fg="yellow",bg='dark blue')
        Teamid.place(x=800,y=30)
        self.entry_team = Entry(frame, textvariable=self.var_Teamid, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        self.entry_team.place(x=800, y=60)

        # Search button
        search_button = Button(frame, text="Search", command=self.search_data, font=("times new roman", 15, "bold"),
                               borderwidth=4, fg="white", bg="green", activeforeground="black", activebackground="green")
        search_button.place(x=20, y=140)



    def search_data(self):
            # Get user input
            search_fname = self.var_fname.get()
            search_lname = self.var_lname.get()
            search_team = self.var_Teamid.get()

            # Connect to the MySQL database
            conn = sqlite3.connect('AppData.db')

            # Create a cursor object to interact with the database
            cursor = conn.cursor()

            try:
                # Execute the SQL query with user input
                query = "SELECT p.player_id, p.team_id, t.TEAM_NAME, p.fname, p.lname, p.position, p.jerseyno " \
                        "FROM players p JOIN team_bar t ON p.team_id = t.TEAM_ID " \
                        "WHERE p.fname = ? AND p.lname = ? AND t.TEAM_NAME = ?"
                cursor.execute(query, (search_fname, search_lname, search_team))

                # Clear existing data in the Treeview
                for row in self.treeview.get_children():
                    self.treeview.delete(row)

                # Fetch all the rows
                rows = cursor.fetchall()

                # Insert data into the Treeview
                for row in rows:
                    self.treeview.insert('', 'end', values=row)

            except Exception as e:
                messagebox.showerror("Error", f"Error fetching data: {e}")

            finally:
                # Close the cursor and connection
                cursor.close()
                conn.close()

    def sort_treeview(self, rows):
        data = [(self.treeview.set(child, rows), child) for child in self.treeview.get_children('')]
        data.sort()
        for i, item in enumerate(data):
            self.treeview.move(item[1], '', i)

      

if __name__ == "__main__":
    main()
