# Entrypoint for webpage
from pyscript import *
import sys

inputval = ""
outputval = ""


# Redirect IO to text area
def newread(*_):
    global inputval
    if not inputval:
        return ""
    t = inputval[0]
    inputval = inputval[1:]
    return t


def newreadline():
    t = ""
    while 1:
        c = newread()
        if c == "" or c == "\n":
            break
        t += c
    return t


def newwrite(x):
    global outputval
    outputval += x


setattr(sys.stdin, "read", newread)
setattr(sys.stdout, "write", newwrite)
setattr(sys.stdin, "readline", newreadline)


@when("click", "#run")
def execute(event):
    global inputval, outputval
    outputval = ""
    code = document.querySelector("#code").value
    inputval = document.querySelector("#input").value
    try:
        stack_based(code, 5)
    except:
        pass
    document.querySelector("#output").value = outputval
