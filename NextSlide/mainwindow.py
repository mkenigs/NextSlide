from tkinter import *
from tkinter.filedialog import askopenfilename
from transcription import Transcriber

def read(input):
    text = input


def startListening():
    if not play['text']:
        text1['text'] = 'Please select a file first'
    else:
        text1['text'] = 'Listening'
        play['image'] = pause
        myTranscriber.start()
        if myTranscriber:
            print(1)
        else:
            print(0)


def stopListening():
    play['image'] = start
    text1['text'] = 'Press play to start'
    myTranscriber.stop()
    if myTranscriber:
        print(1)
    else:
        print(0)


def run():
    if play['image'] == start.name:
        startListening()
    else:
        stopListening()


def getFile():
    play['text'] = askopenfilename()
    global myTranscriber
    if play['text']:
        pickFile['text'] = play['text'][play['text'].rfind('/') + 1:]
        stopListening()
        myTranscriber = Transcriber(play['text'])
    else:
        myTranscriber = None


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
