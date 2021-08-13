from random import randint
from numpy.random import choice
from tkinter.constants import X
import string
import PySimpleGUI as sg
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

alphabet_dict = list(string.ascii_uppercase)
repeats = 5
word = ""
score = 0


#The weights of letters in the English language, sourced from below:
#http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
weights = [8.12, 1.49, 2.71, 4.32, 12.02, 2.30, 2.03, 5.92, 7.31, 0.10, 0.69, 3.98, 2.61, 6.95, 7.68, 1.82, 0.11, 6.02, 6.28, 9.10, 2.88, 1.11, 2.09, 0.17, 2.11, 0.07]

#a dictionary of letters with their scrabble scores in alphabetical order, sourced from below:
#https://scrabble.hasbro.com/en-us/faq
scores = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1}

#An empty list to be filled with buttons.
grid = []


class Handler:
    def __init__(self, x, y, letter):
        self.x = x 
        self.y = y
        self.letter = letter

    def handle_input(self):
        handle_input(self.x, self.y, self.letter)

def create_grid():
    for int in range(1, repeats + 1):
        row = make_row()
        grid.append(row)


def make_row():
    list = []
    for int in range(1, repeats + 1):
        item = choice(alphabet_dict, 1, weights)[0]
        list.append(item)
    return list



def grid_to_buttons():
    for int1 in range(0, len(grid)):
        list = grid[int1]
        for int2 in range(0, len(list)):
            string = list[int2]
            button = sg.Button(string, size = (3, 2), tooltip = "Index " + str(int2) + " " + str(int1))
            button.disabled_button_color = "#b3c9b9"
            list[int2] = button




def make_coords(x, y):
    coords = []
    if (x > 0):
        coords.append((x - 1, y))
        if (y > 0):
            coords.append((x - 1, y - 1))
        if (y < repeats - 1):
            coords.append((x - 1, y + 1))
    if (y > 0):
        coords.append((x, y - 1))
    if (x < repeats - 1):
        coords.append((x + 1, y))
        if (y > 0):
            coords.append((x + 1, y - 1))
        if (y < repeats - 1):
            coords.append((x + 1, y + 1))
    if (y < repeats - 1):
        coords.append((x, y + 1))
    return coords

    
def handle_input(x, y, letter): 
    global word 
    cleaned_letter = "".join([i for i in letter if not i.isdigit()])
    word += cleaned_letter

    print(word)

    coords = make_coords(x, y)
    for list in grid:
        for button in list:
           button.update(disabled=True)
    for coord in coords:
        x = coord[0]
        y = coord[1]
        list = grid[y]
        button = list[x]
        button.update(disabled=False)



def add_keys():
    for int1 in range(0, len(grid)):
        list = grid[int1]
        for int2 in range(0, len(list)):
            button=list[int2]
            handler = Handler(int2, int1, button.Key)
            button.Key=(handler.handle_input)
            print(str(int1) + str(int2))
          
def enable_all():
    for int1 in range(0, len(grid)):
        list = grid[int1]
        for int2 in range(0, len(list)):
            button=list[int2]
            button.update(disabled=False)

def update_score():
    global word
    global score
    for c in word:
        to_add = scores[c]
        score += to_add
    score_field.update(value=score)


def check_word():
    global word
    global word_field
    global words

    if wordnet.synsets(word):
        info_field.update(value="Nice work!")
        update_score()
    else:
        info_field.update(value="Sorry, that's not a real word.")
    word = ""
    word_field.update(value=word)



create_grid()
grid_to_buttons()

word_field = sg.Text(word, size=(25, 1), background_color="#FFFFFF", text_color="#0352fc")
info_field = sg.Text("Input a word.")
score_field = sg.Text(str(score))

layout = [[score_field], [info_field], [word_field], grid, [sg.Button('Clear'), sg.Button('Submit')]]
window = sg.Window(title="Wordify", layout=layout, margins=(100, 50), finalize=True)


add_keys()
wordnet.synsets("egg")



while True:
    event, values= window.read()
    
    if event == sg.WIN_CLOSED:
        break
    if callable(event):
        event()
        print(word)
        word_field.update(value=word)
    if event == 'Clear':
        word = ''
        word_field.update(value=word)
        enable_all()
    if event == 'Submit':
        check_word()
        enable_all()

