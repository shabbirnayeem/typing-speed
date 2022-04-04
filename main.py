from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pynput.keyboard import Key, Controller
import time
import random
import requests


# Desktop App for Typing Speed Test

# ------------------------  Functions --------------------------------------------
WORD_SITE = "https://www.mit.edu/~ecprice/wordlist.10000"


def generate_word():
    response = requests.get(WORD_SITE).text
    word_list = []
    for words in response.splitlines():
        word_list.append(words)

    random.shuffle(word_list)
    for word in word_list:
        return word


def counter():
    # calculate NET WPM
    # formula: gross_wpm - (number of error / time)
    # net_wpm = gross_wpm - len(incorrect_word)

    # Count WPM
    # wpm formula: raw_cpm / 5 == wpm
    gross_wpm = round((len(correct_cpm) / 5))
    wpm_entry.delete(0, 'end')
    wpm_entry.insert(0, gross_wpm)

    # Count CPM
    cpm_entry.delete(0, 'end')
    cpm_entry.insert(0, len(correct_cpm))


def match_text():

    # getting new word from the list
    new_word = generate_word()

    # getting hold of the term from the text area
    term = text_area.get()

    # getting hold of the user input
    user_input = type_area.get().strip()

    # print(user_input)
    count = 0

    # controlling the keyboard
    kb = Controller()

    # appending all the words
    all_words.append(term)

    if term == user_input:
        # if the user types the word correctly append to a list
        correct_wpm.append(f"{user_input}")

        for char in user_input:
            correct_cpm.append(char)
            raw_cpm.append(f"{char}")

        # clear the type area box
        type_area.delete(0, 'end')

        # once user types the work and press space it types a space character
        # does not bring the cursor back to 0
        # using pynput.keyboard to control the keyboard
        # here pressing the backspace once the user is done typing the word
        kb.press(Key.backspace)
        kb.release(Key.backspace)

        # if the user types the word correctly delete the word from text area
        # the first number repreent the number and the second num represent the char index
        # For ex: "1.0" represent line 1 and index 0. this will delete the first letter from line 1
        # in this case: I am getting the size of every words typed in the entry box using type_area.index('insert')
        # Adding 1 for the space
        # text_area.delete("1.0", f"1.{position + 1}")
        text_area.delete(0, 'end')
        text_area.insert("end", new_word)

    elif term != user_input:
        count += 1
        for char in user_input:
            raw_cpm.append(f"{char}")

        # clear the type area box
        type_area.delete(0, 'end')
        # incorrect_word.append(user_input)
        incorrect_word[term] = user_input
        text_area.delete(0, 'end')
        text_area.insert("end", new_word)
        # text_area.tag_add('not_correct', "1.0", f"1.{len(user_input)}")
        # text_area.tag_configure('not_correct', background='blue', foreground='red')
        print(incorrect_word)
    counter()


def timer():
    global amt_time
    while amt_time > -1:
        #  divmod(firstvalue = temp//60, secondvalue = temp%60)
        mins, secs = divmod(amt_time, 60)
        second.set(f"00:00:{secs}")
        # print(mins, secs)
        # updating the GUI window after decrementing the
        # temp value every time
        window.update()
        time.sleep(1)

        if amt_time == 0:

            messagebox.showinfo("Timer Countdown", f"Your score: {len(correct_cpm)} CPM "
                                                   f"(that is {wpm_entry.get()} WPM)\n"
                                                   f"In reality, you typed {len(raw_cpm)} CPM,"
                                                   f"but you made {len(incorrect_word)} mistakes"
                                                   f"(out of {len(all_words)} words), "
                                                   f"which were not counted in the corrected scores.\n"
                                                   f"You mistakes were:\n"
                                                   f"{incorrect_word}")

        amt_time -= 1


def restart():

    # setting the time back to 60 sec
    global amt_time
    amt_time = 60
    # when user click on the restart button setting the seconds to default 60 sec
    # second.set("00:00:10")
    # clearing the correct list to 0
    correct_wpm.clear()
    # # delete the entry from the wpm_entry box
    wpm_entry.delete(0, 'end')
    cpm_entry.delete(0, "end")

    # when the user clicks restart it will delete the words from the text area
    text_area.delete(0, "end")

    # re-insert the text from the word_list
    # random.shuffle(words_list)
    text_area.insert("end", generate_word())

    timer()
    # window.destroy()


# ---------------------------------------------- Setup UI ------------------------------------------------

window = tk.Tk()

window.title("Typing Speed Test")
window.minsize(width=500, height=300)

# --------------------------------------------- Top Frame ------------------------------------------------

top_frame = tk.Frame(window, height=100, width=400, highlightbackground='black',)
top_frame.pack()

wpm_label = tk.Label(top_frame, text="WPM :")
wpm_label.grid(row=0, column=0)
wpm_entry = tk.Entry(top_frame, width=5)
wpm_entry.insert('end', "?")
wpm_entry.grid(row=0, column=1, padx=15)

cpm_label = tk.Label(top_frame, text="CPM :")
cpm_label.grid(row=0, column=2)
cpm_entry = tk.Entry(top_frame, width=5)
cpm_entry.insert('end', "?")
cpm_entry.grid(row=0, column=3, padx=15)


second = StringVar()
second.set("00:00:60")
timer_entry = tk.Entry(top_frame, width=8, textvariable=second)
timer_entry.grid(row=0, column=4, padx=10)
amt_time = int(timer_entry.get().split(':')[-1])

start_button = ttk.Button(top_frame, text="Start", command=timer)
start_button.grid(row=0, column=5)

restart_button = ttk.Button(top_frame, text="Restart", command=restart)
restart_button.grid(row=0, column=6)


# ---------------------------------------------- Mid Frame ------------------------------------------------

mid_frame = tk.Frame(window, height=250, width=400, highlightbackground='black', highlightthickness=.5)
mid_frame.pack()

# count all the words
all_words = []
# Appending all the correct ones
correct_wpm = []
# count all incorrect words
# incorrect_word = []
incorrect_word = {}

# count all the character user types
raw_cpm = []

# count only the correct CPM
correct_cpm = []

# text_area = scrolledtext.ScrolledText(mid_frame, height=10, width=60, wrap='word', undo=True)
text_area = tk.Entry(mid_frame, width=60)
text_area.insert('end', generate_word())
# highlight #
text_area.pack()

# ---------------------------------------------- Bottom Frame ------------------------------------------------

bottom_frame = tk.Frame(window, height=75, width=400, highlightbackground='black', highlightthickness=.5)
bottom_frame.pack()
type_area = tk.Entry(bottom_frame, width=60)
type_area.bind('<space>', (lambda event: match_text()))
type_area.pack()

window.mainloop()




