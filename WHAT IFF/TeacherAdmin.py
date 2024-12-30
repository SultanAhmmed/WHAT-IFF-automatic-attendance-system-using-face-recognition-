from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox, filedialog
import cv2
import attendance_app
import database  # Import the database functions
import io

class TeacherPanel():
    def __init__(self, master=None)-> None:
        # self.window = CTk()
        self.window = CTkToplevel()
        self.window.geometry('1100x650+100+50')
        self.window.resizable(0, 0)
        self.window.title('Teacher Panel')
        self.window.configure(fg_color='#161C30')

        self.cap = None
        self.captured_image = None

        # Set up GUI elements
        self.setup_gui()
        self.treeview_data()
    def setup_gui(self):

        self.image = CTkImage(Image.open('cover.jpeg'), size=(1100, 158))
        logoLabel = CTkLabel(self.window, image=self.image, text='')
        logoLabel.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=0, pady=10)

        # Left Frame (Input Data Section)
        leftFrame = CTkFrame(self.window, fg_color='#161C30')
        leftFrame.grid(row=1, column=0, sticky='ns', padx=10, pady=(20, 10))

        self.idEntry = self.create_entry(leftFrame, 'Std Id', 0)
        self.nameEntry = self.create_entry(leftFrame, 'Name', 1)
        self.phoneEntry = self.create_entry(leftFrame, 'Phone', 2)

        self.DeptBox = self.create_combo_box(leftFrame, 'Dept', 3, ['CSE', 'EEE', 'BBA', 'English', 'MAS'])
        self.genderBox = self.create_combo_box(leftFrame, 'Gender', 4, ['Male', 'Female'])

        choose_photo_button = CTkButton(leftFrame, text='Choose Photo', font=('Cascadia Code', 14, 'bold'), width=120, command=self.choose_photo)
        choose_photo_button.grid(row=5, column=0, padx=10, pady=20)

        self.photo_label = CTkLabel(leftFrame, text="")
        self.photo_label.grid(row=5, column=1, padx=10, pady=20)

        # Right Frame (Student Data Table)
        rightFrame = CTkFrame(self.window, fg_color='#161C30')
        rightFrame.grid(row=1, column=1, sticky='ns', padx=10, pady=10)

        # Widgets
        self.searchBox = CTkComboBox(rightFrame, values=["Search By", "ID", "Name", "Phone"], width=120, font=('Cascadia Code', 15, 'bold'), state='readonly')
        self.searchBox.set("Search By")
        self.searchBox.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="w")

        self.searchEntry = CTkEntry(rightFrame, font=('Cascadia Code', 15, 'bold'), width=150)
        self.searchEntry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

        searchButton = CTkButton(rightFrame, text="Search", font=('Cascadia Code', 15), width=100, command=self.search_student)
        searchButton.grid(row=0, column=2, padx=(0, 10), pady=(10, 0), sticky="w")

        filterButton = CTkButton(rightFrame, text="History", font=('Cascadia Code', 15), width=100, command=self.filter_student)
        filterButton.grid(row=0, column=3, padx=(0, 0), pady=(10, 0), sticky="w")


        # Treeview (Student Data Table)
        self.tree = ttk.Treeview(rightFrame, columns=('ID', 'Name', 'Phone', 'Dept', 'Gender', 'Attendance'), show='headings', height=15)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Dept', text='Dept')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Attendance', text='Attendance')

        # Set column widths to make sure they don't overflow
        self.tree.column('ID', width=60)
        self.tree.column('Name', width=150)
        self.tree.column('Phone', width=120)
        self.tree.column('Dept', width=120)
        self.tree.column('Gender', width=100)
        self.tree.column('Attendance', width=80, stretch=NO)

        self.tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(rightFrame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=3, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bottom frame for action buttons
        buttonFrame = CTkFrame(self.window, fg_color='#1C2331')
        buttonFrame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky='ew')

        addButton = CTkButton(buttonFrame, text="Add Student", font=('Cascadia Code', 15), width=120, command=self.add_student)
        addButton.grid(row=0, column=0, padx=30, pady=10)

        updateButton = CTkButton(buttonFrame, text="Update", font=('Cascadia Code', 15), width=120, command=self.update_student)
        updateButton.grid(row=0, column=1, padx=30, pady=10)

        deleteButton = CTkButton(buttonFrame, text="Delete", font=('Cascadia Code', 15), width=120, command=self.delete_student)
        deleteButton.grid(row=0, column=2, padx=30, pady=10)

        showButton = CTkButton(buttonFrame, text="Show All", font=('Cascadia Code', 15), width=120, command=self.show_all)
        showButton.grid(row=0, column=3, padx=30, pady=10)

        deleteAllButton = CTkButton(buttonFrame, text="Delete All", font=('Cascadia Code', 15), width=120, command=self.delete_all)
        deleteAllButton.grid(row=0, column=4, padx=30, pady=10)

        clearButton = CTkButton(buttonFrame, text="Clear", font=('Cascadia Code', 15), width=120, command=self.clear_inputs)
        clearButton.grid(row=0, column=5, padx=30, pady=10)

        # Bind Treeview selection event
        self.tree.bind('<<TreeviewSelect>>', self.selection)

    def clear_inputs(self):
        """Clear all input fields in the form."""
        self.idEntry.delete(0, 'end')
        self.nameEntry.delete(0, 'end')
        self.phoneEntry.delete(0, 'end')
        self.DeptBox.set('')
        self.genderBox.set('')
        self.photo_label.configure(image=None,text='')
        self.photo_label.image = None
        self.captured_image = None

    def create_entry(self, parent, text, row, width=180):
        label = CTkLabel(parent, text=text, font=('Cascadia Code', 18, 'bold'), text_color='#fff')
        label.grid(row=row, column=0, padx=20, pady=10, sticky='w')
        entry = CTkEntry(parent, font=('Cascadia Code', 15, 'bold'), width=width)
        entry.grid(row=row, column=1, padx=10)
        return entry

    def create_combo_box(self, parent, text, row, values, default=''):
        label = CTkLabel(parent, text=text, font=('Cascadia Code', 18, 'bold'), text_color='#fff')
        label.grid(row=row, column=0, padx=20, pady=10, sticky='w')
        combo_box = CTkComboBox(parent, values=values, width=180, font=('Cascadia Code', 15, 'bold'), state='readonly')
        combo_box.grid(row=row, column=1, padx=10)
        combo_box.set(default or values[0])
        return combo_box

    def choose_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            image = Image.open(file_path)
            self.captured_image = self.image_to_binary(image)
            print("Photo selected and converted to binary.")

            display_size = (100, 100)
            resize_image = image.resize(display_size)
            self.photo = CTkImage(resize_image, size=display_size)

            self.photo_label.configure(image=self.photo)
            self.photo_label.image = self.photo

    def image_to_binary(self, image):
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        return buffer.getvalue()

    def add_student(self):
        student_id = self.idEntry.get()
        name = self.nameEntry.get()
        phone = self.phoneEntry.get()
        dept = self.DeptBox.get()
        gender = self.genderBox.get()

        if not all([student_id, name, phone, dept, gender, self.captured_image]):
            messagebox.showerror("Error", "Please fill in all fields and select a photo.")
            return

        if database.id_exists(student_id):
            messagebox.showerror("Error", f"Student with ID {student_id} already exists.")
            return

        try:
            database.insert(student_id, name, phone, dept, gender, self.captured_image)
            messagebox.showinfo("Success", "Student added successfully.")
            self.clear_inputs()
            self.show_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {e}")

    # def show_all(self):
    #     for row in self.tree.get_children():
    #         self.tree.delete(row)

    #     students = database.get_all_students()
    #     for student in students:
    #         self.tree.insert("", "end", values=student)

    def search_student(self):
        search_value = self.searchEntry.get()
        search_by = self.searchBox.get()

        if not search_value or search_by == "Search By":
            messagebox.showerror("Error", "Please select a search criteria and enter a value.")
            return

        students = database.search(search_by.lower(), search_value)
        if not students:
            messagebox.showinfo("No Results", "No matching students found.")
        else:
            for row in self.tree.get_children():
                self.tree.delete(row)
            for student in students:
                self.tree.insert("", "end", values=student)

    def filter_student(self):
        selected_item = self.tree.selection()
        
        if selected_item:
            student_id = self.tree.item(selected_item[0])['values'][0]
            print(student_id)
            
            if student_id:
                try:
                    attendance_app.AttendanceApp(self.window, student_id)
                except Exception as e:
                    print(f"Error: {e}")
                    messagebox.showerror('Error', 'Something went wrong while opening the attendance history.')
            else:
                messagebox.showwarning('Warning', 'Select the data first')
        else:
            messagebox.showwarning('Warning', 'No row selected. Please select a student first.')


    def delete_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            student_id = self.tree.item(selected_item[0])['values'][0]
            try:
                database.delete(student_id)
                messagebox.showinfo("Success", "Student deleted successfully.")
                self.show_all()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {e}")
        else:
            messagebox.showerror("Error", "Please select a student to delete.")

    def delete_all(self):
        try:
            database.delete_all()
            messagebox.showinfo("Success", "All students deleted successfully.")
            self.show_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete all students: {e}")

    # def update_student(self):
    #     selected_item = self.tree.selection()
    #     if selected_item:
    #         student_id = self.tree.item(selected_item[0])['values'][0]
    #         name = self.nameEntry.get()
    #         phone = self.phoneEntry.get()
    #         dept = self.DeptBox.get()
    #         gender = self.genderBox.get()

    #         if not all([name, phone, dept, gender]):
    #             messagebox.showerror("Error", "Please fill in all fields.")
    #             return

    #         try:
    #             database.update(student_id, name, phone, dept, gender)
    #             messagebox.showinfo("Success", "Student updated successfully.")
    #             self.show_all()
    #         except Exception as e:
    #             messagebox.showerror("Error", f"Failed to update student: {e}")

    def selection(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_inputs()
            if row:
                self.idEntry.delete(0, 'end')
                self.idEntry.insert(0, row[0])
                self.nameEntry.delete(0, 'end')
                self.nameEntry.insert(0, row[1])
                self.phoneEntry.delete(0, 'end')
                self.phoneEntry.insert(0, row[2])
                self.DeptBox.set(row[3])
                self.genderBox.set(row[4])

                # Load the photo
                try:
                    if isinstance(row[5], (bytes, bytearray)):  # Ensure it's binary data
                        photo_binary = row[5]
                        image = Image.open(io.BytesIO(photo_binary))  
                        resize_image = image.resize((100, 100))  
                        photo = CTkImage(resize_image, size=(100, 100)) 
                        self.photo_label.configure(image=photo)  
                        self.photo_label.image = photo 
                    else:
                        print(f"Invalid photo data: {row[5]}")
                        self.photo_label.configure(image=None)  # Clear the photo label
                        self.photo_label.image = None
                except (IndexError, IOError) as e:
                    print(f"Error loading photo: {e}")
                    self.photo_label.configure(image=None)  # Clear the photo label
                    self.photo_label.image = None

    def update_student(self):
        student_id = self.idEntry.get()
        name = self.nameEntry.get()
        phone = self.phoneEntry.get()
        dept = self.DeptBox.get()
        gender = self.genderBox.get()
        # photo = 
        try:
            database.update(student_id, name, phone, dept, gender, self.captured_image)
            messagebox.showinfo('Success', 'Student information updated successfully.')
            self.treeview_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {e}")


    def delete_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            student_id = item['values'][0]
            database.delete(student_id)
            messagebox.showinfo('Success', 'Student deleted successfully.')
            self.treeview_data()

    def show_all(self):
        self.treeview_data()

    def delete_all(self):
        messagebox.askyesno("Confirmation!","Are sure to DELETE all data!")
        database.delete_all()
        self.treeview_data()
        # messagebox.showinfo('Success', 'All records deleted successfully.')

    def treeview_data(self):
        students = database.fetch_student()
        self.tree.delete(*self.tree.get_children())
        for student in students:
            self.tree.insert('', END, values=student)

    def start(self):
        self.window.mainloop();

# Running the application
# if __name__ == "__main__":
#     root = CTk()
#     app = TeacherPanel(root)
#     app.start()
