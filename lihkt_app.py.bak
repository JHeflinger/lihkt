from os.path import exists
from datetime import datetime
from os import listdir

global commands
global appRunning
global fileName
global state

state = "MAIN"
defaultCommands = "\t\t help - brings up a list of commands \n\t\t quit - quits the application \n\t\t status - returns the status of the current resume"
mainCommands = "\t\t load - load a new .lkt file to handle \n\t\t create - create a new .lkt file \n\t\t delete - delete an existing file"
loadCommands = "\t\t unload - unload the current file \n\t\t edit - edit the current file \n\t\t generate - generate a new resume"
appRunning = True
fileName = ""

def mainLoop():
    com = getInput()
    handleCommands(com)
    
def handleCommands(com):
    global appRunning
    global fileName
    global state
    if com == "h" or com == "help":
        if state == "MAIN":
            sysPrint("Currently usable commands:\n" + defaultCommands + "\n" + mainCommands)
        elif state == "LOAD":
            sysPrint("Currently usable commands:\n" + defaultCommands + "\n" + loadCommands)
        else:
            sysPrint("CONSOLE ERROR: UNKOWN STATE. CLOSING APPLICATION.")
            appRunning = False
    elif com == "q" or com == "quit":
        sysPrint("Exiting application...")
        appRunning = False
    elif com == "s" or com == "status":
        sysPrint("STATUS: " + getStatus())
    else:
        if state == "MAIN":
            if com == "c" or com == "create":
                sysPrint("Welcome to resume creation! What would you like to name your new resume?")
                handleCreateFile()
                return
            if com == "l" or com == "load":
                sysPrint("Which file would you like to load? (If you'd like to see a list of available files, enter \"?browse\")")
                com = getInput("FILENAME: ")
                fileList = listdir("saves/")
                if com == "?browse":
                    sysPrint("Current available files:")
                    for f in fileList:
                        print("\t" + f.__str__())
                    com = getInput("FILENAME: ")
                if (com in fileList):
                    fileName = com
                    state = "LOAD"
                    sysPrint("Successfully loaded " + com + "! Additional commands are now available. Use \"h\" or \"help\" to view")
                else:
                    sysPrint("Error: filename entered was not found")
                return
        sysPrint("Invalid command. To bring up a list of available commands, use \"h\" or \"help\"")

def handleCreateFile():
    global fileName
    fileName = getInput("NAME: ")
    while len(fileName) <= 0 or ("\\" in fileName) or (":" in fileName) or ("*" in fileName) or ("?" in fileName) or ("\"" in fileName) or ("<" in fileName) or (">" in fileName) or ("|" in fileName):
        sysPrint("Invalid name detected. Please use a valid file name. (cannot include the characters \"\\\", \":\", \"*\", \"?\", \"\"\", \"<\", \">\", or \"|\")")
        fileName = getInput("NAME: ")
    fileName += ".lkt"
    filePath = "saves/" + fileName;
    if exists(filePath):
        sysPrint("WARNING: There is already a file under this name saved. Would you like to overwrite this file? (y/n)")
        yOrN = getYorN()
        if yOrN == "n":
            handleCreateFile()
            return
    with open(filePath, "w") as f:
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write("Last saved: " + date + "\n")
    sysPrint("Resume base successfully created! To edit or generate a resume from this file, load the file using the \"l\" or \"load\" command!")
        
def getStatus():
    if len(fileName) <= 0:
        return "No file currently uploaded. To begin resume creation/edit use the corresponding command."
    else:
        if state == "LOAD":
            return fileName + " is currently loaded and ready to edit."

def validateNum(str):
    num = -1
    try:
        num = int(str)
        if num >= 0:
            return num
        else:
            return -1
    except:
        return -1

def validateFloat(str):
    num = -1.0
    try:
        num = float(str)
        if num >= 0.0:
            return num
        else:
            return -1.0
    except:
        return -1.0

def getYorN():
    yOrN = getInput()
    while yOrN != "y" and yOrN != "n":
        sysPrint("invalid input recieved. Please type in \"y\" or \"n\".")
        yOrN = getInput()
    return yOrN

def sysPrint(output):
    print("SYSTEM >> " + output)

def getInput(str=""):
    print("USER << " + str, end="")
    return input()

sysPrint("Welcome to LIKHT! To begin, type in a valid command below. To get a list of commands, enter \"h\" or \"help\"!")
while(appRunning):
    mainLoop()