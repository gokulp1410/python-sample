import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser

# main window
root = tk.Tk()
root.title("Text_Editor")
root.geometry("1080x800")

# Font State 
current_font_family = tk.StringVar(value="Helvetica")
current_font_size = tk.IntVar(value=12)
is_bold = tk.BooleanVar(value=False)
is_italic = tk.BooleanVar(value=False)
is_underline = tk.BooleanVar(value=False)
current_file_path = None

#  Text Widget 
text = tk.Text(root, wrap=tk.WORD, fg="black")
text.pack(expand=tk.YES, fill=tk.BOTH)

#  Status Bar 
status_bar = tk.Label(root, text="Words: 0 | Characters: 0", anchor="e")
status_bar.pack(fill=tk.X, side=tk.BOTTOM)


def update_font(*args):
    """Apply font style, size, and family."""
    weight = "bold" if is_bold.get() else "normal"
    slant = "italic" if is_italic.get() else "roman"
    underline = 1 if is_underline.get() else 0

    new_font = font.Font(
        family=current_font_family.get(),
        size=current_font_size.get(),
        weight=weight,
        slant=slant,
        underline=underline,
    )
    text.configure(font=new_font)


def update_status_bar(event=None):
    content = text.get("1.0", tk.END)
    words = len(content.split())
    chars = len(content) - 1  # remove trailing newline
    status_bar.config(text=f"Words: {words} | Characters: {chars}")


#  File Operations 

def new_file():
    global current_file_path
    if text.get("1.0", tk.END).strip():
        confirm = messagebox.askyesnocancel("Confirm", "Save current file?")
        if confirm:
            save_file()
        elif confirm is None:
            return

    text.delete("1.0", tk.END)
    current_file_path = None
    update_status_bar()


def open_file():
    global current_file_path
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text.delete("1.0", tk.END)
            text.insert(tk.END, file.read())
        current_file_path = file_path
        update_status_bar()


def save_file():
    global current_file_path

    if not current_file_path:
        current_file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
        )

    if current_file_path:
        with open(current_file_path, "w", encoding="utf-8") as file:
            file.write(text.get("1.0", tk.END))
        messagebox.showinfo("Saved", "File saved successfully!")


#  Text Formatting 

def choose_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        text.config(fg=color)


#  Menu Bar 
menu = tk.Menu(root)
root.config(menu=menu)

# File Menu
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Font Menu
font_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Font", menu=font_menu)

# Font Family Submenu
family_menu = tk.Menu(font_menu, tearoff=0)
font_menu.add_cascade(label="Family", menu=family_menu)

for f in sorted(font.families()):
    family_menu.add_radiobutton(label=f, variable=current_font_family, value=f, command=update_font)

# Font Size Submenu
size_menu = tk.Menu(font_menu, tearoff=0)
font_menu.add_cascade(label="Size", menu=size_menu)

for size in range(8, 49, 2):
    size_menu.add_radiobutton(label=str(size), variable=current_font_size, value=size, command=update_font)

# Style Menu
style_menu = tk.Menu(font_menu, tearoff=0)
font_menu.add_cascade(label="Style", menu=style_menu)
style_menu.add_checkbutton(label="Bold", variable=is_bold, command=update_font)
style_menu.add_checkbutton(label="Italic", variable=is_italic, command=update_font)
style_menu.add_checkbutton(label="Underline", variable=is_underline, command=update_font)

# Color Menu
menu.add_command(label="Text Color", command=choose_text_color)

# ---------- Keyboard Shortcuts ----------
root.bind("<Control-n>", lambda e: new_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-s>", lambda e: save_file())

# ---------- Word Count Tracking ----------
text.bind("<KeyRelease>", update_status_bar)

# Initialize
update_font()
update_status_bar()

root.mainloop()
