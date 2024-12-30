import customtkinter as ctk
from PIL import Image
import time
from main import App  # Import App class from attendance_system

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Splash Screen Logic
def splash_screen():
    # Create the main window
    root = ctk.CTk()
    root.title("WHAT IFF")

    # Set the window size and position
    width_of_window = 427
    height_of_window = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    root.geometry(f"{width_of_window}x{height_of_window}+{int(x_coordinate)}+{int(y_coordinate)}")
    root.overrideredirect(1)

    # Create the main frame
    frame = ctk.CTkFrame(root, width=427, height=250, corner_radius=0)
    frame.place(x=0, y=0)

    # Create the "WHAT IFF" label
    label1 = ctk.CTkLabel(frame, text="WHAT IFF", font=("Helvetica", 26), text_color="white")
    label1.place(x=140, y=90)

    # Create the "Loading..." label
    label2 = ctk.CTkLabel(frame, text="Loading...", font=("FiraCode Nerd Font", 11), text_color="white")
    label2.place(x=10, y=215)

    # Load the images
    image_a = Image.open('c2.png')
    image_b = Image.open('c1.png')

    # Create the animation
    for _ in range(2):  # Reduced iterations for faster transition
        l1 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_a, size=(10, 10))).place(x=180, y=145)
        l2 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_b, size=(10, 10))).place(x=200, y=145)
        l3 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_b, size=(10, 10))).place(x=220, y=145)
        l4 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_b, size=(10, 10))).place(x=240, y=145)
        root.update_idletasks()
        time.sleep(0.3)

        l1 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_b, size=(10, 10))).place(x=180, y=145)
        l2 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_a, size=(10, 10))).place(x=200, y=145)
        l3 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_b, size=(10, 10))).place(x=220, y=145)
        l4 = ctk.CTkLabel(frame, text='', image=ctk.CTkImage(image_b, size=(10, 10))).place(x=240, y=145)
        root.update_idletasks()
        time.sleep(0.3)

    root.destroy()  # Close the splash screen

# Main Execution
if __name__ == "__main__":
    splash_screen()  # Show splash screen
    app = App()  # Start the attendance system
    app.start()
