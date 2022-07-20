from os.path import exists
from datetime import datetime
from os import listdir
from os import remove
from pyautogui import typewrite
from fpdf import FPDF

global commands
global appRunning
global fileName
global state
global saved
global tempFile

state = "MAIN"
defaultCommands = "\t\t help - brings up a list of commands \n\t\t quit - quits the application \n\t\t info - returns the status of the current resume"
mainCommands = "\t\t load - load a new .lkt file to handle \n\t\t create - create a new .lkt file \n\t\t delete - delete an existing file"
loadCommands = "\t\t unload - unload the current file \n\t\t edit - edit the current file \n\t\t generate - generate a new resume \n\t\t view - view the contents of your file"
editCommands = "\t\t save - save changes to the file \n\t\t add - add an element to your resume \n\t\t remove - remove an element of your resume \n\t\t modify - modify an element to your resume \n\t\t finish - finish editing your resume \n\t\t view - view the contents of your file"
elements = []
fileElements = []
appRunning = True
saved = True
fileName = ""
tempFile = []

def mainLoop():
    com = getInput()
    handleCommands(com)
    
def handleCommands(com):
    global appRunning
    global fileName
    global state
    global tempFile
    global elements
    global saved
    global fileElements
    if fileName != "":
        if com == "v" or com == "view":
            miniSavedStr = ""
            if saved:
                miniSavedStr = "SAVED"
            else:
                miniSavedStr = "NOT SAVED"
            sysPrint(fileName + " currently reads as follows: ")
            print("\t STATUS: " + miniSavedStr)
            print("\t " + tempFile[0][0:len(tempFile[0]) - 1])
            for i in range(len(tempFile)):
                if i > 0:
                    print("\t " + tempFile[i][0:len(tempFile[i]) - 1])
            return
        elif com == "s" or com == "save":
            sysPrint("Saving file... Please do not exit the application or data may be corrupted")
            now = datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M:%S")
            tempFile[0] = "Last saved: " + date + "\n"
            with open("saves/" + fileName, "w") as f:
                f.writelines(tempFile)
            sysPrint("Saving finished!")
            saved = True
            return
    if com == "h" or com == "help":
        if state == "MAIN":
            sysPrint("Currently usable commands:\n" + defaultCommands + "\n" + mainCommands)
        elif state == "LOAD":
            sysPrint("Currently usable commands:\n" + defaultCommands + "\n" + loadCommands)
        elif state == "EDIT":
            sysPrint("Currently usable commands:\n" + defaultCommands + "\n" + editCommands)
        else:
            sysPrint("CONSOLE ERROR: UNKOWN STATE. CLOSING APPLICATION.")
            appRunning = False
    elif com == "q" or com == "quit":
        if saved == False:
            sysPrint("WARNING: you have unsaved work. Would you like to go back to save your work? (y/n)")
            yOrN = getYorN()
            if yOrN == "y":
                sysPrint("returning to menu...")
                return
        sysPrint("Exiting application...")
        appRunning = False
    elif com == "i" or com == "info":
        sysPrint("STATUS: " + getStatus())
    elif com == "debug":
        try:
            exec(getRawInput(getInput()))
        except:
            sysPrint("Unable to execute command.")
    else:
        if state == "MAIN":
            if com == "c" or com == "create":
                sysPrint("Welcome to resume creation! What would you like to name your new resume?")
                handleCreateFile()
                return
            elif com == "l" or com == "load":
                sysPrint("Which file would you like to load? (If you'd like to see a list of available files, enter \"?browse\")")
                com = getInput("FILENAME: ")
                fileList = listdir("saves/")
                while com == "?browse":
                    sysPrint("Current available files:")
                    for f in fileList:
                        print("\t" + f.__str__())
                    com = getInput("FILENAME: ")
                if (".lkt" in com) == False:
                    com += ".lkt"
                if (com in fileList):
                    fileName = com
                    with open("saves/" + fileName, "r") as f:
                        tempFile = f.readlines()
                    state = "LOAD"
                    sysPrint("Successfully loaded " + com + "! Additional commands are now available. Use \"h\" or \"help\" to view")
                else:
                    sysPrint("Error: filename entered was not found")
                return
            elif com == "d" or com == "delete":
                sysPrint("Which file would you like to delete? (If you'd like to see a list of available files, enter \"?browse\")")
                com = getInput("FILENAME: ")
                fileList = listdir("saves/")
                while com == "?browse":
                    sysPrint("Current available files:")
                    for f in fileList:
                        print("\t" + f.__str__())
                    com = getInput("FILENAME: ")
                if (com in fileList):
                    sysPrint("All information in this file will be permanently lost. Are you sure you want to delete " + com + "? (y/n)")
                    yOrN = getYorN()
                    if yOrN == "y":
                        remove("saves/" + com)
                        sysPrint("Successfully deleted " + com + "!")
                    else:
                        sysPrint("Cancelled file deletion.")
                else:
                    sysPrint("Error: filename entered was not found")
                return
        elif state == "LOAD":
            if com == "u" or com == "unload":
                sysPrint("Unloaded " + fileName + ". Available commands have changed. Use \"h\" or \"help\" to view")
                fileName = ""
                state = "MAIN"
                return
            elif com == "e" or com == "edit":
                sysPrint("You are now in EDIT mode. Available commands have been changed. Use \"h\" or \"help\" to view")
                state = "EDIT"
                return
            elif com == "g" or com == "generate":
                if saved == False:
                    sysPrint("ERROR: You have unsaved work. All work must be saved before generating.")
                    return
                generatePDF()
                return
        elif state == "EDIT":
            if com == "a" or com == "add":
                sysPrint("What element would you like to add? (If you'd like to see a list of available elements, enter \"?browse\")")
                com = getInput("ELEMENT: ")
                while com == "?browse":
                    sysPrint("Current available elements:")
                    for i in range(len(elements)):
                        print("\t" + elements[i])
                    com = getInput("ELEMENT: ")
                if (com in elements):
                    addElement(com)
                else:
                    sysPrint("Error: element entered was not found")
                return
            elif com == "f" or com == "finish":
                sysPrint("Returned to LOAD menu")
                state = "LOAD"
                return
            elif com == "r" or com == "remove":
                sysPrint("What element would you like to remove? (If you'd like to see a list of available elements, enter \"?browse\". If you'd like to see the contents as well, enter \"?superbrowse\".)")
                com = getInput("ELEMENT: ")
                getElements()
                while com == "?browse":
                    sysPrint("Current available elements:")
                    for i in range(len(fileElements)):
                        print("\t" + fileElements[i])
                    com = getInput("ELEMENT: ")
                while com == "?superbrowse":
                    sysPrint("Current available elements:")
                    for t in tempFile[1:len(tempFile)]:
                        print("\t " + t[0:len(t) - 1])
                    com = getInput("ELEMENT: ")
                if (com in fileElements):
                    removeElement(com)
                else:
                    sysPrint("Error: element entered was not found")
                return
            elif com == "m" or com == "modify":
                sysPrint("What element would you like to modify? (If you'd like to see a list of available elements, enter \"?browse\". If you'd like to see the contents as well, enter \"?superbrowse\".)")
                com = getInput("ELEMENT: ")
                getElements()
                while com == "?browse":
                    sysPrint("Current available elements:")
                    for i in range(len(fileElements)):
                        print("\t " + fileElements[i])
                    com = getInput("ELEMENT: ")
                while com == "?superbrowse":
                    sysPrint("Current available elements:")
                    for t in tempFile[1:len(tempFile)]:
                        print("\t " + t[0:len(t) - 1])
                    com = getInput("ELEMENT: ")
                if (com in fileElements):
                    modifyElement(com)
                else:
                    sysPrint("Error: element entered was not found")
                return
        sysPrint("Invalid command. To bring up a list of available commands, use \"h\" or \"help\"")

def generatePDF():
    global tempFile
    theme = ""
    sysPrint("Preparing file to generate...")
    if ("theme" in getElements()) == False:
        sysPrint("No theme element found in your current file. Would you like to add one? (y/n)")
        yOrN = getYorN()
        if yOrN == "y":
            sysPrint("Please enter your desired theme. If you'd like a list of available themes, enter \"?browse\")")
            com = getInput("THEME: ")
            fileList = listdir("themes/")
            while com == "?browse":
                sysPrint("Current available themes:")
                for f in fileList:
                    print("\t" + f.__str__()[0:f.__str__().index(".thm")])
                com = getInput("THEME: ")
            if (".thm" in com) == False:
                com += ".thm"
            if (com in fileList):
                tempFile.append("theme:" + com + "\n")
                now = datetime.now()
                date = now.strftime("%d/%m/%Y %H:%M:%S")
                tempFile[0] = "Last saved: " + date + "\n"
                with open("saves/" + fileName, "w") as f:
                    f.writelines(tempFile)
                sysPrint("Successfully added theme!")
            else:
                sysPrint("ERROR: invalid theme entered. Returning to menu...")
                return
        else:
            sysPrint("No valid theme detected. Using default theme...")
            theme = "default.thm"
    if theme != "default.thm":
        for s in tempFile:
            if "theme" in s:
                theme = s[6:len(s) - 1]
                break
    sysPrint("Generating PDF using " + theme + "...")
    fileList = listdir("themes/")
    if theme in fileList:
        themeContent = []
        pdf = FPDF()
        pdf.add_page()
        with open("themes/" + theme, "r") as f:
            themeContent = f.readlines()
        for t in themeContent:
            fullElement = t.split(":")
            qualifier = fullElement[0]
            define = fullElement[1].split(",")
            content = getContent(qualifier)
            content = getRawInput(content)
            if content != "" or qualifier == "manual_override":
                contentShards = content.split("\n")
                for c in contentShards:
                    if c == contentShards[len(contentShards) - 1]:
                        pdf.set_font(define[0], size = int(define[1]))
                        pdf.cell(w = int(define[2]), h = int(define[3]), txt = getRawInput(define[4]) + c, border = define[5], ln = int(define[6]), align = define[7], fill = define[8], link = define[9][0:len(define[9]) - 1])
                    else:
                        pdf.set_font(define[0], size = int(define[1]))
                        pdf.cell(w = int(define[2]), h = int(define[3]), txt = getRawInput(define[4]) + c, border = define[5], ln = 1, align = define[7], fill = define[8], link = define[9][0:len(define[9]) - 1])
        pdf.output("PDFs/lastgeneratedpdf.pdf")
        sysPrint("Finished generating PDF! What would you like to name your PDF? (leave blank to use .lkt filename)")
        pdfname = getInput("PDF NAME:")
        if pdfname == "":
            pdfname = fileName[0:len(fileName) - 4]
        while len(fileName) <= 0 or ("\\" in fileName) or (":" in fileName) or ("*" in fileName) or ("?" in fileName) or ("\"" in fileName) or ("<" in fileName) or (">" in fileName) or ("|" in fileName):
            sysPrint("Invalid name detected. Please use a valid file name. (cannot include the characters \"\\\", \":\", \"*\", \"?\", \"\"\", \"<\", \">\", or \"|\")")
            pdfname = getInput("PDF NAME:")
        pdf.output("PDFs/" + pdfname + ".pdf")
        sysPrint("Successfully generated pdf as " + pdfname + ".pdf! You can find your PDF in the PDFs folder!")
    else:
        sysPrint("ERROR: Could not load theme. Please make sure " + theme + " is inside your \"themes\" folder. Returning to menu...")

def modifyElement(com):
    global tempFile
    global saved
    index = 1
    for t in tempFile[1:len(tempFile)]:
        if t[0:t.index(":")] == com:
            sysPrint("Please enter your modifications below!")
            newContent = getPresetInput("MODIFY CONTENT BELOW: ", t[t.index(":") + 1:len(t) - 1])
            tempFile[index] = com + ":" + newContent + "\n"
            saved = False
            sysPrint("Sucessfully modified " + com + "!")
            return
        index += 1

def removeElement(com):
    global tempFile
    global saved
    for t in tempFile[1:len(tempFile)]:
        if t[0:t.index(":")] == com:
            tempFile.remove(t)
            saved = False
            sysPrint("Sucessfully removed " + com + "!")
            return

def getContent(con):
    global tempFile
    for t in tempFile[1:len(tempFile)]:
        if t[0:t.index(":")] == con:
            return t[t.index(":") + 1:len(t) - 1]
    return ""

def getElements():
    global tempFile
    global fileElements
    fileElements = []
    for t in tempFile[1:len(tempFile)]:
        fileElements.append(t[0:t.index(":")])
    return fileElements

def addElement(com):
    global tempFile
    global saved
    getElements()
    if com in fileElements:
        sysPrint("WARNING: this field has been detected to exist in your file already. Would you like to modify this field instead? (y/n)")
        yOrN = getYorN()
        if yOrN == "y":
            modifyElement(com)
            return
        else:
            sysPrint("Would you like to make an additional field instead? (y/n)")
            yOrN = getYorN()
            if yOrN == "n":
                sysPrint("Returning to menu...")
                return
    sysPrint("Adding " + com + " to resume! Please fill out the contents of this field")
    contents = getInput("CONTENTS: ")
    newField = com + ":" + contents + "\n"
    tempFile.append(newField)
    saved = False
    sysPrint("Successfully added! To view the contents of your current file, use the command \"v\" or \"view\"")

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
        if state == "LOAD" or state == "EDIT":
            if saved == True:
                return fileName + " is currently loaded and ready to edit!"
            else:
                return fileName + " is currently NOT SAVED. Make sure to save your work before exiting the application!"

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

def getRawInput(myInput):
    while "\\n" in myInput:
        myInput = myInput[0:myInput.index("\\n")] + "\n" + myInput[myInput.index("\\n") + 2:len(myInput)]
    while "\\t" in myInput:
        myInput = myInput[0:myInput.index("\\t")] + "    " + myInput[myInput.index("\\t") + 2:len(myInput)]
    return myInput

def getPresetInput(prompt, prefill=''):
    try:
        print("USER << " + prompt)
        typewrite(prefill)
        return input()
    except (ImportError, KeyError):
        import readline
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        print("ERROR")
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

def loadElements():
    global elements
    with open("settings/elements.stg", "r") as f:
        elements = f.readlines()
    for i in range(len(elements)):
        elements[i] = elements[i][0:len(elements[i]) - 1]

loadElements()
sysPrint("Welcome to LIKHT!\n\t -> You are currently using the WINDOWS version! \n\t -> To begin, type in a valid command below. To get a list of commands, enter \"h\" or \"help\"!")
while(appRunning):
    mainLoop()