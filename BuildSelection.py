from PyQt5 import QtCore, QtGui, QtWidgets
from releaseToolMain import *

class Ui_PlatformSelection(object):
    def setupUi(self, PlatformSelection):
        PlatformSelection.setObjectName("PlatformSelection")
        PlatformSelection.resize(350, 318)
        self.centralwidget = QtWidgets.QWidget(PlatformSelection)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(20, 40, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox))
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 70, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_2))
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 100, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_3))
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(20, 130, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_4))
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(20, 160, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_5))
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(20, 190, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_6.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_6))
        self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.setGeometry(QtCore.QRect(20, 220, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_7.setFont(font)
        self.checkBox_7.setObjectName("checkBox_7")
        self.checkBox_7.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_7))
        self.checkBox_8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_8.setGeometry(QtCore.QRect(20, 250, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_8.setFont(font)
        self.checkBox_8.setObjectName("checkBox_8")
        self.checkBox_8.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_8))
        self.checkBox_9 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_9.setGeometry(QtCore.QRect(20, 280, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_9.setFont(font)
        self.checkBox_9.setObjectName("checkBox_9")
        self.checkBox_9.stateChanged.connect(lambda:self.addOrRemoveElement(self.checkBox_9))
        PlatformSelection.setCentralWidget(self.centralwidget)


        self.retranslateUi(PlatformSelection)
        QtCore.QMetaObject.connectSlotsByName(PlatformSelection)

        if PlatformQueue.count(self.checkBox.text()) == 1:
            self.checkBox.setChecked(True)
        if PlatformQueue.count(self.checkBox_2.text()) == 1:
            self.checkBox_2.setChecked(True)
        if PlatformQueue.count(self.checkBox_3.text()) == 1:
            self.checkBox_3.setChecked(True)
        if PlatformQueue.count(self.checkBox_4.text()) == 1:
            self.checkBox_4.setChecked(True)
        if PlatformQueue.count(self.checkBox_5.text()) == 1:
            self.checkBox_5.setChecked(True)
        if PlatformQueue.count(self.checkBox_6.text()) == 1:
            self.checkBox_6.setChecked(True)
        if PlatformQueue.count(self.checkBox_7.text()) == 1:
            self.checkBox_7.setChecked(True)
        if PlatformQueue.count(self.checkBox_8.text()) == 1:
            self.checkBox_8.setChecked(True)
        if PlatformQueue.count(self.checkBox_9.text()) == 1:
            self.checkBox_9.setChecked(True)

    def addOrRemoveElement(self,cb):
        if cb.isChecked() == True and PlatformQueue.count(cb.text()) < 1:
            PlatformQueue.append(cb.text())
        elif cb.isChecked() == False and PlatformQueue.count(cb.text()) == 1:
            PlatformQueue.remove(cb.text())


    def retranslateUi(self, PlatformSelection):
        _translate = QtCore.QCoreApplication.translate
        PlatformSelection.setWindowTitle(_translate("PlatformSelection", "PlatformSelection"))
        self.checkBox.setText(_translate("PlatformSelection", "Atlas"))
        self.checkBox_2.setText(_translate("PlatformSelection", "Cosmos"))
        self.checkBox_3.setText(_translate("PlatformSelection", "Odyssey"))
        self.checkBox_4.setText(_translate("PlatformSelection", "Pathfinder"))
        self.checkBox_5.setText(_translate("PlatformSelection", "Sojourner"))
        self.checkBox_6.setText(_translate("PlatformSelection", "Taurus"))
        self.checkBox_7.setText(_translate("PlatformSelection", "Spitzer"))
        self.checkBox_8.setText(_translate("PlatformSelection", "Ulysses"))
        self.checkBox_9.setText(_translate("PlatformSelection", "Shoemaker"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PlatformSelection = QtWidgets.QMainWindow()
    ui = Ui_PlatformSelection()
    ui.setupUi(PlatformSelection)
    PlatformSelection.show()
    sys.exit(app.exec_())
