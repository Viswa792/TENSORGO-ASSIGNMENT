from customtkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import phase1_statistical_function_added
import phase2_plotting_added
import phase3_qa_added

# Global variable to track file attachment status
file_attached = False
path=''
ds_flag=0
# Function to handle attachment of files

def attach_file():
    global ds_flag
    if ds_flag==1:
        phase1_statistical_function_added.dest()
        ds_flag=0
    global path
    global file_attached
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Attached file: {file_path}")
        file_attached = True
        # Enable the other buttons
        stats_button.configure(state="normal")
        plot_button.configure(state="normal")
        qa_button.configure(state="normal")
    path=file_path

# Function to handle Descriptive Stats button click
def descriptive_stats():
    global path
    phase1_statistical_function_added.ds(app,path)
    global ds_flag
    ds_flag=1
# Function to handle Plotting button aclick
def plotting():
    global ds_flag
    global path
    if ds_flag==1:
        phase1_statistical_function_added.dest()
        ds_flag=0
    phase2_plotting_added.main(path)
# Function to handle Q&A button click
def q_and_a():
    global path
    global ds_flag
    if ds_flag == 1:
        phase1_statistical_function_added.dest()
        ds_flag = 0
    phase3_qa_added.main(path)

app = CTk()
app.title(" DATA ANALYZER ")
app.configure(bg="#c5c8e2")
set_appearance_mode("light")
set_default_color_theme("green")
app.iconbitmap("images/ima.jpg")

# Set window size and position
window_width = 750
window_height = 500

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Load and resize the image
img = Image.open("images/ima.jpg")
img_width = int(433)  # Calculate the width of the image
img_height = int(474)  # Use the height of the window for the image
img = img.resize((img_width, img_height), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img)

# Create a label to display the image
image_label = CTkLabel(master=app, image=img1, bg_color="#c5c8e2")
image_label.place(relx=0, rely=0, relwidth=0.6, relheight=1)

# Frame on the right half
frame = CTkFrame(master=app, width=0.4 * window_width, height=window_height, fg_color="#c5c8e2")
frame.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

# Label
label = CTkLabel(master=frame, text="WELCOME", font=("Arial", 30, 'bold'), text_color="black", width=50)
label.place(x=60, y=10)

# Attachment Button
attach_button = CTkButton(master=frame, text="Attach File", width=200, corner_radius=20, cursor="hand2", command=attach_file)
attach_button.place(x=50, y=50)

# Descriptive Stats Button (initially disabled)
stats_button = CTkButton(master=frame, text="Descriptive Stats", width=150, corner_radius=20, cursor="hand2", state="disabled", command=descriptive_stats)
stats_button.place(x=0, y=90)

# Plotting Button (initially disabled)
plot_button = CTkButton(master=frame, text="Plotting", width=130, corner_radius=20, cursor="hand2", state="disabled", command=plotting)
plot_button.place(x=160, y=90)

# Q&A Button (initially disabled)
qa_button = CTkButton(master=frame, text="Q & A", width=150, corner_radius=20, cursor="hand2", state="disabled", command=q_and_a)
qa_button.place(x=65, y=130)

# Disable resizing of the window
app.resizable(width=False, height=False)

app.mainloop()