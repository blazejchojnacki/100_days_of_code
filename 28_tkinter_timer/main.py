from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
# SESSION = ["reset", WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, SHORT_BREAK_MIN,
#            WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN]
SECONDS = 0.2  # 60
step = 0
check_mark = ""

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global step, check_mark
    step = 0
    check_mark = ""
    check_mark_label.config(text=check_mark)
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")

# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    global step, check_mark
    step += 1
    step_time = 0
    if step % 2 == 0 and step > 0 and step % 8 != 0:
        step_time = SHORT_BREAK_MIN
        # count_down(SHORT_BREAK_MIN)
        check_mark += " v "
        check_mark_label.config(text=check_mark)
        title_label.config(text="break", fg=PINK)
    elif step % 8 == 0:
        step_time = LONG_BREAK_MIN
        # count_down(LONG_BREAK_MIN)
        title_label.config(text="long break", fg=PINK)
        reset_timer()
    else:
        step_time = WORK_MIN
        # count_down(WORK_MIN)
        title_label.config(text="work", fg=RED)
    count_down(int(step_time * SECONDS))


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    if count % 60 < 10:
        time_format = f"{int((count - count % 60) / 60)}:0{count % 60}"
    else:
        time_format = f"{int((count - count % 60) / 60) }:{count % 60}"
    canvas.itemconfig(timer_text, text=time_format)
    if count >= 0 and step != 0:
        window.after(1000, count_down, count - 1)
    elif step == 0:
        reset_timer()
    elif step != 0:
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=2, column=2)

title_label = Label(text="Timer", font=(FONT_NAME, 50), fg=GREEN, bg=YELLOW)
title_label.grid(row=1, column=2)

start_button = Button(text="start", highlightthickness=0, command=start_timer)
start_button.grid(row=3, column=1)

reset_button = Button(text="reset", highlightthickness=0, command=reset_timer)
reset_button.grid(row=3, column=3)

check_mark_label = Label(text=check_mark, fg=GREEN, bg=YELLOW)
check_mark_label.grid(row=4, column=2)

window.mainloop()
