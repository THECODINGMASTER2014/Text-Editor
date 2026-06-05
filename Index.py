from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.colorchooser import askcolor

kitty = Tk()
kitty.title("WordSmith")
kitty.geometry("800x600")

kitty.rowconfigure(0, weight=1)
kitty.columnconfigure(1, weight=1)

font_size = 12

def open_file():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not filepath:
        return

    txt_edit.delete(1.0, END)

    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(END, text)

    kitty.title(f"WordSmith - {filepath}")

def save_file():
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not filepath:
        return

    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, END)
        output_file.write(text)

    kitty.title(f"WordSmith - {filepath}")

def increase_font():
    global font_size
    font_size += 2
    txt_edit.config(font=("Arial", font_size))

def decrease_font():
    global font_size
    if font_size > 6:
        font_size -= 2
        txt_edit.config(font=("Arial", font_size))

def change_color():
    color = askcolor(title="Choose Text Color")[1]
    if color:
        txt_edit.config(fg=color)

def standard_font():
    global font_size
    font_size = 12
    txt_edit.config(font=("Arial", font_size), fg="black")
def clear_text():
    txt_edit.delete(1.0, END)

# Text editor
txt_edit = Text(kitty, font=("Arial", font_size))
txt_edit.grid(row=0, column=1, sticky="nsew")

# Button frame
fr_buttons = Frame(kitty, relief=RAISED, bd=2)
fr_buttons.grid(row=0, column=0, sticky="ns")

# Buttons
btn_open = Button(fr_buttons, text="Open", command=open_file)
btn_save = Button(fr_buttons, text="Save As...", command=save_file)
btn_increase = Button(fr_buttons, text="A+", command=increase_font)
btn_decrease = Button(fr_buttons, text="A-", command=decrease_font)
btn_color = Button(fr_buttons, text="Text Color", command=change_color)
btn_standard = Button(fr_buttons, text="Default Font", command=standard_font)
btn_clear = Button(fr_buttons, text="Clear Text", command=clear_text)
# Layout
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_increase.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_decrease.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_color.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
btn_standard.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
btn_clear.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

kitty.mainloop()