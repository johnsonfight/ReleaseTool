from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import configparser
from SetConfig import Ui_SetConfig

ini_file = ''

class Ui_SelectIni(object):
	def setupUi(self, SelectIni):
		SelectIni.setObjectName("SelectIni")
		SelectIni.resize(480, 360)
		self.centralwidget = QtWidgets.QWidget(SelectIni)
		self.centralwidget.setObjectName("centralwidget")

		self.btn_ConfigFile = QtWidgets.QPushButton(self.centralwidget)
		self.btn_ConfigFile.setGeometry(QtCore.QRect(40, 140, 400, 60))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.btn_ConfigFile.setFont(font)
		self.btn_ConfigFile.setObjectName("btn_ConfigFile")
		self.btn_ConfigFile.clicked.connect(self.Btn_ConfigFile)

		SelectIni.setCentralWidget(self.centralwidget)
		self.retranslateUi(SelectIni)
		QtCore.QMetaObject.connectSlotsByName(SelectIni)

	def retranslateUi(self, SelectIni):
		_translate = QtCore.QCoreApplication.translate
		SelectIni.setWindowTitle(_translate("SelectIni", "SelectIni"))
		self.btn_ConfigFile.setText(_translate("SelectIni", "Select .ini file of your platform"))

	def openWindow(self, filename):
		self.window = QtWidgets.QMainWindow()
		self.ui = Ui_SetConfig(filename)
		self.ui.setupUi(self.window, filename)
		self.window.show()


	def getConfigFile(self):
		ini_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open config file' '', "*.ini")
		self.openWindow(ini_file)
		SelectIni.close()

	def Btn_ConfigFile(self):
		self.getConfigFile()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	SelectIni = QtWidgets.QMainWindow()
	ui = Ui_SelectIni()
	ui.setupUi(SelectIni)
	SelectIni.show()
	sys.exit(app.exec_())