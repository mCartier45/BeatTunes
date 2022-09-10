import tkinter as tk


if __name__ == "__main__":
    window = tk.Tk()


    greeting = tk.Label(text="Hello, Tkinter")
    greeting.pack()


    window.mainloop()