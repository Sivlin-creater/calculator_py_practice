import tkinter as tk
import math

# -----------------------------
# Calculator Buttons
# -----------------------------
button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

row_count = len(button_values)
column_count = len(button_values[0])

# -----------------------------
# Colors
# -----------------------------
color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

# -----------------------------
# Variables
# -----------------------------
A = ""
B = ""
operator = None

# -----------------------------
# Window
# -----------------------------
window = tk.Tk()
window.title("Calculator")
window.resizable(False, False)

frame = tk.Frame(window, bg=color_black)

label = tk.Label(
    frame,
    text="0",
    font=("Arial", 45),
    bg=color_black,
    fg=color_white,
    anchor="e",
    width=11,
    height=2
)

label.grid(row=0, column=0, columnspan=4, sticky="we")

# -----------------------------
# Functions
# -----------------------------


def clear_all():
    global A, B, operator
    A = ""
    B = ""
    operator = None


def remove_zero_decimal(num):
    if float(num).is_integer():
        return str(int(num))
    return str(round(num, 10)).rstrip("0").rstrip(".")


def update_display(text):
    label.config(text=text)

    length = len(text)

    if length <= 10:
        label.config(font=("Arial", 45))
    elif length <= 16:
        label.config(font=("Arial", 32))
    else:
        label.config(font=("Arial", 22))


def calculate():

    global A, B, operator

    if A == "" or B == "" or operator is None:
        return

    numA = float(A)
    numB = float(B)

    if operator == "+":
        result = numA + numB

    elif operator == "-":
        result = numA - numB

    elif operator == "×":
        result = numA * numB

    elif operator == "÷":

        if numB == 0:
            update_display("Error")
            clear_all()
            return

        result = numA / numB

    result = remove_zero_decimal(result)

    update_display(result)

    A = result
    B = ""
    operator = None


def button_clicked(value):
    global A, B, operator

    # ======================
    # Operators
    # ======================
    if value in right_symbols:

        if value == "=":

            calculate()

        else:

            # First operator
            if operator is None:

                A = label["text"]
                operator = value
                update_display(f"{A} {operator}")

            # Continuous calculation
            else:

                if B != "":

                    calculate()

                    operator = value
                    update_display(f"{A} {operator}")

    # ======================
    # Top buttons
    # ======================
    elif value in top_symbols:

        if value == "AC":

            clear_all()
            update_display("0")

        elif value == "+/-":

            if operator is None:

                try:
                    num = -float(label["text"])
                    update_display(remove_zero_decimal(num))
                except:
                    pass

            else:

                if B != "":

                    B = remove_zero_decimal(-float(B))
                    update_display(f"{A} {operator} {B}")

        elif value == "%":

            if operator is None:

                try:
                    num = float(label["text"]) / 100
                    update_display(remove_zero_decimal(num))
                except:
                    pass

            else:

                if B != "":

                    B = remove_zero_decimal(float(B) / 100)
                    update_display(f"{A} {operator} {B}")

    # ======================
    # Square Root
    # ======================
    elif value == "√":

        if operator is None:

            try:

                num = float(label["text"])

                if num < 0:
                    update_display("Error")
                    clear_all()
                    return

                update_display(remove_zero_decimal(math.sqrt(num)))

            except:
                update_display("Error")
                clear_all()

        else:

            if B != "":

                try:

                    num = float(B)

                    if num < 0:
                        update_display("Error")
                        clear_all()
                        return

                    B = remove_zero_decimal(math.sqrt(num))
                    update_display(f"{A} {operator} {B}")

                except:
                    update_display("Error")
                    clear_all()

    # ======================
    # Decimal
    # ======================
    elif value == ".":

        if operator is None:

            text = label["text"]

            if "." not in text:
                update_display(text + ".")

        else:

            if "." not in B:

                if B == "":
                    B = "0."
                else:
                    B += "."

                update_display(f"{A} {operator} {B}")

    # ======================
    # Numbers
    # ======================
    else:

        if operator is None:

            text = label["text"]

            if text == "0" or text == "Error":
                update_display(value)
            else:
                update_display(text + value)

        else:

            if B == "0":
                B = value
            else:
                B += value

            update_display(f"{A} {operator} {B}")


# -----------------------------
# Create Buttons
# -----------------------------
for row in range(row_count):
    for column in range(column_count):

        value = button_values[row][column]

        button = tk.Button(
            frame,
            text=value,
            font=("Arial", 30),
            width=4,
            height=1,
            borderwidth=0,
            command=lambda value=value: button_clicked(value)
        )

        if value in top_symbols:
            button.config(
                bg=color_light_gray,
                fg=color_black,
                activebackground=color_light_gray
            )

        elif value in right_symbols:
            button.config(
                bg=color_orange,
                fg=color_white,
                activebackground=color_orange
            )

        else:
            button.config(
                bg=color_dark_gray,
                fg=color_white,
                activebackground=color_dark_gray
            )

        button.grid(
            row=row + 1,
            column=column,
            padx=1,
            pady=1,
            sticky="nsew"
        )

# -----------------------------
# Configure Grid
# -----------------------------
for i in range(column_count):
    frame.grid_columnconfigure(i, weight=1)

for i in range(row_count + 1):
    frame.grid_rowconfigure(i, weight=1)

frame.pack(fill="both", expand=True)
frame.pack_propagate(False)

frame.config(width=320, height=480)

# -----------------------------
# Center Window
# -----------------------------
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width - window_width) / 2)
window_y = int((screen_height - window_height) / 2)

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# -----------------------------
# Run
# -----------------------------
window.mainloop()
