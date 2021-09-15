import tkinter as tk
from tkinter import messagebox
import random
import string

words = ['elephant', 'zebra', 'giraffe', 'panda', 'alligator',
         'toyota', 'mazda', 'mercedes', 'lexus', 'lamborghini',
         'guitar', 'piano', 'bass', 'drums', 'violin',
         'iran', 'japan', 'cambodia', 'jamaica', 'congo',
         'football', 'basketball', 'volleyball', 'tennis', 'karate']


def chooseWord():
    return random.choice(words)


class Hangman:
    def __init__(self):
        # score and remaining tries, initially set to 0 and 10 respectively
        self.score = 0
        self.tries = 10

        # the query, random word chosen from the list along with a list of words that have already been chosen once
        self.query = chooseWord()
        self.used_words = []

        # how much of the query has been solved. we make it a list so that we can change it later
        self.query_display = list('-' * len(self.query))

        # two lists representing inputs that are correct(26 english letters capital and small)
        # along with a list representing letters that have already been guessed
        self.letters = list(string.ascii_uppercase + string.ascii_lowercase)
        self.tried = []

        # root widget
        self.root = tk.Tk()
        self.root.title('Hangman - A Python Project')
        self.root.config(bg='black',
                         width=45,
                         height=45)

        # label 1: hangman title
        self.lb1 = tk.Label(self.root)
        self.lb1.config(text='H A N G M A N',
                        fg='black',
                        bg='white',
                        font='Helvetica 26 bold')
        self.lb1.grid(row=0, column=0)

        # label 2: display score
        self.lb2 = tk.Label(self.root)
        self.lb2.config(text=self.display_score(),
                        fg='black',
                        bg='white',
                        font='Helvetica 20 bold')
        self.lb2.grid(row=2, column=0)

        # label 3: display remaining tries
        self.lb3 = tk.Label(self.root)
        self.lb3.config(text=self.display_tries(),
                        fg='black',
                        bg='white',
                        font='Helvetica 20 bold',)
        self.lb3.grid(row=4, column=0)

        # label 4: display query and how much of it is solved
        self.lb4 = tk.Label(self.root)
        self.lb4.config(text=self.query_display,
                        fg='black',
                        bg='white',
                        font='Helvetica 20 bold')
        self.lb4.grid(row=6, column=0)

        # test label: will be removed later
        self.test = tk.Label(self.root)
        self.test.config(text=self.query)
        self.test.grid(row=7, column=0)

        # Entry: letter entry
        self.ent1 = tk.Entry(self.root)
        self.ent1.config()
        self.ent1.grid(row=8, column=0)

        self.btn1 = tk.Button(self.root)
        self.btn1.config(text='Enter',
                         command=self.entry_command)
        self.btn1.grid(row=10, column=0)

    # method for running the game
    def run(self):
        self.root.mainloop()

    # method for displaying current score
    def display_score(self):
        return 'Score: ' + str(self.score)

    # method for displaying remaining guesses
    def display_tries(self):
        return 'Remaining Guesses: ' + str(self.tries)

    # method for finding instances of a letter in the query and storing them in a list.
    # will be used in another method
    def indexes(self, letter):
        result = []
        index = 0
        if letter in self.query:
            while index < len(self.query):
                index = self.query.find(letter, index)
                if index == -1:
                    break
                result.append(index)
                index += len(letter)
        return result

    # method changing query display when a letter is in the query
    def input_letter(self, letter):
        if letter in self.query:
            for i in self.indexes(letter):
                self.query_display[i] = letter
                self.lb4.config(text=self.query_display)

    # method for subtracting number of guesses left and changing the label
    def subtract_tries(self):
        self.tries -= 1
        self.lb3.config(text=self.display_tries())

    # method for making the query display list into a string so we can compare
    def str_query_display(self):
        result = ''
        for i in self.query_display:
            result += i
        return result

    # method for checking whether the player has guessed the right word or not
    def check_query(self):
        return self.query == self.str_query_display()

    # method for entering the input
    def entry_command(self):
        inp = self.ent1.get()
        if inp in self.letters and inp not in self.tried:
            # add the input to the list of guessed letters
            self.tried.append(inp)
            # call input_letter on inp, if inp is in query, it'll be changed
            self.input_letter(inp)
            # subtract number of remaining guesses by 1
            self.subtract_tries()
            # testing to see if it's working correctly
            print(self.query)
            print(self.str_query_display())
            # reset_query if the player has ran out of guesses without getting it right
            if self.tries == 0 and not self.check_query():
                tk.messagebox.showinfo('Alert', 'Ran out of guesses!')
                self.reset_query()
            # if the player has got it right
            elif self.check_query():
                self.score += 1
                self.lb2.config(text=self.display_score())
                tk.messagebox.showinfo('Alert', 'CORRECT!')
                self.reset_query()
        # if inp has already been guessed
        elif inp in self.tried:
            tk.messagebox.showinfo('Alert', 'Already tried that letter!')
            self.ent1.delete(0, 'end')
        # if inp is incorrect (not a capital or small letter)
        else:
            self.ent1.delete(0, 'end')

    # reset query for when the player runs out of guesses or guesses correct
    def reset_query(self):
        self.query = chooseWord()
        self.query_display = list('-' * len(self.query))
        self.lb4.config(text=self.query_display)
        self.tries = 10
        self.lb3.config(text=self.display_tries())


hangman = Hangman()
hangman.run()
