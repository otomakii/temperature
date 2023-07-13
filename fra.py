from tkinter import *
from functools import partial


class Converter:

    def __init__(self):

        # Initialise variables (such as the feedback variable)
        self.to_help = ""
        self.var_feedback = StringVar()
        self.var_feedback.set("")
        self.var_has_error = StringVar()
        self.var_has_error.set("no")
        self.all_calculation = []

        # format for buttons
        # font(Quicksand),size(14),type(bold)
        button_font = ("Quicksand", "10", "bold")

        # Gui frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Converter",
                                  font=("Quicksand", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)

        instructions = "Please enter a temperature below, " \
                       "then press one of the buttons to convert " \
                       "it from centigrade to Fahrenheit or vise versa."
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wraplength=250, width=50,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Quicksand", "14")
                                )
        self.temp_entry.grid(row=2, padx=10, pady=10)

        "Please enter a number"
        self.output_label = Label(self.temp_frame, text="",
                                  fg="red")
        self.output_label.grid(row=3)

        # Conversion, help and history/export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        self.to_celsius_button = Button(self.button_frame,
                                        text="To Degrees C",  # what the text says
                                        bg="royal blue",  # behind the text colour
                                        fg="black",
                                        font=button_font, width=12,  # text colour
                                        command=lambda: self.temp_convert(-459))
        self.to_celsius_button.grid(row=0, column=0, padx=5, pady=5)  # where the button is positioned

        self.to_fahrenheit_button = Button(self.button_frame,
                                           text="To Degrees F",  # what the text says
                                           bg="red",  # behind the text colour
                                           fg="black",
                                           font=button_font, width=12,  # text colour
                                           command=lambda: self.temp_convert(-273))
        self.to_fahrenheit_button.grid(row=0, column=1, padx=5, pady=5)  # where the button is positioned

        self.to_history_button = Button(self.button_frame,
                                        text="History / Export",
                                        bg="dark gray",
                                        fg="black",
                                        font=button_font, width=12)
        self.to_history_button.grid(row=1, column=0, padx=5, pady=5)

        self.to_help_button = Button(self.button_frame,
                                     text="Help / Info",
                                     bg="dark gray",
                                     fg="black",
                                     font=button_font, width=12,
                                     command=self.to_help)
        self.to_help_button.grid(row=1, column=1, padx=5, pady=5)

    # checks user input and if it's valid, converts temperature
    def check_temp(self, min_value):

        has_error = "no"
        error = "Please enter a number that is more" \
                " than {}".format(min_value)

        response = self.temp_entry.get()

        # checks for valid number
        try:
            response = float(response)

            if response < min_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"
        else:
            self.var_has_error.set("no")

            return response

    @staticmethod
    def round_ans(val):
        var_rounded = (val * 2 + 1) // 2
        return "{:.0f}".format(var_rounded)

    # check temperature is valid and convert it
    def temp_convert(self, min_val):
        to_convert = self.check_temp(min_val)
        deg_sign = u'\N{DEGREE SIGN}'
        set_feedback = "yes"
        answer = ""
        from_to = ""

        if to_convert == "invalid":
            set_feedback = "no"

        # Convert to Celsius
        elif min_val == -459:
            answer = (to_convert - 32) * 5 / 9
            from_to = "{} F{} is {} C{}"

        # convert to Fahrenheit
        else:
            answer = to_convert * 1.8 + 32
            from_to = "{} C{} is {} F{}"

        if set_feedback == "yes":
            to_convert = self.round_ans(to_convert)
            answer = self.round_ans(answer)

            feedback = from_to.format(to_convert, deg_sign,
                                      answer, deg_sign)
            self.var_feedback.set(feedback)

            self.all_calculation.append(feedback)
            print(self.all_calculation)

        self.output_answer()

    # check temperature is more than -273 and convert it
    # redy for next calculation
    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            self.output_label.config(fg="red")
            self.temp_entry.config(bg="white")
        else:
            self.output_label.config(fg="green")
            self.temp_entry.config(bg="white")

        self.output_label.config(text=output)

    def to_help(self):
        DisplayHelp(self)


class DisplayHelp:

    def __init__(self, partner):

        # setup dialogue box
        background = "white"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_button.config(state=DISABLED)

        # user
        # release
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box,
                                width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help / Info",
                                        font=("Quicksand", "14"))
        self.help_heading_label.grid(row=0)

        help_text = "To use the program simply enter the temperature\r" \
                    "you wish to convert and then choose to convert\r" \
                    "to either degrees Celsius or Fahrenheit\r" \
                    "Note that -273 degrees C, -459 F is absolute zero\r" \
                    "If you try to convert a temperature that is less\r" \
                    "than that you will get an error message.\r" \
                    "To see your calculation history and export it\r" \
                    "to a text file, please click the History/Export button"
        self.help_text_Label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_Label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Quicksand", "14"),
                                     text="Dismiss", bg="gray",
                                     fg="black",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue used by button and x at top of dialogue.
    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# --Main Routine--
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.resizable(False, False)
    root.mainloop()
