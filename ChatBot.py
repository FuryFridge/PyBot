from tkinter import messagebox
from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pyttsx3
import speech_recognition as s
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

bot = ChatBot('Bill')
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english')


def ask_bot():
    Q = questionField.get()
    ans = bot.get_response(Q)
    text_area.configure(state=NORMAL)
    text_area.insert(END, 'You: ' + Q + '\n\n')
    text_area.insert(END, 'Bot: ' + str(ans) + '\n\n')
    text_area.configure(state=DISABLED)
    engine.say(ans)
    engine.runAndWait()

    questionField.delete(0, END)
    text_area.yview(END)


def take_query():
    sr = s.Recognizer()
    sr.pause_threshold = 1
    print('Your bot is listenning to you...')
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            questionField.delete(0, END)
            questionField.insert(0, query)
            ask_bot()
        except Exception as e:
            messagebox.showerror('Error', 'Your voice not recognized')


root = Tk()
root.geometry('500x540+100+30')
root.resizable(0, 0)
root.title('ChatBot v1.0.0')
root.config(bg='#5D5C61')

pic = PhotoImage(file='bot.png')

pic_lbl = Label(root, image=pic, bg='#5D5C61')
pic_lbl.pack(side=TOP, pady=5)
center_frame = Frame(root)
center_frame.pack()

scrollabar = Scrollbar(center_frame)
scrollabar.pack(side=RIGHT, fill=Y)

text_area = Text(center_frame, state=DISABLED, font=('arial', 16), width=80, height=15, yscrollcommand=scrollabar.set)
text_area.pack(side=LEFT, fill=BOTH)

questionField = Entry(root, font=('arial', 16))
questionField.place(x=0, y=490, height=30, width=460)

ask_pic = PhotoImage(file='send1.png')
ask_btn = Button(root, image=ask_pic, width=30, height=30, bd=0, bg='#5D5C61', activebackground='#5D5C61',
                 cursor='hand2', command=ask_bot)
ask_btn.place(x=465, y=490)


def enter_function(event):
    ask_btn.invoke()


root.bind('<Return>', enter_function)


def rep():
    while True:
        take_query()


#t = threading.Thread(target=rep)
#t.start()

root.mainloop()
