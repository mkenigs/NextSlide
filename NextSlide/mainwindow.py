from tkinter import *
from tkinter.filedialog import askopenfilename
import transcription
import threading

def read(input):
    text = input

class MainWindow():
    def __init__(self, master):
        self.master = master
        self.master.title('NextSlide')
        self.master.geometry('400x320')
        self.master.resizable(0, 0)

        self.text1 = Label(text='Press play to start')
        self.text1.pack(padx=20, pady=20)

        self.start = PhotoImage(file='Play.png')
        self.pause = PhotoImage(file='Pause.png')
        self.play = Button(image=self.start, height=100, width=100, command=self.run)
        self.play.pack(padx=20, pady=20)

        self.pickFile = Button(text='Please select a file', height=100, width=100, command=self.getFile)
        self.pickFile.pack(padx=20, pady=20)

        self.myTranscriber = None


    def startListening(self):
        if not self.play['text']:
            self.text1['text'] = 'Please select a file first'
        else:
            self.text1['text'] = 'Listening'
            self.play['image'] = self.pause
            threading.Thread(target=self.myTranscriber.start).start()


    def stopListening(self):
        self.play['image'] = self.start
        self.text1['text'] = 'Press play to start'
        if self.myTranscriber: self.myTranscriber.stop()


    def run(self):
        if self.play['image'] == self.start.name:
            self.startListening()
        else:
            self.stopListening()


    def getFile(self):
        self.play['text'] = askopenfilename()
        if self.play['text']:
            self.pickFile['text'] = self.play['text'][self.play['text'].rfind('/') + 1:]
            self.stopListening()
            self.myTranscriber = transcription.Transcriber(self.play['text'])


if __name__ == '__main__':
    master = Tk()
    myGui = MainWindow(master)
    master.mainloop()
