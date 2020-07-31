import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow,
                             QAction, qApp,
                             QHBoxLayout, QVBoxLayout, QMessageBox,
                             QLineEdit, QTableWidget, QTableWidgetItem,
                             QGridLayout, QPlainTextEdit,
                             QDesktopWidget, QLabel, QRadioButton,
                             QGroupBox, QSizePolicy, QCheckBox, QFileDialog,
                             QTextEdit, QTextBrowser)
from PyQt5.QtGui import QFont, QColor

#making a files dictionary that is going to be a global variable

files_dictionary = {

    "fasta": "",
    "tsv": "",
    "data": "",
    "mzML": "",
    "idXML": "",
    "ini_path" : ""
    }

booleans_dictionary = {

        "fasta": False,
        "tsv": False,
        "data": False,
        "mzML": False,
        "idXML": False,
        "ini_path" : False
        }

class Files_Number_Handler():

    #gets a folder path as an argument and searches for files that end with
    #.fasta or .tsv and saves them in the corresponding Array

    def Identify_Files_Numbers(folder_path):
        fasta_files=[]
        tsv_files = []
        mzML_files = []
        idXML_files= []
        ini_files = []

        fileslist = sorted(os.listdir(folder_path))

        for file in fileslist:
            if file.endswith(".fasta"):
                fasta_files.append(file)

            if file.endswith(".tsv"):
                tsv_files.append(file)

            if file.endswith(".mzML"):
                mzML_files.append(file)

            if file.endswith(".idXML"):
                idXML_files.append(file)

            if file.endswith(".ini"):
                ini_files.append(file)

            if file.endswith(".csv"):
                tsv_files.append(file)

        if len(mzML_files) == 0 and len(idXML_files) == 0:
            User_Warning = QMessageBox()
            User_Warning.setIcon(QMessageBox.Information)
            User_Warning.setText("No mzML and idXML files found. Please select a different folder.")
            User_Warning.setWindowTitle("Information")
            Information = User_Warning.exec_()


        if  len(mzML_files) == 0 and len(idXML_files) != 0:
            User_Warning = QMessageBox()
            User_Warning.setIcon(QMessageBox.Information)
            User_Warning.setText("No mzML files found. Please select a different folder.")
            User_Warning.setWindowTitle("Information")
            Information = User_Warning.exec_()
            Files_Number_Handler.Dictionary_Change_Boolean('idXML')

        if len(mzML_files) != 0 and len(idXML_files) == 0:
            User_Warning = QMessageBox()
            User_Warning.setIcon(QMessageBox.Information)
            User_Warning.setText("No idXML files found. Please select a different folder.")
            User_Warning.setWindowTitle("Information")
            Information = User_Warning.exec_()
            Files_Number_Handler.Dictionary_Change_Boolean('mzML')

        if len(mzML_files) != 0 and len(idXML_files) != 0:
            Files_Number_Handler.Dictionary_Change_Boolean('mzML')
            Files_Number_Handler.Dictionary_Change_Boolean('idXML')




        return fasta_files,tsv_files,mzML_files,idXML_files,ini_files

    #works just like  Identify_Files_Numbers but for the manualy option

    def Identify_Files_Numbers_Manualy(folder_path):

            mzML_files = []
            idXML_files= []
            mzMLLoaded = 0
            idXMLLoaded = 0
            fileslist = sorted(os.listdir(folder_path))
            for file in fileslist:
                if file.endswith(".mzML"):
                    mzML_files.append(file)

                if file.endswith(".idXML"):
                    idXML_files.append(file)


            if len(mzML_files) == 0 and len(idXML_files) == 0:
                User_Warning = QMessageBox()
                User_Warning.setIcon(QMessageBox.Information)
                User_Warning.setText("No mzML and idXML files found. Pleas select a different folder.")
                User_Warning.setWindowTitle("Information")
                Information = User_Warning.exec_()



            if  len(mzML_files) == 0 and len(idXML_files) != 0:
                User_Warning = QMessageBox()
                User_Warning.setIcon(QMessageBox.Information)
                User_Warning.setText("No mzML files found. Pleas select a different folder.")
                User_Warning.setWindowTitle("Information")
                Information = User_Warning.exec_()
                Files_Number_Handler.Dictionary_Change_Boolean('idXML')


            if len(mzML_files) != 0 and len(idXML_files) == 0:
                User_Warning = QMessageBox()
                User_Warning.setIcon(QMessageBox.Information)
                User_Warning.setText("No idXML files found. Pleas select a different folder.")
                User_Warning.setWindowTitle("Information")
                Information = User_Warning.exec_()
                Files_Number_Handler.Dictionary_Change_Boolean('mzML')

            if len(mzML_files) != 0 and len(idXML_files) != 0:
                Files_Number_Handler.Dictionary_Change_Boolean('mzML')
                Files_Number_Handler.Dictionary_Change_Boolean('idXML')



            return idXML_files,mzML_files

    #checks if array contains only on element, it is important because if
    #more than 1 file exists user needs to select the file he wants to use

    def Check_If_More_Than_One(arraytotest):
        if len(arraytotest)>1:
            return True
        else :
            return False

    def Check_If_Less_Than_One(arraytotest):
        if len(arraytotest)==0:
            return True
        else :
            return False
    def Check_If_One(arraytotest) :
        if len(arraytotest) == 1:
            return True
        else:
            return False


        #used to save paths of files when loaded manually from a tab widget

    def Dictionary_Change_File(file_type,file_path):
        global files_dictionary
        files_dictionary[file_type] = file_path

        #used to return the values of the dictionary

    def Dictionary_Return_Value(file_type):
        global files_dictionary
        return files_dictionary[file_type]

        #changes the value to true if file loaded,
        #should be used whenever loading data
        #in to the dictionary manually

    def Dictionary_Change_Boolean(file_type):
        global booleans_dictionary
        booleans_dictionary[file_type] = True

        #returns the boolean for the file

    def Dictionary_Return_Boolean(file_type):
        global booleans_dictionary
        return booleans_dictionary[file_type]
