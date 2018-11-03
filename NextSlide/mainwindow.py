import tkinter as tk


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(padx=135, pady=115)
        self.photo = tk.PhotoImage(file="play_black.gif")
        self.play = tk.Button(self)
        self.play["text"] = "Start Listening"
        #self.play["image"] = self.photo
        self.play["fg"] = "red"
        self.play["height"] = 5
        self.play["width"] = 20
        self.play["command"] = self.run
        self.play.bind("<Enter>", self.color)
        self.play.pack(side='top')

    def run(self):
        print("hi there, everyone!")


    def color(self, event):
        event.widget["activeforeground"] = "blue"


root = App()
root.master.title("NextSlide")
root.mainloop()
