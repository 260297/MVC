import tkinter as tk
from View.view import EstudanteGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = EstudanteGUI(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
