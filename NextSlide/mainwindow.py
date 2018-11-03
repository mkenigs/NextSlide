from tkinter import *
from tkinter.filedialog import askopenfilename


def read(input):
    text = input


def startListening():
    play['image'] = pause


def stopListening():
    play['image'] = start


def run():
    if play['image'] == start.name:
        startListening()
    else:
        stopListening()
        text1['text'] = 'Press play to start'


def getFile():
    filename = askopenfilename()
    if filename:
        pickFile['text'] = filename[filename.rfind('/') + 1:]
        stopListening()
        print('hello world this is a \n test')
        print("hello world this is another \n test")


master = Tk()
master.title('NextSlide')
master.geometry('200x160')
master.resizable(0, 0)

text1 = Label(text='Press play to start')
text1.pack(padx=10, pady=10)

start = PhotoImage(file='Play.png')
pause = PhotoImage(file='Pause.png')
play = Button(image=start, height=50, width=50, command=run)
play.pack(padx=10, pady=10)

pickFile = Button(text='Please select a file', height=50, width=50, command=getFile)
pickFile.pack(padx=10, pady=10)

mainloop()
