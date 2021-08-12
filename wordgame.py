from random import randint
from tkinter.constants import X
import string
import PySimpleGUI as sg
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

alphabet_dict = list(string.ascii_uppercase)
repeats = 5
word = ""
#checker = new SpellChecker


grid = []
preserved_grid = []

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
        index = randint(1, 26)
        list.append(alphabet_dict[index - 1])
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

def check_word():
    global word
    global word_field
    global words

    if wordnet.synsets(word):
        info_field.update(value="Nice work!")
    else:
        info_field.update(value="Sorry, that's not a real word.")
    word = ""
    word_field.update(value=word)


create_grid()
grid_to_buttons()

word_field = sg.Text(word, size=(25, 1), background_color="#FFFFFF", text_color="#0352fc")
info_field = sg.Text("Input a word.")

layout = [[info_field], [word_field], grid, [sg.Button('Clear'), sg.Button('Submit')]]
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

