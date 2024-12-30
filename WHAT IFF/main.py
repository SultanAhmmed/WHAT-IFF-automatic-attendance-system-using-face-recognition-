from customtkinter import CTk, CTkButton, CTkLabel, CTkImage
from tkinter import messagebox
import subprocess
import cv2
from PIL import Image
import os
from datetime import datetime
from database import fetch_student_photo, mark_attendance
from io import BytesIO
import numpy as np
import shutil
from TeacherAdmin import TeacherPanel
import login

class App:
    def __init__(self) -> None:
        self.main_window = CTk()
        self.main_window.geometry("800x520+350+100")
        self.main_window.resizable(False, False)
        self.main_window.title('Attendance System')
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.records_of_student_photo = fetch_student_photo()

        if self.records_of_student_photo is not None:
            self.featch_database(self.records_of_student_photo)


        self.attendence_button = CTkButton(
            self.main_window,
            text='Attendence',
            fg_color='#c97d0d',       
            hover_color='#001d35',     
            font=('Cascadia Code', 18, 'bold'),  
            text_color='white',        
            corner_radius=20,          
            command=self.attendence,
            anchor='center',
            height=45    
        )
        self.attendence_button.place(x=610, y=250)

        self.teacher_button = CTkButton(
            self.main_window,
            text='Teacher Panel →',
            fg_color='#307e04',       
            hover_color='#001d35',     
            font=('Cascadia Code', 18, 'bold'),  
            text_color='white',        
            corner_radius=20,          
            anchor='center',
            height=45,
            command=self.teacher_PL 
        )
        self.teacher_button.place(x=590, y=190)

        self.webcam_label = CTkLabel(self.main_window, text='', width=500, height=500)
        self.webcam_label.place(x=10, y=10)

        # Initialize face cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.add_webcam(self.webcam_label)

    def featch_database(self,records):
        for id ,name, photo_blob in records:
                # Convert the student photo to a numpy array
                img = self.convertBinary_image(photo_blob)
                
                # Save the student photo to the temporary directory
                student_img_path = os.path.join(self.db_dir, f'{id}_{name}.jpg')
                cv2.imwrite(student_img_path, img)
    
    def teacher_PL(self):
        # Create an instance of the login window
        login_window = login.LoginWindow(self.main_window)

        # Hide the main window while the login is happening
        self.main_window.withdraw()

        # Start the login window, it's using the same main loop as the root window
        self.main_window.wait_window(login_window.master)  # This will wait until login window is closed

        # Check if login was successful
        if login_window.get_result():
            # Proceed to Teacher Panel if login is successful
            self.teacher_admin_panel()
        else:
            # Show message if login failed
            messagebox.showerror("Error", "Login failed. Please try again.")
            self.main_window.deiconify()  # Show the main window again

    def teacher_admin_panel(self):
        # Create and display the Teacher Admin Panel
        app = TeacherPanel(self.main_window)
        app.window.protocol("WM_DELETE_WINDOW", lambda: self.on_teacher_panel_close(self.main_window, app))
        app.window.mainloop()

    def on_teacher_panel_close(self, root, app):
        app.window.destroy()
        root.deiconify()
        self.featch_database(self.records_of_student_photo)



    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        
        self._label = label
        self.process_webcam()
    
    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            self.most_recent_capture_arr = frame

            # Convert the frame to grayscale for face detection
            gray_frame = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

            # Initialize variables to find the largest face
            largest_face = None
            max_area = 0

            # Find the largest face based on area
            for (x, y, w, h) in faces:
                area = w * h  # Calculate area of the face
                if area > max_area:  # Check if this face is larger than the current largest
                    max_area = area
                    largest_face = (x, y, w, h)

            # Draw rectangle around the largest face if found
            if largest_face is not None:
                (x, y, w, h) = largest_face
                cv2.rectangle(self.most_recent_capture_arr, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Resize and convert to RGB for display
            self.resized_frame = cv2.resize(self.most_recent_capture_arr, (550, 412))
            img_ = cv2.cvtColor(self.resized_frame, cv2.COLOR_BGR2RGB)

            # Convert to PIL image and create CTkImage
            self.most_recent_capture_pil = Image.fromarray(img_)
            ctk_img = CTkImage(self.most_recent_capture_pil, size=(550, 412))

            # Update the label with the image
            self._label.configure(image=ctk_img)
            self._label.image = ctk_img

            # Call this method again after 20 ms
            self._label.after(20, self.process_webcam)

    def attendence(self):
        # Save the most recent capture image temporarily
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        try:
            # Run the face_recognition command with the temporary directory
            output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
            matched_names = []
            for line in output.splitlines():
                if "," in line:
                    _, name = line.split(",", 1)  # Split only on the first comma
                    matched_names.append(name.strip().replace("\\n'", '').strip())  # Clean up unwanted characters
            
            name = matched_names[0]
            if name != 'unknown_person' and  name != 'no_persons_found':
                id,name = matched_names[0].split('_')

            # print(id)
            if name == 'unknown_person':
                messagebox.showwarning('Warning','You are not in Database!')
            elif name == 'no_persons_found':
                messagebox.showerror('Error','Remove cover from your face!')
            else:
                messagebox.showinfo('Greeting',f'Hello, {name}!')
                # print(name)
                current_date = datetime.now().strftime("%Y-%m-%d")
                try:
                    mark_attendance(id, name, current_date)
                except:
                    messagebox.showerror('Unable to update database')


        except subprocess.CalledProcessError as e:
            print("Error in face recognition:", e)

        os.remove(unknown_img_path)

    def convertBinary_image(self, photo_blob):
        image_bytes = BytesIO(photo_blob)
        # Open the image using PIL and convert to OpenCV format
        img = Image.open(image_bytes).convert('RGB')
        return np.array(img)

    def start(self):
        self.main_window.mainloop()
        if os.path.exists(self.db_dir):
            shutil.rmtree(self.db_dir)


# if __name__ == "__main__":
#     app = App()
#     app.start()

    