import pandas
from tkinter import messagebox
import turtle

# created screen obj
screen = turtle.Screen()
screen.setup(725, 491)
screen.title("U.S. States Games")

# imported object image
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

# data read from CSV
data = pandas.read_csv("./50_states.csv")
list_states = data.state.to_list()

# Empty list to record entered states
answer_list = []

game_on = True
# loop for game seq.
while game_on:
    try:
        user_answer = screen.textinput(title=f"{len(answer_list)}/50 State names memorization game",
                                       prompt="Write name of a USA state or type 'stop' to end the game:")
        answer_state = user_answer.title()

        if answer_state in list_states:
            answer_list.append(answer_state)
            if len(answer_list) == 50:
                game_on = False

        if answer_state.lower() == "stop":
            game_on = False

        state_row = data[data.state == answer_state]

        new_x = int(state_row.x)
        new_y = int(state_row.y)

        another_turtle = turtle.Turtle()
        another_turtle.hideturtle()
        another_turtle.penup()
        another_turtle.goto(new_x, new_y)
        another_turtle.write(f"{state_row.state.item()}", align="center", font=("Courier", 8, "bold"))
    # Needed to keep broad except
    except TypeError:
        continue

missed_states_list = [missed_states for missed_states in list_states if missed_states not in answer_list]

dictionary_missed_states = {
    "states": missed_states_list
}
# Creating dataframe of missed states from dictionary
data_frame = pandas.DataFrame(dictionary_missed_states)
# Saving of state names that were not typed, saved into a new CSV file from dataframe
data_frame.to_csv("./states_names_you_missed.csv", index=False)

try:
    list_missed_states = pandas.read_csv('./states_names_you_missed.csv')
    list_m_states = list_missed_states["states"].tolist()
    formatted_series = "\n".join(f"{states}" for states in list_m_states)
except FileNotFoundError:
    # If no file created due to not typing any states name
    messagebox.showinfo(title="Message", message="You did not enter any name of a USA state.")
else:
    # formatted_series is already defined in the try block if the file was read successfully
    messagebox.showinfo(title="   Missed States list   ", message=f"Name of the states that you need to "
                                                                  f"memorize: \n\n{formatted_series}")
# Game over seq.
turtle.write("Game Over", align="center", font=("Courier", 30, "bold"))

turtle.mainloop()
