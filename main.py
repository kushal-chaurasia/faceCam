#################################################
#                   IMPORTS                     #
#################################################
import datetime
import glob
import os
import smtplib
import sqlite3
import time
import tkinter as tk
import tkinter.simpledialog as tsd
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox as mess
from tkinter import ttk

import cv2
import numpy as np
import pandas as pd
from PIL import Image


#################################################
#                   FUNCTIONS                   #
#################################################


def check_files():
    dir1 = os.path.isdir("resources")
    dir2 = os.path.isdir("resources\\TrainingImages")
    file1 = os.path.isfile("resources\\database.db")
    file2 = os.path.isfile("resources\\haarcascade_frontalface_default.xml")
    file3 = os.path.isfile("resources\\Trainer.yml")
    if dir1:
        pass
    else:
        os.mkdir("resources")
    if dir2:
        pass
    else:
        os.mkdir("resources\\TrainingImages")
    if file1:
        pass
    else:
        con = sqlite3.connect('resources\\database.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE admin (cp_pass TEXT, smtp_email TEXT, smtp_pass TEXT)")
        cur.execute("CREATE TABLE student_attendance (id INTEGER, name TEXT, date TEXT, time TEXT)")
        cur.execute(
            "CREATE TABLE student_details (serial_no INTEGER, id INTEGER, name TEXT, PRIMARY KEY(serial_no AUTOINCREMENT))")
        cur.close()
        con.commit()
        con.close()
    if file2:
        pass
    else:
        mess.showinfo(title='Error!', message='haarcascade_frontalface_default.xml missing!')
        window.destroy()
    if file3:
        pass
    else:
        mess.showinfo(title='Error!', message='Trainer.yml missing!')
        train_images()


def check_admin():
    cursors.execute("SELECT * FROM admin")
    data_row = cursors.fetchone()
    if data_row is None:
        mess.showinfo(title='Message!', message='No admin password found in database!')
        create_admin_pass_gui()
    else:
        pass


def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


# /////////////////////////////////////////////////////////// #
#                    NEW CPANEL PASSWORD                      #
# /////////////////////////////////////////////////////////// #


global register_admin_pass_gui
global cre_gui_cp_pass


def create_admin_pass_gui():
    global register_admin_pass_gui
    register_admin_pass_gui = tk.Tk()
    register_admin_pass_gui.geometry("460x80")
    register_admin_pass_gui.resizable(False, False)
    register_admin_pass_gui.title("New Admin Password")
    register_admin_pass_gui.configure(background="white")
    lbl4 = tk.Label(register_admin_pass_gui, text='   Enter New C Panel Password', bg='white',
                    font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global cre_gui_cp_pass
    cre_gui_cp_pass = tk.Entry(register_admin_pass_gui, width=25, fg="black", relief='solid',
                               font=('times', 12, ' bold '),
                               show='*')
    cre_gui_cp_pass.place(x=235, y=10)
    cancel = tk.Button(register_admin_pass_gui, text="Cancel", command=register_admin_pass_gui.destroy, fg="black",
                       bg="red", height=1,
                       width=25, activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=230, y=45)
    save1 = tk.Button(register_admin_pass_gui, text="Save", command=create_admin_pass, fg="black", bg="#3ece48",
                      height=1,
                      width=25,
                      activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=30, y=45)
    register_admin_pass_gui.mainloop()


def create_admin_pass():
    local_new_cp_pass = cre_gui_cp_pass.get()
    if local_new_cp_pass == "":
        mess.showinfo(title='Error!', message='Password field cannot be blank!')
        create_admin_pass_gui()
    else:
        cursors.execute("INSERT INTO admin (cp_pass) VALUES (?)", [local_new_cp_pass])
        connection.commit()
        register_admin_pass_gui.destroy()
        mess.showinfo(title='Password Registered', message='New password was registered successfully!')


# /////////////////////////////////////////////////////////// #
#                   CHANGE CPANEL PASSWORD                    #
# /////////////////////////////////////////////////////////// #


global change_cp_pass_gui_form
global old_c_pass
global new_c_pass
global cnf_new_c_pass


def change_cp_pass_gui():
    global change_cp_pass_gui_form
    change_cp_pass_gui_form = tk.Tk()
    change_cp_pass_gui_form.geometry("460x160")
    change_cp_pass_gui_form.resizable(False, False)
    change_cp_pass_gui_form.title("Change Control Panel Password")
    change_cp_pass_gui_form.configure(background="white")
    lbl4 = tk.Label(change_cp_pass_gui_form, text='   Enter C Panel Password:', bg='white',
                    font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global old_c_pass
    old_c_pass = tk.Entry(change_cp_pass_gui_form, width=25, fg="black", relief='solid', font=('times', 12, ' bold '),
                          show='*')
    old_c_pass.place(x=220, y=10)
    lbl5 = tk.Label(change_cp_pass_gui_form, text='   Enter New Password:', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new_c_pass
    new_c_pass = tk.Entry(change_cp_pass_gui_form, width=25, fg="black", relief='solid', font=('times', 12, ' bold '),
                          show='*')
    new_c_pass.place(x=220, y=45)
    lbl6 = tk.Label(change_cp_pass_gui_form, text='   Confirm New Password:', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global cnf_new_c_pass
    cnf_new_c_pass = tk.Entry(change_cp_pass_gui_form, width=25, fg="black", relief='solid',
                              font=('times', 12, ' bold '), show='*')
    cnf_new_c_pass.place(x=220, y=80)
    cancel = tk.Button(change_cp_pass_gui_form, text="Cancel", command=change_cp_pass_gui_form.destroy, fg="black",
                       bg="red", height=1, width=25,
                       activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=230, y=120)
    save1 = tk.Button(change_cp_pass_gui_form, text="Save", command=change_cp_pass, fg="black", bg="#3ece48", height=1,
                      width=25,
                      activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=30, y=120)
    change_cp_pass_gui_form.mainloop()


def change_cp_pass():
    cursors.execute("SELECT * FROM admin")  # select query
    data_row = cursors.fetchone()
    if data_row is None:
        mess.showinfo(title='Message!', message='No admin password found in database!')
        create_admin_pass_gui()
    else:
        local_old_c_pass = (old_c_pass.get())
        local_new_c_pass = (new_c_pass.get())
        local_cnf_new_c_pass = (cnf_new_c_pass.get())
        if local_old_c_pass in data_row:
            if local_new_c_pass == local_cnf_new_c_pass:
                cursors.execute("UPDATE admin SET cp_pass = (?) WHERE cp_pass = (?)",
                                [local_new_c_pass, local_old_c_pass])
            else:
                mess.showinfo(title='Error', message='Confirm new password again!!!')
                return
        else:
            mess.showinfo(title='Wrong Password', message='Please enter correct old password.')
            return
        mess.showinfo(title='Password Changed', message='Password changed successfully!!')
    change_cp_pass_gui_form.destroy()
    connection.commit()


# /////////////////////////////////////////////////////////// #
#                   CHANGE EMAIL/PASSWORD                     #
# /////////////////////////////////////////////////////////// #


global email_pass_gui_form
global change_email_cp_pass
global new_admin_email
global new_admin_email_password


def change_admin_email_pass_gui():
    global email_pass_gui_form
    email_pass_gui_form = tk.Tk()
    email_pass_gui_form.geometry("460x160")
    email_pass_gui_form.resizable(False, False)
    email_pass_gui_form.title("Change Admin Email/Password")
    email_pass_gui_form.configure(background="white")
    lbl4 = tk.Label(email_pass_gui_form, text='   Enter C Panel Password', bg='white', font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global change_email_cp_pass
    change_email_cp_pass = tk.Entry(email_pass_gui_form, width=25, fg="black", relief='solid',
                                    font=('times', 12, ' bold '),
                                    show='*')
    change_email_cp_pass.place(x=220, y=10)
    lbl5 = tk.Label(email_pass_gui_form, text='   Enter New Admin Email', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new_admin_email
    new_admin_email = tk.Entry(email_pass_gui_form, width=25, fg="black", relief='solid', font=('times', 12, ' bold '))
    new_admin_email.place(x=220, y=45)
    lbl6 = tk.Label(email_pass_gui_form, text='   Enter New Admin Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global new_admin_email_password
    new_admin_email_password = tk.Entry(email_pass_gui_form, width=25, fg="black", relief='solid',
                                        font=('times', 12, ' bold '),
                                        show='*')
    new_admin_email_password.place(x=220, y=80)
    cancel = tk.Button(email_pass_gui_form, text="Cancel", command=email_pass_gui_form.destroy, fg="black", bg="red",
                       height=1, width=25,
                       activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=230, y=120)
    save1 = tk.Button(email_pass_gui_form, text="Save", command=save_admin_email_pass, fg="black", bg="#3ece48",
                      height=1, width=25,
                      activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=30, y=120)
    email_pass_gui_form.mainloop()


def save_admin_email_pass():
    cursors.execute("SELECT * FROM admin")
    data_row = cursors.fetchone()
    if data_row is None:
        mess.showinfo(title='Message!', message='No admin password found in database!')
        while True:
            email_pass_gui_form.destroy()
            new_pass = tsd.askstring('New Password!', 'Please enter a new password below', show='*')
            if new_pass == "":
                mess.showinfo(title='Error!', message='Password field cannot be blank!')
            else:
                cursors.execute("INSERT INTO admin (cp_pass) VALUES (?)", [new_pass])  # insert query
                connection.commit()
                mess.showinfo(title='Password Registered', message='New password was registered successfully!')
                return
    else:
        local_admin_cp_pass = change_email_cp_pass.get()
        local_new_admin_email = new_admin_email.get()
        local_new_admin_pass = new_admin_email_password.get()
        if local_admin_cp_pass in data_row:
            cursors.execute("UPDATE admin SET smtp_email  = (?), smtp_pass = (?) WHERE cp_pass = (?)",
                            [local_new_admin_email, local_new_admin_pass, local_admin_cp_pass])  # insert query
        else:
            mess.showinfo(title='Wrong Password', message='Please enter correct c_panel password.')
            return
        mess.showinfo(title='Success!', message='New Admin Email/Password registered successfully!!')
    email_pass_gui_form.destroy()
    connection.commit()


# /////////////////////////////////////////////////////////// #
#                       DELETE DATABASE                       #
# /////////////////////////////////////////////////////////// #


global delete_db_gui
global del_gui_cp_pass


def delete_database_gui():
    global delete_db_gui
    delete_db_gui = tk.Tk()
    delete_db_gui.geometry("460x80")
    delete_db_gui.resizable(False, False)
    delete_db_gui.title("Delete Database")
    delete_db_gui.configure(background="white")
    lbl4 = tk.Label(delete_db_gui, text='   Enter C Panel Password', bg='white', font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    global del_gui_cp_pass
    del_gui_cp_pass = tk.Entry(delete_db_gui, width=25, fg="black", relief='solid', font=('times', 12, ' bold '),
                               show='*')
    del_gui_cp_pass.place(x=220, y=10)
    cancel = tk.Button(delete_db_gui, text="Cancel", command=delete_db_gui.destroy, fg="black", bg="red", height=1,
                       width=25, activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=230, y=45)
    save1 = tk.Button(delete_db_gui, text="Delete", command=delete_database, fg="black", bg="#3ece48", height=1,
                      width=25,
                      activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=30, y=45)
    delete_db_gui.mainloop()


def delete_database():
    cursors.execute("SELECT * FROM admin")
    data_row = cursors.fetchone()
    if data_row is None:
        mess.showinfo(title='Message!', message='No admin password found in database!')
        new_pass = tsd.askstring('New Password!', 'Please enter a new password below', show='*')
        if new_pass == "":
            mess.showinfo(title='Error!', message='Password field cannot be blank!')
        else:
            cursors.execute("INSERT INTO admin (cp_pass) VALUES (?)", [new_pass])
            mess.showinfo(title='Password Registered', message='New password was registered successfully!')
            return
    else:
        local_admin_cp_pass = del_gui_cp_pass.get()
        if local_admin_cp_pass in data_row:
            cursors.execute("DELETE FROM admin")
            cursors.execute("DELETE FROM sqlite_sequence")
            cursors.execute("DELETE FROM student_attendance")
            cursors.execute("DELETE FROM student_details")
            os.remove('resources//Trainer.yml')
            attendance_list = glob.glob('resources/Attendance-*.csv', recursive=True)
            for attendance in attendance_list:
                os.remove(attendance)
            images_list = glob.glob('resources/TrainingImages/*.jpg', recursive=True)
            for images in images_list:
                os.remove(images)
        else:
            mess.showinfo(title='Wrong Password', message='Please enter correct c_panel password.')
            return
        mess.showinfo(title='Success!', message='Database deleted successfully!!')
    delete_db_gui.destroy()
    connection.commit()


# /////////////////////////////////////////////////////////// #
#                       CONTACT  US                           #
# /////////////////////////////////////////////////////////// #


def contact_us():
    mess.showinfo(title='Contact us', message="Please contact us on : 'kushal28feb97@gmail.com' ")


# /////////////////////////////////////////////////////////// #
#                       SAVE PROFILE                          #
# /////////////////////////////////////////////////////////// #


global sv_profile_gui
global sv_cp_pass


def save_profile_gui():
    cursors.execute("SELECT * FROM admin")
    data_row = cursors.fetchone()
    if data_row is None:
        mess.showinfo(title='Message!', message='No admin password found in database!')
        register_admin_pass_gui()
    else:
        global sv_profile_gui
        sv_profile_gui = tk.Tk()
        sv_profile_gui.geometry("460x80")
        sv_profile_gui.resizable(False, False)
        sv_profile_gui.title("Save Profile")
        sv_profile_gui.configure(background="white")
        lbl4 = tk.Label(sv_profile_gui, text='   Enter C Panel Password', bg='white', font=('times', 12, ' bold '))
        lbl4.place(x=10, y=10)
        global sv_cp_pass
        sv_cp_pass = tk.Entry(sv_profile_gui, width=25, fg="black", relief='solid', font=('times', 12, ' bold '),
                              show='*')
        sv_cp_pass.place(x=220, y=10)
        cancel = tk.Button(sv_profile_gui, text="Cancel", command=sv_profile_gui.destroy, fg="black", bg="red",
                           height=1,
                           width=25, activebackground="white", font=('times', 10, ' bold '))
        cancel.place(x=230, y=45)
        save1 = tk.Button(sv_profile_gui, text="Save", command=save_profile, fg="black", bg="#3ece48", height=1,
                          width=25,
                          activebackground="white", font=('times', 10, ' bold '))
        save1.place(x=30, y=45)
        sv_profile_gui.mainloop()


def save_profile():
    cursors.execute("SELECT * FROM admin")
    data_row = cursors.fetchone()
    if data_row is None:
        mess.showinfo(title='Message!', message='No admin password found in database!')
        new_pass = tsd.askstring('New Password!', 'Please enter a new password below', show='*')
        if new_pass == "":
            mess.showinfo(title='Error!', message='Password field cannot be blank!')
        else:
            cursors.execute("INSERT INTO admin (cp_pass) VALUES (?)", [new_pass])  # insert query
            mess.showinfo(title='Password Registered', message='New password was registered successfully!')
            return
    else:
        while True:
            local_admin_cp_pass = sv_cp_pass.get()
            if local_admin_cp_pass in data_row:
                train_images()
                mess.showinfo(title='Success!', message='Record inserted successfully!')
                break
            elif local_admin_cp_pass == "":
                mess.showinfo(title='Error!', message='Password field cannot be blank!')
                break
            else:
                mess.showinfo(title='Error!', message='Invalid password!')
                break
    sv_profile_gui.destroy()
    connection.commit()


# /////////////////////////////////////////////////////////// #
#                       CLEAR BUTTONS                         #
# /////////////////////////////////////////////////////////// #


def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


# /////////////////////////////////////////////////////////// #
#                       SAVE PROFILE                          #
# /////////////////////////////////////////////////////////// #


def take_images():
    textfield1_id = (txt.get())
    textfield1_name = (txt2.get())
    if (textfield1_name.isalpha()) or (' ' in textfield1_name):
        cursors.execute("SELECT id FROM student_details WHERE id = (?)", [textfield1_id])
        data_row = cursors.fetchone()
        if data_row is None:
            cursors.execute("INSERT INTO student_details (id,name) VALUES (?,?)", [textfield1_id, textfield1_name])
            cursors.execute("SELECT * FROM student_details WHERE id = (?)", [textfield1_id])
            inserted_data = cursors.fetchall()
            for data in inserted_data:
                cam = cv2.VideoCapture(0)
                harcascade_path = "resources\\haarcascade_frontalface_default.xml"
                detector = cv2.CascadeClassifier(harcascade_path)
                sample_num = 0
                while True:
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        sample_num = sample_num + 1
                        cv2.imwrite(
                            "resources\\TrainingImages\ " + str(data[2]) + "." + str(data[0]) + "." + str(
                                data[1]) + '.' + str(
                                sample_num) + ".jpg",
                            gray[y:y + h, x:x + w])
                        cv2.imshow('Taking Images', img)
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    elif sample_num > 100:
                        break
                cam.release()
                cv2.destroyAllWindows()
                res = "Images Taken for ID : " + textfield1_id
                message1.configure(text=res)
                mess.showinfo(title='Success!', message='Id registered!')
        else:
            mess.showinfo(title='Error!', message='Id already registered!')
    else:
        if not textfield1_name.isalpha():
            res = "Invalid Name!"
            message.configure(text=res)
    connection.commit()


# /////////////////////////////////////////////////////////// #
#                       CAPTURE FACES                         #
# /////////////////////////////////////////////////////////// #


def train_images():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ID = get_images_and_labels("resources\\TrainingImages")
    # noinspection PyBroadException
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess.showinfo(title='Error!', message='No data found! Please register someone first!')
        return
    recognizer.save("resources\\Trainer.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    cursors.execute("SELECT * FROM student_details")
    count_rows = cursors.fetchall()
    message.configure(text='Total number of registrations  : ' + str(len(count_rows)))
    connection.commit()


def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in image_paths:
        pil_image = Image.open(imagePath).convert('L')
        image_np = np.array(pil_image, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(image_np)
        Ids.append(ID)
    return faces, Ids


# /////////////////////////////////////////////////////////// #
#                       TAKE ATTENDANCE                       #
# /////////////////////////////////////////////////////////// #


iid_count = 0


def track_images():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("resources\\Trainer.yml")
    harcascade_path = "resources\\haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(harcascade_path)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    cursors.execute("SELECT * FROM student_details")
    fetch_one = cursors.fetchone()
    if fetch_one is None:
        mess.showinfo(title='Error!', message='Please register student profile before taking attendance!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    else:
        stu_id = str
        stu_name = str
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf < 50:
                    cursors.execute("SELECT name,id FROM student_details WHERE serial_no = (?)", [serial])
                    fetch_data = cursors.fetchone()
                    stu_id = fetch_data[1]
                    stu_name = fetch_data[0]
                else:
                    pass
                cv2.putText(im, stu_name, (x, y + h), font, 1, (255, 255, 255), 2)
            cv2.imshow('Taking Attendance', im)
            if cv2.waitKey(1) == ord('q'):
                break
        cursors.execute("INSERT INTO student_attendance VALUES (?,?,?,?)",
                        [stu_id, stu_name, date, timestamp])
        global iid_count
        tv.insert(parent='', index='end', iid=iid_count, text=stu_id, values=(stu_name, date, timestamp))
        iid_count += 1
        connection.commit()
        cam.release()
        cv2.destroyAllWindows()


# /////////////////////////////////////////////////////////// #
#                       EMAIL ATTENDANCE                      #
# /////////////////////////////////////////////////////////// #


def email_attendance():
    sql = "SELECT * FROM student_attendance"
    df = pd.read_sql_query(sql, connection)
    df.to_csv('resources\\Attendance-' + date + '.csv')
    cursors.execute("SELECT smtp_email, smtp_pass FROM admin")
    fetch_one = cursors.fetchone()
    if fetch_one is None:
        mess.showinfo(title='Error!', message='No admin password found!')
    elif fetch_one[0] is None:
        mess.showinfo(title='Error!', message='No admin email found!')
    elif fetch_one[1] is None:
        mess.showinfo(title='Error!', message='No admin password found!')
    else:
        smtp_email = fetch_one[0]
        smtp_password = fetch_one[1]
        to_address = tsd.askstring('Email Attendance!', 'Please enter a email address below (eg: demo1234@gmail.com) :')
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = to_address
        msg['Subject'] = ('Attendance-' + date + '.csv')
        body = 'Face Recognition Based Attendance System\nAttendance-' + date + '.csv'
        msg.attach(MIMEText(body, 'plain'))
        filename = ('Attendance-' + date + '.csv')
        attachment = open('resources\\Attendance-' + date + '.csv', 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(smtp_email, smtp_password)
        text = msg.as_string()
        s.sendmail(smtp_email, to_address, text)
        s.quit()
        mess.showinfo(title='Success!', message='Attendance emailed to : ' + to_address)
    connection.commit()


# /////////////////////////////////////////////////////////// #
#                       CLOSING PROGRAM                       #
# /////////////////////////////////////////////////////////// #


def end():
    if mess.askokcancel("Quit", "Do you want to quit?"):
        connection.commit()
        cursors.close()
        connection.close()
        window.destroy()


#################################################
#                   USED STUFFS                 #
#################################################
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }

#################################################
#                  GUI FRONT-END                #
#################################################
window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#00aeff")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#00aeff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System", fg="white", bg="#262523", width=55,
                    height=1, font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |  ", fg="orange", bg="#262523", width=55,
                 height=1, font=('times', 18, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="orange", bg="#262523", width=55, height=1, font=('times', 18, ' bold '))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",
                 bg="#3ece48", font=('times', 17, ' bold '))
head2.grid(row=0, column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",
                 bg="#3ece48", font=('times', 17, ' bold '))
head1.place(x=0, y=0)

lbl = tk.Label(frame2, text="Enter ID", width=20, height=1, fg="black", bg="#00aeff", font=('times', 17, ' bold '))
lbl.place(x=80, y=55)

txt = tk.Entry(frame2, width=32, fg="black", font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name", width=20, fg="black", bg="#00aeff", font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2, width=32, fg="black", font=('times', 15, ' bold '))
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile", bg="#00aeff", fg="black", width=39, height=1,
                    activebackground="yellow", font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="", bg="#00aeff", fg="black", width=39, height=1, activebackground="yellow",
                   font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Today's attendance:", width=20, fg="black", bg="#00aeff", height=1,
                font=('times', 17, ' bold '))
lbl3.place(x=100, y=110)

#################################################
#                   STARTUP                     #
#################################################


check_files()
connection = sqlite3.connect('resources\\database.db')
global cursors
# noinspection PyRedeclaration
cursors = connection.cursor()
check_admin()
cursors.execute("SELECT * FROM student_details")
rows = cursors.fetchall()
message.configure(text='Total number of registrations  : ' + str(len(rows)))

#################################################
#                   MENUBAR                     #
#################################################


menubar = tk.Menu(window, relief='ridge')

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change C Panel Password', command=change_cp_pass_gui)
filemenu.add_command(label='Change Admin Email/Password', command=change_admin_email_pass_gui)
filemenu.add_command(label='Delete Database', command=delete_database_gui)
menubar.add_cascade(label='Admin', font=('times', 29, ' bold '), menu=filemenu)

filemenu2 = tk.Menu(menubar, tearoff=0)
filemenu2.add_command(label='Contact Us', command=contact_us)
filemenu2.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('times', 29, ' bold '), menu=filemenu2)

#################################################
#           TREEVIEW ATTENDANCE TABLE           #
#################################################


tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'))
tv.column('#0', width=82)
tv.column('name', width=130)
tv.column('date', width=133)
tv.column('time', width=133)
tv.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=4)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

#################################################
#                   SCROLLBAR                   #
#################################################


scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)

#################################################
#                   BUTTONS                     #
#################################################


clearButton = tk.Button(frame2, text="Clear", command=clear, fg="black", bg="#ea2a2a", width=11,
                        activebackground="white", font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2, fg="black", bg="#ea2a2a", width=11,
                         activebackground="white", font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)
takeImg = tk.Button(frame2, text="Take Images", command=take_images, fg="white", bg="blue", width=34, height=1,
                    activebackground="white", font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=save_profile_gui, fg="white", bg="blue", width=34, height=1,
                     activebackground="white", font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=track_images, fg="black", bg="yellow", width=35, height=1,
                     activebackground="white", font=('times', 15, ' bold '))
trackImg.place(x=30, y=50)
quitWindow = tk.Button(frame1, text="Quit", command=end, fg="black", bg="red", width=35, height=1,
                       activebackground="white", font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)
emailWindow = tk.Button(frame1, text="Email Attendance", command=email_attendance, fg="black", bg="orange", width=35,
                        height=1,
                        activebackground="white", font=('times', 15, ' bold '))
emailWindow.place(x=30, y=500)


#################################################
#                      END                      #
#################################################


window.configure(menu=menubar)
window.protocol("WM_DELETE_WINDOW", end)
window.mainloop()


#################################################
