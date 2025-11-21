import tkinter as tk
import runpy
import os

root = tk.Tk()
root.geometry("800x500")
root.title("Bank Management System")
text = runpy.run_path("run.py")["main_menu"].options
label = tk.Label(root,text = text, font=('Arial', 12))
label.pack(pady = 100)
if __name__ == "__main__":
    root.mainloop()