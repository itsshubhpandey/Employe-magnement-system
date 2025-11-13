from pathlib import Path
from tkinter import *

from PIL import Image, ImageTk  # For resizing images

from employee import open_employee_frame


# ---------- Main Window ----------
Window = Tk()
Window.geometry("1380x868+0+0")
Window.title("Employee Management System")
Window.configure(bg="white")

# ---------- Left Sidebar (CREATE THIS FIRST!) ----------
leftframe = Frame(Window, bg='#4A63FF')
leftframe.place(x=0, y=0, width=200, height=900)

# Load and resize logo
logo_path = Path(__file__).resolve().parent / "assets" / "logo.png"

if logo_path.exists():
    try:
        original_image = Image.open(logo_path)
        resized_image = original_image.resize((200, 180))
        logo_img = ImageTk.PhotoImage(resized_image)

        logo_label = Label(leftframe, image=logo_img, bg="#4A63FF")
        logo_label.image = logo_img  # keep reference
        logo_label.pack(pady=20)
    except Exception:
        logo_label = Label(
            leftframe,
            text="LOGO",
            font=("Cascadia Mono", 20, "bold"),
            bg="#4A63FF",
            fg="white",
        )
        logo_label.pack(pady=20)
else:
    logo_label = Label(
        leftframe,
        text="LOGO",
        font=("Cascadia Mono", 20, "bold"),
        bg="#4A63FF",
        fg="white",
    )
    logo_label.pack(pady=20)


employee_frame = None

# ---------- Function to Open Employee Frame ----------



# ---------- Sidebar Buttons ----------
button_config = {
    'font': ('Cascadia Mono', 15), 
    'bd': 0, 
    'bg': '#4A63FF',
    'fg': 'white',
    'activebackground': "white", 
    'width': 20,
    'cursor': 'hand2'
}





menu_label = Label(leftframe, text="Menu", font=('Cascadia Mono', 25, 'bold'), 
                      bg='#4A63FF', fg='white')
menu_label.pack(pady=20)


employeeButton = Button(leftframe, text="Employees", command=lambda: open_employee_frame(Window), **button_config)
employeeButton.pack(pady=5)

supplierButton = Button(leftframe, text="Supplier", **button_config)
supplierButton.pack(pady=5)

productsButton = Button(leftframe, text="Products", **button_config)
productsButton.pack(pady=5)

categoryButton = Button(leftframe, text="Category", **button_config)
categoryButton.pack(pady=5)

salesButton = Button(leftframe, text="Sales", **button_config)
salesButton.pack(pady=5)

exitButton = Button(leftframe, text="Exit", command=Window.destroy, **button_config)
exitButton.pack(pady=5)

# ---------- Run Main Loop ----------
Window.mainloop()