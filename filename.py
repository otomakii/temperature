from datetime import date
import re


# if filename is blank, return to default name
# Otherwise check filename and either return
# an error or return the filename with ".txt" extension
def filename_maker(filename):
    if filename == "":

        filename_ok == ""
        date_part = get_date()
        filename = "{}_temperature_calculations".format(date_part)

    else:
        filename_ok = check_filename(filename)

    if filename_ok == "":
        filename += ".txt"

    else:
        filename = filename_ok

    return filename


# retrieve date
def get_date():
    today = date.today()

    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%y")

    return "{}_{}_{}".format(year, month, day)


# check filename only contains letters, numbers, underscores
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

