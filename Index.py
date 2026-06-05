from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.colorchooser import askcolor
from spellchecker import SpellChecker

kitty = Tk()
kitty.title("WordSmith")
kitty.geometry("900x600")

kitty.rowconfigure(0, weight=1)
kitty.columnconfigure(1, weight=1)

font_size = 20
spell = SpellChecker()

# ---------------- Functions ----------------

def open_file():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not filepath:
        return

    txt_edit.delete("1.0", END)

    with open(filepath, "r", encoding="utf-8") as file:
        txt_edit.insert("1.0", file.read())

    kitty.title(f"WordSmith - {filepath}")
    highlight_mistakes()


def save_file():
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not filepath:
        return

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(txt_edit.get("1.0", END))

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
    txt_edit.delete("1.0", END)
    update_word_count()


def undo():
    try:
        txt_edit.edit_undo()
    except:
        pass


def redo():
    try:
        txt_edit.edit_redo()
    except:
        pass


def update_word_count():
    text = txt_edit.get("1.0", "end-1c")
    words = len(text.split())
    status_bar.config(text=f"Words: {words}")


def highlight_mistakes(event=None):
    txt_edit.tag_remove("misspelled", "1.0", END)

    text = txt_edit.get("1.0", "end-1c")
    words = text.split()

    start_pos = "1.0"

    for word in words:
        pos = txt_edit.search(word, start_pos, stopindex=END)

        if not pos:
            continue

        end_pos = f"{pos}+{len(word)}c"

        clean_word = word.strip(
            ".,!?;:()[]{}\"'"
        ).lower()

        if clean_word and clean_word not in spell:
            txt_edit.tag_add("misspelled", pos, end_pos)

        start_pos = end_pos

    update_word_count()

# ---------------- Text Area ----------------

txt_edit = Text(
    kitty,
    font=("Arial", font_size),
    wrap=WORD,
    undo=True
)

txt_edit.grid(row=0, column=1, sticky="nsew")

txt_edit.tag_configure(
    "misspelled",
    foreground="red",
    underline=True
)

txt_edit.bind("<KeyRelease>", highlight_mistakes)

# ---------------- Button Panel ----------------

fr_buttons = Frame(kitty, relief=RAISED, bd=2)
fr_buttons.grid(row=0, column=0, sticky="ns")

Button(fr_buttons, text="Open", command=open_file).grid(
    row=0, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="Save", command=save_file).grid(
    row=1, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="A+", command=increase_font).grid(
    row=2, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="A-", command=decrease_font).grid(
    row=3, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="Text Color", command=change_color).grid(
    row=4, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="Default Font", command=standard_font).grid(
    row=5, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="Clear Text", command=clear_text).grid(
    row=6, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="Undo", command=undo).grid(
    row=7, column=0, sticky="ew", padx=5, pady=5
)

Button(fr_buttons, text="Redo", command=redo).grid(
    row=8, column=0, sticky="ew", padx=5, pady=5
)

# ---------------- Status Bar ----------------

status_bar = Label(
    kitty,
    text="Words: 0",
    anchor="w"
)

status_bar.grid(
    row=1,
    column=1,
    sticky="ew"
)

kitty.mainloop()