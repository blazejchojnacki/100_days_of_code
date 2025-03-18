from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FR = 'French'
EN = 'English'

# CARD = {FR: {
#     'background': BACKGROUND_COLOR,
#     'image': card_recto
# }}
try:
    all_words_data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    all_words_data = pandas.read_csv("data/french_words.csv")
all_words = all_words_data.to_dict(orient="records")

remaining_words = all_words.copy()

current_word = {'a': 'b'}


def pick_new_word():
    global current_word, window_timer
    window.after_cancel(window_timer)
    current_word = random.choice(all_words)
    lang = FR
    card_canvas.itemconfig(card_side, image=card_recto_image)
    card_canvas.itemconfig(language_text, text=lang, fill='black')
    card_canvas.itemconfig(word_text, text=current_word[lang], fill='black')

    window_timer = window.after(3000, func=show_card)


def show_card():
    lang = EN
    card_canvas.itemconfig(card_side, image=card_verso_image)
    card_canvas.itemconfig(language_text, text=lang, fill='white')
    card_canvas.itemconfig(word_text, text=current_word[lang], fill='white')


def retain_card():
    pick_new_word()


def reject_card():
    global remaining_words
    for item in remaining_words:
        if item == current_word:
            remaining_words.remove(item)
    pick_new_word()


def save_retained_words():
    remaining_words_data = pandas.DataFrame(data=remaining_words)
    remaining_words_data.to_csv(path_or_buf="words_to_learn.csv", index=False, mode='w')


window = Tk()
window.title("Flashy")
window.minsize(width=800, height=600)
window.configure(background=BACKGROUND_COLOR, padx=50, pady=50)

window_timer = window.after(3000, func=show_card)

card_canvas = Canvas(master=window, bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
card_canvas.grid(row=1, column=1, columnspan=2)

card_recto_image = PhotoImage(file="images/card_front.png")
card_verso_image = PhotoImage(file="images/card_back.png")
card_side = card_canvas.create_image(400, 263, image=card_recto_image)

language_text = card_canvas.create_text(400, 150, text="language", font=("Ariel", 32, "italic"))
word_text = card_canvas.create_text(400, 263, text="word", font=("Ariel", 40, "bold"))

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(master=window, image=cross_image, highlightthickness=0, command=retain_card)
cross_button.grid(row=3, column=1)
check_image = PhotoImage(file="images/right.png")
check_button = Button(master=window, image=check_image, highlightthickness=0, command=reject_card)
check_button.grid(row=3, column=2)

pick_new_word()

window.mainloop()

save_retained_words()
