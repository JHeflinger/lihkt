import lihkt
import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
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
    QTabWidget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.files = []
        self.setWindowTitle("LIHKT")
        self.setFixedSize(QSize(300, 300))
        self._createActions()
        self._connectActions()
        self._createMenuBar()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
    
    def _createActions(self):
        self.newThemeAction = QAction("&New Theme", self)
        self.newContentAction = QAction("&New Content", self)
        self.openAction = QAction("&Open", self)
        self.importThemesAction = QAction("&Import Themes", self)
        self.importElementsAction = QAction("&Import Elements", self)
        self.saveAction = QAction("&Save", self)
        self.saveAsAction = QAction("&Save As", self)
        self.shellAction = QAction("&Shell", self)
    
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
        #self.saveAction.triggered.connect(self.pasteContent)
        #self.saveAsAction.triggered.connect(self.cutContent)
        self.shellAction.triggered.connect(self.openShell)
        
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Likht files (*.lkt *.thm)")
        self.files.append(fname)
        if fname[0] != "":
            self.tabs.addTab(ElementsTab(fname[0]), fname[0].split("/")[len(fname[0].split("/")) - 1])
            
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
    def __init__(self, filepath):
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
        self.layout = QVBoxLayout()
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
                lineLayout.addWidget(QLineEdit(elementContent[0]))
            elif type == "M":
                print("yo implement multiple elements boyeeee")
            self.layout.addLayout(lineLayout)
            
        self.setLayout(self.layout)
        
    def getContentFromElement(self, element):
        contents = []
        for content in self.filecontent:
            if content.split(":")[0] == element:
                contents.append(content.split(":")[1])
        return contents

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
