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
    """This class contains methods that are used to determine the number of
    files in a given parameter. It can be a folder path or an array

    Attributes
    ----------


    fasta_files : Array
       an array to save the paths of fasta files

    tsv_files : Array
       an array to save the paths of tsv files

    mzML_files : Array
       an array to save the paths of mzMl files

    idXML_files : Array
       an array to save the paths of idXML files

    ini_files : Array
       an array to save the paths of ini files
    fileslist : Array
       an array containg all the files of a fiven folder

    User_Warning : QMessageBox
       a QMessageBox to inform the user of erros

    Methods
    -------
    Identify_Files_Numbers(folder_path)
       gets a folder path and  determines if there are less than one file
       of each type that is needed if not than saves the files in arrays

    Identify_Files_Numbers_Manualy(folder_path)
       works just like Identify_Files_Numbers but only cheks files that
       can not be loaded manually

    Check_If_More_Than_One(arraytotest)
       checks if there is more than one element in a given  array

    Check_If_Less_Than_One(arraytotest)
       checks if there is less than one element in a given array

    Check_If_One(arraytotest)
       checks if there is exactly one element in a given array

    Dictionary_Change_File(file_type,file_path)
       changes the value of a given file type in the global dictionary

    Dictionary_Return_Value(file_type)
       gives the value of the key that mathces the file type in the dictionary

    Dictionary_Change_Boolean(file_type)
       changes the bollean value of the key that mathces the given file type

    Dictionary_Return_Boolean(file_type)
        returns the value of the key that matches the given file type

    """

    #gets a folder path as an argument and searches for files that end with
    #.fasta or .tsv and saves them in the corresponding Array

    def Identify_Files_Numbers(folder_path):

        """
        gets a folder path and  determines if there are less than one file
        of each type that is needed if not than saves the files in arrays

        Parameters
        ---------
        folder_path
            a string that descibes the path to a folder

        Returns
        -------
        fasta_files,tsv_files,mzML_files,idXML_files,ini_files
            array that contain the paths to the files as strings
        """
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
            """
            gets a folder path and  determines if there are less than one file
            of each type that is needed if not than saves the files in arrays

            Parameters
            ---------
            folder_path
                a string that descibes the path to a folder

            Returns
            -------
            idXML_files,mzML_files
                array that contain the paths to the files as strings
            """

            mzML_files = []
            idXML_files= []
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
        """
        checks if there is more than one element in a given  array

        Parameters
        ---------
        arraytotest
            an array containing file paths as elements

        Returns
        -------
        True or False
        """
        return len(arraytotest) > 1

    def Check_If_Less_Than_One(arraytotest):
        """
        checks if there is less than one element in a given array

        Parameters
        ---------
        arraytotest
            an array containing file paths as elements

        Returns
        -------
        True or False
        """
        return len(arraytotest) == 0

    def Check_If_One(arraytotest) :
        """
        cheks if there is exactly one element in a given array

        Parameters
        ---------
        arraytotest
            an array containing file paths as elements

        Returns
        -------
        True or False
        """
        return len(arraytotest) == 1


        #used to save paths of files when loaded manually from a tab widget

    def Dictionary_Change_File(file_type,file_path):
        """
        changes the value of a given file type in the global dictionary

        Parameters
        ---------
        file_type
            a string that descibes a spesific file type

        Returns
        -------
        none
        """
        files_dictionary[file_type] = file_path

        #used to return the values of the dictionary

    def Dictionary_Return_Value(file_type):
        """
        gives the value of the key that mathces the file type in the dictionary

        Parameters
        ---------
        file_type
            a string that descibes a spesific file type

        Returns
        -------
        files_dictionary[file_type]
            a string that descibes a path to a spesific  file type
        """
        return files_dictionary[file_type]

        #changes the value to true if file loaded,
        #should be used whenever loading data
        #in to the dictionary manually

    def Dictionary_Change_Boolean(file_type):
        """
        changes the bollean value of the key that mathces the given file type

        Parameters
        ---------
        file_type
            a string that descibes a spesific file type

        Returns
        -------
        none
        """
        booleans_dictionary[file_type] = True

        #returns the boolean for the file

    def Dictionary_Return_Boolean(file_type):
        """
        returns the value of the key that matches the given file type

        Parameters
        ---------
        file_type
            a string that descibes a spesific file type

        Returns
        -------
        booleans_dictionary[file_type]
            a boolean that shows if a spesific file type has been loaded
        """
        return booleans_dictionary[file_type]
