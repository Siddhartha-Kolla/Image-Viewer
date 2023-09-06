from tkinter import *
import customtkinter
from PIL import Image, ImageTk
from tkinter import filedialog
import sqlite3
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()

root.title("Image Storager")
root.iconbitmap("codemy.ico")
root.geometry("500x600")

logo = ImageTk.PhotoImage(Image.open("logo.png").resize((500,150)))
logo_lb = Label(master=root,image=logo,bd=0)
logo_lb.place(relx=0.5,rely=0.1,anchor=CENTER)

def login_opn():
    def writeTofile(data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
    root_log = customtkinter.CTkToplevel()
    root_log.grab_set()

    root_log.title("Image Storager")
    root_log.iconbitmap("codemy.ico")
    root_log.geometry("750x600")

    swi_var = customtkinter.StringVar(value="*")

    wel_log_lbl = customtkinter.CTkLabel(master=root_log, text="Login", text_font=("Comic Sans MS", 50))
    wel_log_lbl.place(relx=0.5, rely=0.075, anchor=CENTER)

    error_reg_lbl = customtkinter.CTkLabel(master=root_log, text="The passwords doesn't match",
                                           text_font=("Times New Roman", 13))
    error_reg_lbl.place(relx=0.5, rely=0.25, anchor=CENTER)

    usr_nm_ent = customtkinter.CTkEntry(master=root_log, placeholder_text="Username", height=40, width=400,
                                        text_font=("Helvetica", 20))
    usr_nm_ent.place(relx=0.5, rely=0.375, anchor=CENTER)

    pass_ent = customtkinter.CTkEntry(master=root_log, placeholder_text="Password", height=40, width=400,
                                      text_font=("Helvetica", 20), show="*")
    pass_ent.place(relx=0.5, rely=0.525, anchor=CENTER)

    pas_sh_sw = customtkinter.CTkSwitch(master=root_log, text="Show Password", variable=swi_var, onvalue="",
                                        offvalue="*", command=lambda: pass_ent.configure(show=swi_var.get()))
    pas_sh_sw.place(relx=0.5, rely=0.65, anchor=CENTER)

    def img_viw(data):
        writeTofile(data, "memory.png")
        root_log.destroy()
        img_viwer = customtkinter.CTkToplevel()
        img_viwer.grab_set()
        img_viwer.iconbitmap("codemy.ico")
        img_viwer.title("Image Storager")
        img = ImageTk.PhotoImage(Image.open("memory.png"))
        image = customtkinter.CTkLabel(img_viwer, image=img)
        image.pack()
        img_viwer.mainloop()

    def login():
        global img_viw_counter
        if usr_nm_ent.get() == "":
            error_reg_lbl.configure(text="Please enter an Username.", text_color="#e81e22")
            return None
        elif pass_ent.get() == "":
            error_reg_lbl.configure(text="Please enter a Password.", text_color="#e81e22")
            return None
        else:
            conn = sqlite3.connect("image_viewer.db")
            c = conn.cursor()

            c.execute("SELECT username FROM user_data")
            usr_nm = [i[0] for i in c.fetchall()]

            if usr_nm_ent.get() in usr_nm:
                c.execute(f"SELECT password FROM user_data where username = '{usr_nm_ent.get()}'")
                password = c.fetchone()[0]
                if password == pass_ent.get():
                    c.execute(f"SELECT picture FROM user_data where username = '{usr_nm_ent.get()}'")
                    img_viw(c.fetchone()[0])
                else:
                    error_reg_lbl.configure(text="Wrong Password! Please type a valid password.", text_color="#e81e22")
                    return None
            elif usr_nm_ent.get() not in usr_nm:
                error_reg_lbl.configure(text="Invalid Username! Please enter a valid Username.", text_color="#e81e22")
                return None

    log_btn = customtkinter.CTkButton(master=root_log, text="Login", text_font=("Verdana", 25), width=400, height=40,
                                      corner_radius=50, command=login)
    log_btn.place(relx=0.5, rely=0.81, anchor=CENTER)

    root_log.mainloop()
    os.remove("memory.png")

login_btn = customtkinter.CTkButton(master=root,text="Login",height=60,width=400,text_font=("Comic Sans MS",25),command=login_opn)
login_btn.place(relx=0.5,rely=0.4,anchor= CENTER)

def register_opn():
    root_reg = customtkinter.CTkToplevel()
    root_reg.grab_set()

    root_reg.title("Image Storager")
    root_reg.iconbitmap("codemy.ico")
    root_reg.geometry("900x600")

    switch_var = customtkinter.StringVar(value="*")
    img_data = ""

    def convertToBinaryData(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    wel_reg_lbl = customtkinter.CTkLabel(master=root_reg, text="Register", text_font=("Comic Sans MS", 50))
    wel_reg_lbl.place(relx=0.5, rely=0.075, anchor=CENTER)

    update_lbl = customtkinter.CTkLabel(master=root_reg, text="", text_font=("Times New Roman", 13))
    update_lbl.place(relx=0.5, rely=0.22, anchor=CENTER)

    usr_ent = customtkinter.CTkEntry(master=root_reg, placeholder_text="Username", height=40, width=400,
                                     text_font=("Helvetica", 20))
    usr_ent.place(relx=0.5, rely=0.325, anchor=CENTER)

    pas_ent = customtkinter.CTkEntry(master=root_reg, placeholder_text="Password", height=40, width=400,
                                     text_font=("Helvetica", 20), show=switch_var.get())
    pas_ent.place(relx=0.5, rely=0.435, anchor=CENTER)

    pas_rpt_ent = customtkinter.CTkEntry(master=root_reg, placeholder_text="Repeat Password", height=40, width=400,
                                         text_font=("Helvetica", 20), show=switch_var.get())
    pas_rpt_ent.place(relx=0.5, rely=0.545, anchor=CENTER)

    def fil_opn():
        file_typ = (
            ("Portable Network Graphics", "*.png"),
            ("JPG", "*.jpg")
        )
        root_reg.filename = filedialog.askopenfilename(initialdir="/", title="Choose your Image:", filetypes=file_typ)
        global img_data
        img_data = root_reg.filename

    fil_btn = customtkinter.CTkButton(master=root_reg, text="Choose Image", command=fil_opn)
    fil_btn.place(relx=0.375, rely=0.675, anchor=CENTER)

    def sp():
        pas_ent.configure(show=switch_var.get())
        pas_rpt_ent.configure(show=switch_var.get())

    pas_show_swi = customtkinter.CTkSwitch(master=root_reg, text="Show Passwords", variable=switch_var, onvalue="",
                                           offvalue="*", command=sp)
    pas_show_swi.place(relx=0.6, rely=0.675, anchor=CENTER)

    def submit():
        global img_data
        conn = sqlite3.connect("image_viewer.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists user_data(username text,password text,picture blob)""")
        conn.commit()
        c.execute("SELECT username FROM user_data")
        conn.commit()
        usr_nm = [i[0] for i in c.fetchall()]

        if usr_ent.get() == "":
            update_lbl.configure(text="Please enter a Username.", text_color="#e81e22")
            return None
        elif pas_ent.get() == "":
            update_lbl.configure(text="Please enter a password.", text_color="#e81e22")
            return None
        elif pas_ent.get() != pas_rpt_ent.get():
            update_lbl.configure(text="The passwords doesn't match. Please type your password correctly.",
                                 text_color="#e81e22")
            return None
        elif img_data == "":
            update_lbl.configure(text="File not chosen. Please Choose a file", text_color="#e81e22")
            return None
        elif usr_ent.get() in usr_nm:
            update_lbl.configure(text="Username already taken. Please enter another Username.", text_color="#e81e22")
            return None
        data_lst = (usr_ent.get(), pas_ent.get(), convertToBinaryData(img_data))
        c.execute("INSERT INTO user_data(username,password,picture) VALUES (?,?,?)", data_lst)
        conn.commit()
        update_lbl.configure(text="Succesfully created your profile", text_color="#06d65a")
        conn.close()

    sub_btn = customtkinter.CTkButton(master=root_reg, text="Submit", text_font=("Verdana", 25), width=400, height=50,
                                      command=submit)
    sub_btn.place(relx=0.5, rely=0.81, anchor=CENTER)

    root_reg.mainloop()

register_btn = customtkinter.CTkButton(master=root, text="Register", height=60, width=400, text_font=("Comic Sans MS", 25),fg_color="#212325",border_width=3.5,border_color="#1f6aa5",command=register_opn)
register_btn.place(relx=0.5, rely=0.6, anchor= CENTER)

right_lbl = customtkinter.CTkLabel(master=root,text="©2022 Siddhartha Kolla. All rights reserved")
right_lbl.place(relx=0.25,rely=0.98,anchor=CENTER)


root.mainloop()