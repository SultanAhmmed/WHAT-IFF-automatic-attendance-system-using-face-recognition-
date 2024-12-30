import customtkinter as ctk
from tkinter import ttk
import database

class AttendanceApp(ctk.CTkToplevel):
    def __init__(self, parent, student_id):
        super().__init__(parent)
        self.title("Attendance History")
        self.geometry("700x500+200+50")
        self.student_id = student_id

        # Filter Frame for Month Input
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(pady=10)

        ctk.CTkLabel(self.filter_frame, text="Month (1-12):").grid(row=0, column=0, padx=5)
        self.month_entry = ctk.CTkEntry(self.filter_frame, width=100)
        self.month_entry.grid(row=0, column=1, padx=5)

        filter_button = ctk.CTkButton(self.filter_frame, text="Filter Attendance", command=self.filter_attendance)
        filter_button.grid(row=0, column=2, padx=5)

        # Treeview for Attendance History
        self.result_treeview = ttk.Treeview(self, columns=("Name", "Date"), show="headings")
        self.result_treeview.heading("Name", text="Name")
        self.result_treeview.heading("Date", text="Date")
        self.result_treeview.pack(fill="both", expand=True)

        # Load all attendance history by default
        self.load_attendance_history()

    def load_attendance_history(self):
        # Fetch all attendance history from the database
        attendance_history = database.get_attendance_by_student(self.student_id)
        self.result_treeview.delete(*self.result_treeview.get_children())  # Clear old results

        for row in attendance_history:
            self.result_treeview.insert("", ctk.END, values=row)

    
    def filter_attendance(self):
        month = self.month_entry.get()
        if not month.isdigit() or not (1 <= int(month) <= 12):
            ctk.CTkLabel(self, text="Invalid month! Enter a value between 1 and 12.", fg_color="red").pack(pady=5)
            return

        # Fetch attendance history filtered by month from database
        attendance_history = database.filter_attendance(self.student_id, month)
        self.result_treeview.delete(*self.result_treeview.get_children())  # Clear old results

        for row in attendance_history:
            self.result_treeview.insert("", ctk.END, values=row)
