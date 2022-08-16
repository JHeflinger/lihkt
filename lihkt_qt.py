import lihkt
import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDialog,
    QFileDialog,
    QDialogButtonBox,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QFrame,
    QComboBox,
    QScrollArea,
    QMenu,
    QAction,
    QTabWidget,
    QShortcut)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.files = []
        self.setWindowTitle("LIHKT")
        self.resize(QSize(900, 500))
        self._createActions()
        self._connectActions()
        self._createMenuBar()
        self._createShortCuts()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
    
    def _createActions(self):
        self.newThemeAction = QAction("&New Theme", self)
        self.newContentAction = QAction("&New Content", self)
        self.openAction = QAction("&Open (ctrl+o)", self)
        self.importThemesAction = QAction("&Import Themes", self)
        self.importElementsAction = QAction("&Import Elements", self)
        self.saveAction = QAction("&Save (ctrl+s)", self)
        self.saveAsAction = QAction("&Save As", self)
        self.shellAction = QAction("&Shell (alt+s)", self)
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        newMenu = fileMenu.addMenu("New File...")
        newMenu.addAction(self.newThemeAction)
        newMenu.addAction(self.newContentAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        importMenu = fileMenu.addMenu("Import...")
        importMenu.addAction(self.importThemesAction)
        importMenu.addAction(self.importElementsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.shellAction)

    def _connectActions(self):
        #self.newThemeAction.triggered.connect(self.newFile)
        #self.newContentAction.triggered.connect(self.openFile)
        self.openAction.triggered.connect(self.openFile)
        #self.importThemesAction.triggered.connect(self.close)
        #self.importElementsAction.triggered.connect(self.copyContent)
        self.saveAction.triggered.connect(self.saveFile)
        #self.saveAsAction.triggered.connect(self.cutContent)
        self.shellAction.triggered.connect(self.openShell)
      
    def _createShortCuts(self):
        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_save.activated.connect(self.saveFile)
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.shortcut_open.activated.connect(self.openFile)
        self.shortcut_shell = QShortcut(QKeySequence('Alt+S'), self)
        self.shortcut_shell.activated.connect(self.openShell)
      
    def saveFile(self):
        self.tabs.currentWidget().save()
        
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Likht files (*.lkt *.thm)")
        self.files.append(fname)
        if fname[0] != "":
            self.tabs.addTab(ElementsTab(fname[0], self.tabs), fname[0].split("/")[len(fname[0].split("/")) - 1])
            
    def openShell(self):
        dlg = ShellDialog()
        if dlg.exec():
            try:
                exec(dlg.shellBox.toPlainText())
            except:
                dlg2 = notifyDialog("ERROR IN EXECUTING SCRIPT")
                dlg2.exec()

class notifyDialog(QDialog):
    def __init__(self, msg):
        super().__init__()
        self.setWindowTitle("Notification")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class ShellDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shell")
        QBtn = QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        title = QLabel("Enter Script:")
        self.shellBox = QTextEdit("")
        self.layout.addWidget(title)
        self.layout.addWidget(self.shellBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class ElementsTab(QWidget):
    def __init__(self, filepath, tabWidget):
        super().__init__()
        
        #file handling
        self.filepath = filepath
        self.filecontent = []
        self.elements = []
        with open(filepath, 'r') as file:
            self.filecontent = file.readlines()
        with open("settings/elements.lconf", 'r') as file:
            self.elements = file.readlines()
        
        #layout
        self.fileWidgets = {}
        self.layout = QVBoxLayout()
        self.tabWidget = tabWidget
        self.saved = True
        for element in self.elements:
        
            content = element.split(":")
            lineLayout = QHBoxLayout()
            type = content[0]
            header = content[1]
            lineLayout.addWidget(QLabel(header))
            
            elementContent = self.getContentFromElement(header)
            if len(elementContent) == 0:
                elementContent = [""]
                
            if type == "S":
                widget = QLineEdit(unfactorText(elementContent[0]))
                widget.textChanged.connect(self.unSave)
                self.fileWidgets[header] = widget
                lineLayout.addWidget(widget)
            elif type == "M":
                widget = QTextEdit(unfactorText(elementContent[0]))
                widget.textChanged.connect(self.unSave)
                self.fileWidgets[header] = widget
                lineLayout.addWidget(widget)
            elif type == "C":
                widget = ComplexElement(header, unfactorText(elementContent[0]), self)
                #widget.textChanged.connect(self.unSave)
                self.fileWidgets[header] = widget
                lineLayout.addWidget(widget)
                
            self.layout.addLayout(lineLayout)
            
        self.setLayout(self.layout)
        
    def getContentFromElement(self, element):
        contents = []
        for content in self.filecontent:
            if content.split(":")[0] == element:
                contents.append(content.split(":")[1])
        return contents
        
    def unSave(self):
        if self.saved:
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), self.tabWidget.tabText(self.tabWidget.currentIndex()) + "*")
            self.saved = False
            
    def save(self): #next to implement: multi elements,
        if not self.saved:
            with open(self.filepath, "w") as f:
                newFileContent = []
                for content in self.filecontent:
                    components = content.split(":")
                    element = components[0]
                    if element in self.fileWidgets:
                        newContent = ""
                        if isinstance(self.fileWidgets[element], QLineEdit):
                            newContent = element + ":" + refactorText(self.fileWidgets[element].text()) + ":\n"
                        else:
                            newContent = element + ":" + refactorText(self.fileWidgets[element].toPlainText()) + ":\n"
                        newFileContent.append(newContent)
                    else:
                        newFileContent.append(content)
                f.writelines(newFileContent)
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), self.tabWidget.tabText(self.tabWidget.currentIndex())[0:len(self.tabWidget.tabText(self.tabWidget.currentIndex())) - 1])
            self.saved = True

class ComplexElement(QWidget):
    def __init__(self, header, elementContent, parent):
        super().__init__()
        self.contents = elementContent.split("|")
        self.layout = QVBoxLayout()
        self.parentLayout = QVBoxLayout()
        self.parent = parent
        
        for content in self.contents:
            widget = QLineEdit(content)
            widget.textChanged.connect(self.parent.unSave)
            self.layout.addWidget(widget)
        
        addBtn = QPushButton("Add new " + header.lower())
        addBtn.clicked.connect(self.addContent)
        self.layout.addWidget(addBtn)
        self.parentLayout.addLayout(self.layout)
        self.parentLayout.addWidget(addBtn)
        self.setLayout(self.parentLayout)
        
    def addContent(self):
        widget = QLineEdit("")
        widget.textChanged.connect(self.parent.unSave)
        self.layout.addWidget(widget)

def refactorText(str):
    newStr = str.replace("\n", "\\n")
    newStr = newStr.replace(":", "\\;")
    return newStr
    
def unfactorText(str):
    newStr = str.replace("\\;", ":")
    newStr = newStr.replace("\\n", "\n")
    return newStr

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
