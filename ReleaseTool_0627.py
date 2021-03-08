# import sys
# print(sys.path)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from releaseToolMain import *
from BuildSelection import Ui_PlatformSelection

class Ui_MainWindow(object):
    def __init__(self, filename):
        f = Functions()
        f.read_config(filename)
        f.Prepare_for_repo()
        repo = git.Repo(INI[0]['repo_dell'])


    def Run_Button1(self):
        # if self.CB_scanCPI.isChecked():
        #     for p in PlatformQueue:
        #         f.scan_CPI(p)
        #     pass
        if self.CB_CpCPI.isChecked():
            for p in PlatformQueue:
                f.cherrypick_CPI(p)
            pass
        if self.CB_DellBiosVersion.isChecked():
            for p in PlatformQueue:
                f.edit_BV(p, BV_list_keywords)
            pass
        if self.CB_PlatformConfig.isChecked():
            for p in PlatformQueue:
                f.edit_PC(p, DM_list_keywords)
            pass

        f.check_before_POT()


    def Run_Button2(self):
        for p in PlatformQueue:
            if self.CB_BlockBranch.isChecked():
                f.commit_n_push_block_branch(p)
                pass
        for p in PlatformQueue:
            if self.CB_Branch_Tag.isChecked():
                for p in PlatformQueue:
                    f.create_rel_branch(p)
                    f.create_rel_tag(p)
                pass
        for p in PlatformQueue:
            if self.CB_RunBatch.isChecked():
                f.build_n_release(p)
                pass
        for p in PlatformQueue:
            if self.CB_ToSVN.isChecked():
                f.upload_to_svn(p)
                pass
            # if self.CB_Rename.isChecked():
            #     f.rename_EFI_withSWB()

    def Run_Button3(self):
        DUP_Checkbox = True
        if self.CB_CreateMail.isChecked():
            if self.radioButton.isChecked() == True:
                DUP_Checkbox = True
            else:
                DUP_Checkbox = False
            for p in PlatformQueue:
                RN_obj = f.read_existing_RN(read_RN[p], p)
                f.create_release_mail(RN_obj, p, DUP_Checkbox)
            pass
        for p in PlatformQueue:
            if self.CB_pushBranchTag.isChecked():
                for p in PlatformQueue:
                    f.push_branch_tag(p)
                pass
                    
    def show_popup(self):
        self.openWindow()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 460)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1100, 700, 81, 61))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Users/Johnson_Nieh/Users/Johnson_Nieh/.designer/backup/PLicon.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 40, 800, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 100, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        # self.CB_ReadRN = QtWidgets.QCheckBox(self.centralwidget)
        # self.CB_ReadRN.setGeometry(QtCore.QRect(840, 160, 221, 20))
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # self.CB_ReadRN.setFont(font)
        # self.CB_ReadRN.setIconSize(QtCore.QSize(24, 24))
        # self.CB_ReadRN.setChecked(True)
        # self.CB_ReadRN.setObjectName("CB_ReadRN")


        #
        # Run 1
        #
        # self.CB_scanCPI = QtWidgets.QCheckBox(self.centralwidget)
        # self.CB_scanCPI.setGeometry(QtCore.QRect(40, 160, 280, 20))
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # self.CB_scanCPI.setFont(font)
        # self.CB_scanCPI.setIconSize(QtCore.QSize(24, 24))
        # self.CB_scanCPI.setChecked(False)
        # self.CB_scanCPI.setObjectName("CB_scanCPI")

        self.CB_CpCPI = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_CpCPI.setGeometry(QtCore.QRect(40, 160, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_CpCPI.setFont(font)
        self.CB_CpCPI.setIconSize(QtCore.QSize(24, 24))
        self.CB_CpCPI.setChecked(False)
        self.CB_CpCPI.setObjectName("CB_CherryPick CPI")

        self.CB_DellBiosVersion = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_DellBiosVersion.setGeometry(QtCore.QRect(40, 200, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_DellBiosVersion.setFont(font)
        self.CB_DellBiosVersion.setIconSize(QtCore.QSize(24, 24))
        self.CB_DellBiosVersion.setChecked(True)
        self.CB_DellBiosVersion.setObjectName("CB_DellBiosVersion")

        self.CB_PlatformConfig = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_PlatformConfig.setGeometry(QtCore.QRect(40, 240, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_PlatformConfig.setFont(font)
        self.CB_PlatformConfig.setIconSize(QtCore.QSize(24, 24))
        self.CB_PlatformConfig.setChecked(True)
        self.CB_PlatformConfig.setObjectName("CB_PlatformConfig")

        #
        # Run 2
        #
        self.CB_BlockBranch = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_BlockBranch.setGeometry(QtCore.QRect(430, 160, 361, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_BlockBranch.setFont(font)
        self.CB_BlockBranch.setIconSize(QtCore.QSize(24, 24))
        self.CB_BlockBranch.setChecked(True)
        self.CB_BlockBranch.setObjectName("CB_BlockBranch")

        self.CB_Branch_Tag = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_Branch_Tag.setGeometry(QtCore.QRect(430, 200, 361, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_Branch_Tag.setFont(font)
        self.CB_Branch_Tag.setIconSize(QtCore.QSize(24, 24))
        self.CB_Branch_Tag.setChecked(True)
        self.CB_Branch_Tag.setObjectName("CB_Branch_Tag")

        self.CB_RunBatch = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_RunBatch.setGeometry(QtCore.QRect(430, 240, 361, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_RunBatch.setFont(font)
        self.CB_RunBatch.setIconSize(QtCore.QSize(24, 24))
        self.CB_RunBatch.setChecked(True)
        self.CB_RunBatch.setObjectName("CB_RunBatch")

        self.CB_ToSVN = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_ToSVN.setGeometry(QtCore.QRect(430, 280, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_ToSVN.setFont(font)
        self.CB_ToSVN.setIconSize(QtCore.QSize(24, 24))
        self.CB_ToSVN.setChecked(True)
        self.CB_ToSVN.setObjectName("CB_ToSVN")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(430, 100, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")



        # self.CB_Tag = QtWidgets.QCheckBox(self.centralwidget)
        # self.CB_Tag.setGeometry(QtCore.QRect(40, 320, 241, 20))
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # self.CB_Tag.setFont(font)
        # self.CB_Tag.setIconSize(QtCore.QSize(24, 24))
        # self.CB_Tag.setChecked(True)
        # self.CB_Tag.setObjectName("CB_Tag")



        #
        # Run 3
        #
        self.CB_CreateMail = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_CreateMail.setGeometry(QtCore.QRect(840, 160, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_CreateMail.setFont(font)
        self.CB_CreateMail.setIconSize(QtCore.QSize(24, 24))
        self.CB_CreateMail.setChecked(True)
        self.CB_CreateMail.setObjectName("CB_CreateMail")


        self.CB_pushBranchTag = QtWidgets.QCheckBox(self.centralwidget)
        self.CB_pushBranchTag.setGeometry(QtCore.QRect(840, 200, 361, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_pushBranchTag.setFont(font)
        self.CB_pushBranchTag.setIconSize(QtCore.QSize(24, 24))
        self.CB_pushBranchTag.setChecked(True)
        self.CB_pushBranchTag.setObjectName("CB_pushBranchTag")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(840, 100, 471, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")

        #
        # Button
        #
        self.btn_pop_window = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pop_window.setGeometry(QtCore.QRect(670, 38, 26, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_pop_window.setFont(font)
        self.btn_pop_window.setObjectName("btn_pop_window")
        self.btn_pop_window.clicked.connect(self.show_popup)

        self.btn_Run1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Run1.setGeometry(QtCore.QRect(40, 320, 112, 34))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_Run1.setFont(font)
        self.btn_Run1.setObjectName("btn_Run1")
        self.btn_Run1.clicked.connect(self.Run_Button1)

        self.btn_Run2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Run2.setGeometry(QtCore.QRect(430, 320, 112, 34))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_Run2.setFont(font)
        self.btn_Run2.setObjectName("btn_Run2")
        self.btn_Run2.clicked.connect(self.Run_Button2)

        self.btn_Run3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Run3.setGeometry(QtCore.QRect(840, 320, 112, 34))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_Run3.setFont(font)
        self.btn_Run3.setObjectName("btn_Run3")
        self.btn_Run3.clicked.connect(self.Run_Button3)

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(960, 160, 119, 23))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BIOS Release Tool"))
        self.label_2.setText(_translate("MainWindow", "Step 0 : Make sure data in config file (.ini) is correct, and select platforms"))
        self.label_4.setText(_translate("MainWindow", "Step 1 : Create Code Change"))
        self.label_5.setText(_translate("MainWindow", "Step 2 : Build EFI to POT"))
        self.label_6.setText(_translate("MainWindow", "Step 3 : Create mail, rel/ branch, tag"))
        # self.CB_ReadRN.setText(_translate("MainWindow", "Read RN"))
        # self.CB_Tag.setText(_translate("MainWindow", "Create tag"))
        self.CB_CreateMail.setText(_translate("MainWindow", "Create mail"))
        self.CB_RunBatch.setText(_translate("MainWindow", "Run Makea and Release Batch"))
        self.CB_DellBiosVersion.setText(_translate("MainWindow", "Edit DellBiosVersion.h"))
        # self.CB_Rename.setText(_translate("MainWindow", "Rename .efi with SWB"))
        self.CB_BlockBranch.setText(_translate("MainWindow", f"Commit and push {INI[0]['working_branch']}"))
        self.CB_ToSVN.setText(_translate("MainWindow", "Upload release files to ODM SVN"))
        self.CB_Branch_Tag.setText(_translate("MainWindow", "Create rel/ branch and tag"))
        self.CB_PlatformConfig.setText(_translate("MainWindow", "Edit PlatformConfig.txt"))
        self.CB_pushBranchTag.setText(_translate("MainWindow", "Push rel/ branch and tag"))
        # self.CB_scanCPI.setText(_translate("MainWindow", "Scan CPI"))
        self.CB_CpCPI.setText(_translate("MainWindow", "CherryPick CPI"))
        self.btn_Run1.setText(_translate("MainWindow", "Run"))
        self.btn_Run2.setText(_translate("MainWindow", "Run"))
        self.btn_Run3.setText(_translate("MainWindow", "Run"))
        self.btn_pop_window.setText(_translate("MainWindow", "v"))
        self.radioButton.setText(_translate("MainWindow", "DUPs available"))

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_PlatformSelection()
        self.ui.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
