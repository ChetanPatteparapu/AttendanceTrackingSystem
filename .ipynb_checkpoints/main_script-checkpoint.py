import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import *
# BELOW IMPORT IS TO HASH PASSWORDS
import hashlib
import os
import cv2
import csv

# FILETYPE IMPORT IS FOR CHECKING VALID IMAGE TYPES
import filetype

#LOG-IN PAGE
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # BORDER FRAME FOR LOGIN
        border = tk.LabelFrame(self, text='Login', bg='ivory', bd=10, font=('Arial', 20))
        border.pack(fill="both", expand="yes", padx=200, pady=100)
        
        # USERNAME LABEL AND USERNAME TEXTFIELD
        username_label = tk.Label(border, text="Username", font=("DejaVu Sans Mono", 15), bg='ivory')
        username_label.place(x=350, y=200)
        username_text = tk.Entry(border, width=30, bd=5)
        username_text.place(x=245, y=250)
        
        # PASSWORD LABEL AND PASSWORLD TEXTFIELD
        pwdLabel = tk.Label(border, text="Password", font=("DejaVu Sans Mono", 15), bg='ivory')
        pwdLabel.place(x=350, y=325)
        pwdText = tk.Entry(self, width=30, show="*", bd=5)
        pwdText.place(x=450, y=500)
        
        # FUNCTION TO VERFIFY THE PROVIDED CREDENTIALS
        def verify_user():
            user_name = username_text.get().strip()
            user_pwd = pwdText.get().strip()
            
            encoded_pwd = hashlib.md5(user_pwd.encode("utf")).hexdigest()
            
            try:
                with open("credentials.txt", "r") as file:
                    creds = file.readlines()
                    
                    found = False
                    
                    for pair in creds:
                        current_user, current_hash = pair.split(',')
                        current_user = current_user.strip()
                        current_hash = current_hash.strip()
                        
                        if user_name.__eq__(current_user) and encoded_pwd.__eq__(current_hash):
                            found = True
                            controller.show_frame(IndexPage)
                            break
                    
                    if found == False:
                        messagebox.showinfo("Error", "Sorry! Credentials didn't match!")
            except:
                messagebox.showinfo("Error", "Please enter correct information!")
        
        enter = tk.Button(border, text="Enter", font=("Arial", 15), command=verify_user)
        enter.place(x=300, y=450)
        
        signup_button = tk.Button(border, text="Sign-up", font=('Arial', 15), command=lambda: controller.show_frame(SignUp))
        signup_button.place(x=400, y=450)
        
class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        def save_credentials():
            user_name = username_text.get().strip()
            
            user_pwd = pwdText.get().strip()
            confirm_pwd = confirm_text.get().strip()
            
            if not user_pwd.__eq__(confirm_pwd) or len(user_name) < 1 or len(user_pwd) < 1:
                messagebox.showinfo("Error", "Passwords didn't match!")
                return
            
            if (user_exists(user_name)):
                messagebox.showinfo("Error", "Username already exists!")
                return
            
            encoded_pwd = hashlib.md5(user_pwd.encode("utf")).hexdigest()
            
            with open("credentials.txt", "a") as creds:
                creds.write(f"{user_name},{encoded_pwd}\n")
                messagebox.showinfo("Welcome","You are registered successfully!!")
        
        # BELOW METHOD IS TO CHECK IF THE USER ALREADY EXISTS IN THE FILE SYSTEM
        def user_exists(user_name):
            with open("credentials.txt", "r") as file:
                creds = file.readlines()
                    
                for pair in creds:
                    current_user, current_hash = pair.split(',')
                    if user_name.__eq__(current_user):
                        return True
                
                return False
            
        
        # BORDER FRAME
        border = tk.LabelFrame(self, text='Login', bg='ivory', bd=10, font=('Arial', 20))
        border.pack(fill="both", expand="yes", padx=200, pady=100)
        
        # USERNAME LABEL AND USERNAME TEXTFIELD
        username_label = tk.Label(border, text="Username", font=("DejaVu Sans Mono", 15), bg='ivory')
        username_label.place(x=350, y=100)
        username_text = tk.Entry(border, width=30, bd=5)
        username_text.place(x=245, y=150)
        
        # PASSWORD LABEL AND PASSWORLD TEXTFIELD
        pwdLabel = tk.Label(border, text="Password", font=("DejaVu Sans Mono", 15), bg='ivory')
        pwdLabel.place(x=350, y=225)
        pwdText = tk.Entry(self, width=30, show="*", bd=5)
        pwdText.place(x=450, y=400)
        
        # LABEL FOR CONFIRMING THE PASSWORD
        confirm_label = tk.Label(border, text=" Confirm Password", font=("DejaVu Sans Mono", 15), bg='ivory')
        confirm_label.place(x=320, y=350)
        confirm_text = tk.Entry(self, width=30, show="*", bd=5)
        confirm_text.place(x=450, y=525)
        
        # BELOW IS THE BUTTON TO FINISH THE UPLOAD
        register_button = tk.Button(border, text="Register", font=("DejaVu Sans Mono", 20), bg='ivory', command=save_credentials)
        register_button.place(x=600, y=500)
    
        # BUTTON
        back_button = tk.Button(self, text="Back", font=('Arial', 15), command=lambda: controller.show_frame(MainPage))
        back_button.place(x=1000, y=725)

# MENU PAGE
class IndexPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')
        
        # Below is the function that starts the recording
        # From the OS Module
        def start_script():
            os.system('python3 ATS.py')
        
        # Below is the button to start the recording
        start_rec_button = tk.Button(self, text="Start Recording", font=("Airal", 25), command=start_script)
        start_rec_button.place(x=500, y=250)
        
        # Below is the button to REGISTER A STUDENT
        register_button = tk.Button(self, text="Register Student", font=("Arial", 23), command=lambda: controller.show_frame(RegisterStudent))
        register_button.place(x=500, y=325)
        
        # Below is the button to REGISTER A STUDENT
        remove_student = tk.Button(self, text="Remove Student", font=("Arial", 23), command=lambda: controller.show_frame(RemoveStudent))
        remove_student.place(x=500, y=400)
        
        # Below is the button to REGISTER A STUDENT
        search_record = tk.Button(self, text="Search Record", font=("Arial", 25), command=lambda: controller.show_frame(SearchRecord))
        search_record.place(x=500, y=475)
        
        # BUTTON
        back_button = tk.Button(self, text="Back", font=('Arial', 15), command=lambda: controller.show_frame(MainPage))
        back_button.place(x=1000, y=725)

#LOG-IN PAGE
class RegisterStudent(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # BORDER FRAME FOR REGISTERING
        border = tk.LabelFrame(self, text='Registration', bg='ivory', bd=10, font=('Arial', 20))
        border.pack(fill="both", expand="yes", padx=200, pady=100)
        
        student_name_label = tk.Label(border, text="Student Name", font=("DejaVu Sans Mono", 15), bg='ivory')
        student_name_label.place(x=350, y=200)
        student_name_text = tk.Entry(border, width=30, bd=5)
        student_name_text.place(x=250, y=250)
        
        filepath = ""
        
        def open_file():
            global filepath
            # CHECK IF THE STUDENT'S NAME IS ENTERED
            if (len(student_name_text.get()) < 1):
                messagebox.showinfo("Error", "Please enter the student's name")
                return
            
            filepath = filedialog.askopenfilename()
            
            filepath_label = tk.Label(border, text=filepath, font=("DejaVu Sans Mono", 15), bg='ivory')
            filepath_label.place(x=250, y=350)
            
        def upload_image():
            student_name = student_name_text.get()
            global filepath
            
            # PATH WHERE YOU WANT TO SAVE THE IMAGE
            path = 'student_images'
            
            if len(filepath) < 1 or len(student_name) < 1:
                messagebox.showinfo("Error", "Please choose an image to continue!")
            
            extension = filepath.split(".")[1]
            
            # CHECK FOR STUDENT EXISTENCE
            if student_exists(student_name, path):
                messagebox.showinfo("Error", "Student Already Registered!")
                return
            
            if not filetype.is_image(filepath):
                messagebox.showinfo("Error", "Please upload a valid Image in JPG or PNG")
                return
                
            
            # OPEN THE IMAGE USING CV2 MODULE
            image = cv2.imread(filepath)
            
            
            # SAVE THE IMAGE ON STUDENT NAME OR STUDENT ID TO MAKE IT UNIQUE
            cv2.imwrite(os.path.join(path, f"{student_name}.{extension}"), image)
            
            messagebox.showinfo("Registraion Done", "Student Successfully Registered")
        
        def student_exists(student_name, path):
            registered_students = os.listdir(path)
            
            for student in registered_students:
                if student.startswith('.'):
                    continue
                
                # SPLIT AND PICK THE NAME
                name = student.split('.')[0]
                if name.__eq__(student_name):
                    return True
            
            return False
            
        
        # BELOW IS THE BUTTON TO CHOOSE THE IMAGE
        choose_button = tk.Button(border, text="choose image", font=("DejaVu Sans Mono", 15), bg='ivory', command=open_file)
        choose_button.place(x=335, y=300)
        
        # BELOW IS THE BUTTON TO FINISH THE UPLOAD
        register_button = tk.Button(border, text="Register", font=("DejaVu Sans Mono", 20), bg='ivory', command=upload_image)
        register_button.place(x=600, y=450)
        
        #Button to go back
        back_button = tk.Button(self, text="Back", font=('Arial', 15), command=lambda: controller.show_frame(IndexPage))
        back_button.place(x=1000, y=725)
        
class RemoveStudent(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # BORDER FRAME FOR REGISTERING
        border = tk.LabelFrame(self, text='Remove Student', bg='ivory', bd=10, font=('Arial', 20))
        border.pack(fill="both", expand="yes", padx=200, pady=100)
        
        # LABEL FOR TEXT BOX
        student_name_label = tk.Label(border, text="Student Name", font=("DejaVu Sans Mono", 15), bg='ivory')
        student_name_label.place(x=350, y=200)
        # TEXT BOX FOR STUDENT NAME
        student_name_text = tk.Entry(border, width=30, bd=5)
        student_name_text.place(x=250, y=250)
        
        def remove_student():
            student_name = student_name_text.get().lower()
            
            if len(student_name) < 1:
                messagebox.showinfo("Error", "Please enter the Student Name")
                return
            
            file_name = ""
            # BELOW IS THE DIRECTORY WHERE THE IMAGES ARE LOCATED FOR ENCODINGS
            directory = "student_images"
            images_list = os.listdir(directory)
            
            for image in images_list:
                image_name = image.title().split('.')[0].lower()
                
                if image_name.__eq__(student_name):
                    file_name = image.title()
                    
            
            if len(file_name) < 1:
                messagebox.showinfo("Error", "Name not found!")
            else:
                # BELOW IS THE FUNCTION TO REMOVE THE IMAGE
                os.remove(f"{directory}/{file_name}")
                messagebox.showinfo("Success", "Successfully Removed!")
        
        # BELOW IS THE BUTTON TO FINISH THE UPLOAD
        remove_button = tk.Button(border, text="Remove", font=("DejaVu Sans Mono", 20), bg='ivory', command=remove_student)
        remove_button.place(x=600, y=450)
        
        #Button to go back
        back_button = tk.Button(self, text="Back", font=('Arial', 15), command=lambda: controller.show_frame(IndexPage))
        back_button.place(x=1000, y=725)
        
class SearchRecord(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        def search_student():
            student_name = student_name_text.get()
            student_name = student_name.lower()
            
            if len(student_name) < 1 or len(filelist) < 1:
                messagebox.showinfo("Error", "Please enter a valid name")
                return
            
            selected_path = clicked.get()
            
            if not selected_path.__eq__(file_path):
                cache_students(selected_path)
            
            if student_name in entries:
                result = entries.get(student_name)
            else:
                result = "Not found"
            
            display_label = tk.Label(border, text=f"Time: {result}", font=("Arial", 15), bg='ivory')
            display_label.place(x=330, y=340)
           
        # BELOW FUNCTION IS TO DISPLAY THE CSV FILE IN FULL
        def display_record():
            if len(filelist) < 1:
                return
            
            selected_path = clicked.get()
            
            if not selected_path.__eq__(file_path):
                cache_students(selected_path)
                
            # NOW DISPLAY THE SELECTED CSV FILE
            with open(f"attendance_register/{selected_path}", newline = "") as record:
                attendance = csv.reader(record)
                
                i = 0
                for col in attendance:
                    j = 0
                    for row in col:
                        label = tk.Label(border, width = 10, height = 2, \
                               text = row, relief = tk.RIDGE)
                        label.grid(row = i, column = j)
                        j += 1
                    i += 1
        
        def cache_students(selected_path):
            global file_path
            entries.clear()
            
            with open(f"attendance_register/{selected_path}", 'r+') as f:
                current_register = f.readlines()
                
                for line in current_register:
                    if not line.__contains__(','):
                        continue
                        
                    pair = line.split(',')
                    entries[pair[0].lower()] = pair[1]
            
            file_path = selected_path
                    
            
        
        # BORDER FRAME FOR THE OPTIONS
        border = tk.LabelFrame(self, text='Search Record', bg='ivory', bd=10, font=('Arial', 20))
        border.pack(fill="both", expand="yes", padx=200, pady=100)
        
        # BELOW IS THE PATH FOR THE ATTENDANCE REGISTER
        directory = "attendance_register"
        
        # ADD EVERY FILE ON TO THE FILE-LIST FOR SELECTION
        filelist = [fname for fname in os.listdir(directory) if fname.endswith('.csv')]
        filelist.reverse()
        
        clicked = StringVar()
        if len(filelist) > 0:
            clicked.set(filelist[0])
        
        # DROP-DOWN MENU FOR CHOOSING
        drop = OptionMenu(border, clicked, *filelist)
        drop.place(x=330, y=100)
        
        # BELOW IS THE BUTTON FOR OPENING THE ATTENDANCE RECORD ON A GIVEN DAY
        open_button = tk.Button(border, text="Open", font=('Arial', 10), command=display_record)
        open_button.place(x=480, y=100)
        
        # LABEL FOR TEXT BOX
        student_name_label = tk.Label(border, text="Student Name", font=("DejaVu Sans Mono", 15), bg='ivory')
        student_name_label.place(x=350, y=200)
        # TEXT BOX FOR STUDENT NAME
        student_name_text = tk.Entry(border, width=30, bd=5)
        student_name_text.place(x=250, y=235)
        
        file_path = ""
        # DICTIONARY OR HASHMAP TO STORE STUDENTS INFORMATION
        entries = {}
        
        search_button = tk.Button(border, text="Search", font=('Arial', 15), command=search_student)
        search_button.place(x=350, y=280)
        
        #Button to go back
        back_button = tk.Button(self, text="Back", font=('Arial', 15), command=lambda: controller.show_frame(IndexPage))
        back_button.place(x=1000, y=725)

        
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        
        window.grid_rowconfigure(0, minsize = 800)
        window.grid_columnconfigure(0, minsize = 1200)
        
        self.frames = {}
        for F in (MainPage, SignUp, IndexPage, RegisterStudent, RemoveStudent, SearchRecord):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(MainPage)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")
            
app = Application()
app.maxsize(1200,800)
app.mainloop()