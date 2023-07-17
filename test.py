from tkinter import *
from functools import partial
from datetime import date
import re


class Converter:

    def __init__(self):
        # format for buttons
        # font(Quicksand),size(14),type(bold)
        button_font = ("Quicksand", "12", "bold")

        self.all_calculations = ['0 F is -18 C', '0 C is 32 F',
                                 '30 F is -1 C', '30 C is 86 F',
                                 '40 F is 4 C']
        # Gui frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.button_frame = Frame(padx=30, pady=30)
        self.button_frame.grid(row=0)

        self.to_history_button = Button(self.button_frame,
                                        text="History / Export",
                                        bg="dark gray",
                                        fg="black",
                                        font=button_font, width=12,
                                        command=lambda: self.to_history(self.all_calculations))
        self.to_history_button.grid(row=1, column=1, padx=5, pady=5)

    def to_history(self, all_calculations):
        HistoryExport(self, all_calculations)


class HistoryExport:

    def __init__(self, partner, calc_list):

        max_calcs = 5
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        self.var_filename = StringVar()
        self.var_todays_date = StringVar()
        self.var_calc_list = StringVar()

        self.get_calc_string(calc_list)
        # setup dialogue box
        self.history_box = Toplevel()

        # disable help
        partner.to_history_button.config(state=DISABLED)

        # user
        # release
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300,
                                   height=200)
        self.history_frame.grid()

        self.history_heading_label = Label(self.history_frame,
                                           text="History / Export",
                                           font=("Quicksand", "12"))
        self.history_heading_label.grid(row=0)

        history_text = "Below is your calculation history \r" \
                       "showing 5 / 5 calculations. Please export \r" \
                       "your calculations to see your full history \r" \
                       " \r" \
                       "All calculations are shown to the nearest degree"
        self.text_instructions_label = Label(self.history_frame,
                                             text=history_text,
                                             width=45, justify="left",
                                             wraplength=300,
                                             padx=10, pady=10)
        self.text_instructions_label.grid(row=1)

        self.all_calcs_label = Label(self.history_frame,
                                     text="calculations go here",
                                     padx=10, pady=10, bg="light gray",
                                     width=40, justify="left")
        self.all_calcs_label.grid(row=2)

        # instructions for saving files
        save_text = "Either choose a custom file name and push <Export> \r" \
                    "or simply push <Export> to save your calculations \r" \
                    "in a text file. If the filename already exists \r" \
                    "it will be OVERWRITTEN."
        self.save_instructions_label = Label(self.history_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=3)

        # filename entry widget
        self.filename_entry = Entry(self.history_frame,
                                    font=("quicksand", "12"),
                                    bg="light gray", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_error_label = Label(self.history_frame,
                                          text="Filename error goes here",
                                          fg="black",
                                          font=("quicksand", "12"))
        self.filename_error_label.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame,
                                    font=("quicksand", "12"),
                                    text="Export", bg="light gray",
                                    fg="black", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame,
                                     font=("quicksand", "12"),
                                     text="Dismiss", bg="light gray",
                                     fg="black", width=12,
                                     command=partial(self.close_history, partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

    # change calculation list into a string
    def get_calc_string(self, var_calculations):

        max_calcs = self.var_max_calcs.get()
        calc_string = ""

        oldest_first = ""
        for item in var_calculations:
            oldest_first += item
            oldest_first += "\n"

        self.var_calc_list.set(oldest_first)

        if len(var_calculations) >= max_calcs:
            stop = max_calcs

        else:
            stop = len(var_calculations)

        for item in range(0, stop - 1):
            calc_string += var_calculations[len(var_calculations)
                                            - item - 1]
            calc_string += "\n"

        calc_string += var_calculations[-max_calcs]

        return calc_string

    def make_file(self):
        filename = self.filename_entry.get()

        filename_ok = ""
        date_part = self.get_date()

        if filename == "":
            filename = "{}_temperature_calculations".format(date_part)

        else:
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            success = "Your calculations have \r" \
                      "been saved (filename: {})".format(filename)
            self.var_filename.set(filename)
            self.filename_feedback_label.config(text=success,
                                                fg="dark green")
            self.filename_entry.config(bg="white")

            self.write_to_file()

        else:
            self.filename_error_label.config(text=filename_ok,
                                             fg="red")
            self.filename_error_label.config(bg="pink")

    # retrieves date
    def get_date(self):
        today = date.today()

        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%y")

        todays_date = "{}/{}/{}".format(day, month, year)
        self.var_todays_date.set(todays_date)

        return "{}_{}_{}".format(year, month, day)

    @staticmethod
    def check_filename(filename):
        problem = ""

        valid_char = "[A-Za-z0-9_]"

        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry, no spaces allowed"

            else:
                problem = ("Sorry, no {}'s allowed".format(letter))

            break

        if problem != "":
            problem = "{}. Use letter / numbers /\r" \
                      "underscores only.".format(problem)

        return problem

    # closes help dialogue
    def close_history(self, partner):

        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# --Main Routine--
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.resizable(False, False)
    root.mainloop()

