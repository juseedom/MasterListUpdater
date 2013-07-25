from PyQt4 import QtGui, QtCore
from functools import partial

import sys
import os, time
sys.path.append('C:\\Python27\\project\\Ready')
import ReadExcel
import autoftp

mytime = time.localtime(time.time())
today_date = "%4d%02d%02d" %(mytime.tm_year,mytime.tm_mon,mytime.tm_mday)

class Dialog(QtGui.QDialog):
    """docstring for GuiForm"""
    def __init__(self):
        super(Dialog, self).__init__()
        self.filepath = ['','','']
        
        self.createMenu()
        self.createGridGroupBoxs()
        self.bigEditor = QtGui.QTextEdit()
        self.bigEditor.setReadOnly(True)
               
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.calc)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(buttonBox)
        mainLayout.addWidget(self.bigEditor)
        
        self.setLayout(mainLayout)

        self.setWindowTitle("RF_MasterList_Updater")

    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()

        self.fileMenu = QtGui.QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)
        self.exitAction.triggered.connect(self.reject)

    def createGridGroupBoxs(self):
        self.gridGroupBox = QtGui.QGroupBox("File Browser")
        layout = QtGui.QGridLayout()
        namelist = ["MasterList", "CME_Configuration", "RF MasterList"]
        self.fb_label = list()
        self.fb_lineEdit = list()
        self.fb_button = list()

        for i in range(len(namelist)):
            self.fb_label.append(QtGui.QLabel(namelist[i]))

            self.fb_lineEdit.append(QtGui.QLineEdit())
            self.fb_lineEdit[i].setReadOnly(True)
            self.fb_lineEdit[i].setText(namelist[i])
            self.fb_lineEdit[i].setMinimumWidth(250)

            self.fb_button.append(QtGui.QPushButton("Browse"))
            self.fb_button[i].clicked.connect(partial(self.browseFile,self.fb_lineEdit[i],i))

            layout.addWidget(self.fb_label[i],1+i,0)
            layout.addWidget(self.fb_lineEdit[i],1+i,1)
            layout.addWidget(self.fb_button[i],1+i,2)

        #self.autoMatch = QtGui.QCheckBox("Auto Match")
        self.autoFTP = QtGui.QCheckBox("DL from FTP")

        self.autoFTP.toggled.connect(self.autoFTPDL)
        #self.autoMatch.toggled.connect(self.autoMatchPath)
        #layout.addWidget(self.autoMatch, 1, 3)
        layout.addWidget(self.autoFTP, 2, 3)
        self.gridGroupBox.setLayout(layout)

    def autoMatchPath(self, filepath):
        if filepath.find('LTE_Status') != -1:
            path = filepath[:filepath.rfind('\\')]
            for ml_file in os.listdir(path):
                #find the MasterList in the same Folder
                if ml_file.find('M1 LTE MASTERLIST') != -1:
                    self.filepath[0] = path+'\\'+ml_file
                    self.fb_lineEdit[0].setText(self.filepath[0])
                    return True
        elif filepath.find('M1 LTE MASTERLIST') != -1:
            path = filepath[:filepath.rfind('\\')]
            for cme_file in os.listdir(path):
                #find the MasterList in the same Folder
                if cme_file.find('LTE_Status') != -1:
                    self.filepath[1] = path+'\\'+cme_file
                    self.fb_lineEdit[1].setText(self.filepath[1])
                    return True

    def autoFTPDL(self):
        if self.autoFTP.checkState() == 2:
            self.bigEditor.append('Auto FTP Checked')
            if autoftp.getfilefromftp(ftpaddr = '172.18.95.2', ftppath = '/export/home/sysm/ftproot/TimerTask/12878/output/', \
                lcdpath = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\CME Data\\'):
                self.bigEditor.append('Download File Successfully')
                autoftp.zipfile(lcdpath = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\CME Data\\', \
                    tcdpath = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\RF Parameter\\'+today_date)
                self.filepath[1] = 'D:\\RNP&RNO\\ENGINEER\\Parameters\\RF Parameter\\' +today_date + '\\LTE_Status.csv'
                self.fb_lineEdit[1].setText(self.filepath[1])
                self.autoMatchPath(self.filepath[1])
                self.fb_button[1].setEnabled(False)
            else:
                self.bigEditor.append('Download File Failed')
                self.autoFTP.setCheckState(False)
        else:
            self.bigEditor.append('Auto FTP Canceled')
            self.fb_button[1].setEnabled(True)


    def browseFile(self, lineEdit, i):
        if i == 0:
            fileName = QtGui.QFileDialog.getOpenFileName(self,"Open File",'',"Excel File (*.xlsx);;All File (*)")
        elif i == 1:
            fileName = QtGui.QFileDialog.getOpenFileName(self,"Open File",'',"Excel File (*.csv);;All File (*)")
        elif i == 2:
            fileName = QtGui.QFileDialog.getOpenFileName(self,"Open File",'',"Excel File (*.xls);;All File (*)")
        fileName = fileName.replace('/','\\\\')
        if not fileName:
            return False
        self.filepath[i] = fileName
        lineEdit.setText(fileName)

    def calc(self):
        self.bigEditor.append('Start to Update...')
        self.bigEditor.append('Set file as below:')
        for fp in self.filepath:
            self.bigEditor.append(fp)
        rf = ReadExcel.RFMasterList(rf_path = self.filepath[2])
        self.bigEditor.append("Read RF MasterList Finished...")
        #print self.filepath[0]
        ml = ReadExcel.MasterList(ml_path = str(self.filepath[0]))
        self.bigEditor.append("Read MasterList Finished...")
        cme = ReadExcel.CMEMasterList(cme_path = self.filepath[1])
        self.bigEditor.append("Read CME MasterList Finished...")
        result = ReadExcel.ReadnCompare(rf,ml,cme,self.filepath[1])
        self.bigEditor.append("Update RF MasterList Finished...")
        output_path = self.filepath[1][:self.filepath[1].rfind('\\')]+'\\result.xls'
        result.Update2Excel(output_path)
        self.bigEditor.append("Save Finished...")
        


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
        
