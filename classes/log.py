# def logFormat(message):
#     message = message.replace("<bggreen>", "\u001b[42;1m")
#     message = message.replace("<bgred>", "\u001b[41;1m")
#     message = message.replace("<bgwhite>", "\u001b[47;1m")
#     message = message.replace("<bgblue>", "\u001b[44;1m")
#     message = message.replace("<bgreversed>", "\u001b[7m")
#     message = message.replace("<underline>", "\u001b[4m")
#     message = message.replace("</bg>", "\u001b[0m")

#     message = message.replace("<black>", "\u001b[30m")
#     message = message.replace("<magenta>", "\u001b[35m")
#     message = message.replace("<cyan>", "\u001b[36m")
#     message = message.replace("<white>", "\u001b[37m")
#     message = message.replace("<yellow>", "\u001b[33m")
#     message = message.replace("<green>", "\033[92m")
#     message = message.replace("<blue>", "\033[94m")
#     message = message.replace("<red>", "\033[91m")
#     message = message.replace("<b>", "\033[1m")
#     message = message.replace("</>", "\033[0m")
#     return message

def logFormat(message):
    message = message.replace("<bggreen>", "")
    message = message.replace("<bgred>", "")
    message = message.replace("<bgwhite>", "")
    message = message.replace("<bgblue>", "")
    message = message.replace("<bgreversed>", "")
    message = message.replace("<underline>", "")
    message = message.replace("</bg>", "")

    message = message.replace("<black>", "")
    message = message.replace("<magenta>", "")
    message = message.replace("<cyan>", "")
    message = message.replace("<white>", "")
    message = message.replace("<yellow>", "")
    message = message.replace("<green>", "")
    message = message.replace("<blue>", "")
    message = message.replace("<red>", "")
    message = message.replace("<b>", "")
    message = message.replace("</>", "")
    return message


def write(message, type="normal"):
    if type == "normal":
        message = "----→ {}".format(message)
    if type == "error":
        message = "<bgred>• {}</bg>".format(message)
    elif type == "header":
        message = "<red>► {}</>".format(message)

    print(logFormat(message))
