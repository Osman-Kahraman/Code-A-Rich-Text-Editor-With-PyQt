import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *


class RTE(QMainWindow):
    def __init__(self):
        super(RTE, self).__init__()
        self.editor = QTextEdit()
        self.font_ = QFont()
        self.fontSizeBox = QSpinBox()
        self.fontBox = QComboBox(self)
        
        font = QFont('Times', 24)
        self.editor.setFont(font)
        self.path = ""
        self.setCentralWidget(self.editor)
        self.setWindowTitle('Rich Text Editor')
        self.showMaximized()
        self.create_tool_bar()
        self.editor.setFontPointSize(24)
        
        
    def create_tool_bar(self):
        toolbar = QToolBar()
        
        save_action = QAction(QIcon('save.png'),'Save', self)
        save_action.triggered.connect(self.saveFile)
        toolbar.addAction(save_action)
        
        undoBtn = QAction(QIcon('undo.png'), 'undo', self)
        undoBtn.triggered.connect(self.editor.undo)
        toolbar.addAction(undoBtn)
        
        redoBtn = QAction(QIcon('redo.png'), 'redo', self)
        redoBtn.triggered.connect(self.editor.redo)
        toolbar.addAction(redoBtn)
        
        copyBtn = QAction(QIcon('copy.png'), 'copy', self)
        copyBtn.triggered.connect(self.editor.copy)
        toolbar.addAction(copyBtn)
        
        cutBtn = QAction(QIcon('cut.png'), 'cut', self)
        cutBtn.triggered.connect(self.editor.cut)
        toolbar.addAction(cutBtn)
        
        pasteBtn = QAction(QIcon('paste.png'), 'paste', self)
        pasteBtn.triggered.connect(self.editor.paste)
        toolbar.addAction(pasteBtn)
        
        self.fontSizeBox.setValue(24)
        self.fontSizeBox.valueChanged.connect(self.setFontSize)
        toolbar.addWidget(self.fontSizeBox)

        self.fontBox = QComboBox(self)
        self.fontBox.addItems(["Arial", "Bahnschrift", "Calibri", "Cambria", "Candara", "Comic Sans MS", "Consolas", "Courier", "Fixedsys", "Gadugi", "Georgia", "HoloLens MDL2 Assets", "Impact", "Ink Free", "Javanese Text", "MS Serif", "Times New Roman"])
        self.fontBox.activated.connect(self.setFont)
        toolbar.addWidget(self.fontBox)
        
        self.fontSizeBox.setValue(24)
        self.fontSizeBox.valueChanged.connect(self.setFontSize)
        toolbar.addWidget(self.fontSizeBox)
        
        self.rightAllign = QAction(QIcon('right-align.png'), 'Right Allign', self)
        self.rightAllign.triggered.connect(lambda : self.setAlignment(Qt.AlignRight))
        toolbar.addAction(self.rightAllign)
        
        self.leftAllign = QAction(QIcon('left-align.png'), 'Left Allign', self)
        self.leftAllign.triggered.connect(lambda : self.setAlignment(Qt.AlignLeft))
        toolbar.addAction(self.leftAllign)
        
        self.centerAllign = QAction(QIcon('center-align.png'), 'Center Allign', self)
        self.centerAllign.triggered.connect(lambda : self.setAlignment(Qt.AlignCenter))
        toolbar.addAction(self.centerAllign)
        
        self.color_btn = QAction(QIcon('app_images/color.png'), 'Color', self)
        self.color_btn.triggered.connect(self.setFontColor)
        toolbar.addAction(self.color_btn)

        toolbar.addSeparator()
        
        self.boldBtn = QAction(QIcon('bold.png'), 'Bold', self)
        self.boldBtn.triggered.connect(self.boldText)
        toolbar.addAction(self.boldBtn)
        
        self.underlineBtn = QAction(QIcon('underline.png'), 'underline', self)
        self.underlineBtn.triggered.connect(self.underlineText)
        toolbar.addAction(self.underlineBtn)
        
        self.italicBtn = QAction(QIcon('italic.png'), 'italic', self)
        self.italicBtn.triggered.connect(self.italicText)
        toolbar.addAction(self.italicBtn)
        
        
        self.addToolBar(toolbar)

    def setAlignment(self, pos):
        if pos == Qt.AlignCenter:
            if self.centerAllign.isChecked():
                self.centerAllign.setChecked(True)
        elif pos == Qt.AlignLeft:
            if self.leftAllign.isChecked():
                self.leftAllign.setChecked(True)
        else:
            if self.rightAllign.isChecked():
                self.rightAllign.setChecked(True)

        self.editor.setAlignment(pos)
    
    def setFontColor(self):
        picked_color = QColorDialog.getColor()
        R, G, B, A = picked_color.getRgb()

        self.editor.setTextColor(QColor(R, G, B, A))

    def setFontSize(self):
        value = self.fontSizeBox.value()
        self.editor.setFontPointSize(value)
        
    def setFont(self):
        font = self.fontBox.currentText()
        self.editor.setCurrentFont(QFont(font))    
        
    def italicText(self):
        if self.italicBtn.isChecked():
            self.italicBtn.setChecked(True)
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not(state)) 
    
    def underlineText(self):
        if self.underlineBtn.isChecked():
            self.underlineBtn.setChecked(True)
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not(state))   
        
    def boldText(self):
        if self.boldBtn.isChecked():
            self.boldBtn.setChecked(True)
        
        cursor = self.editor.textCursor()
        if cursor.charFormat().font().bold():
            self.editor.setFontWeight(QFont.Normal)
        else:
            self.editor.setFontWeight(QFont.Bold)       
    
    def saveFile(self):
        print(self.path)
        if self.path == '':
            self.file_saveas()
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)    
            
    def file_saveas(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "text documents (*.text);Text documents (*.txt);All files (*.*)")
        if self.path == '':
            return   
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)        
        
app = QApplication(sys.argv)
window = RTE()
window.show()
sys.exit(app.exec_())        
