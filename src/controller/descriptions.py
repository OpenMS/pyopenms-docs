import os
import sys
import glob
import pandas as pd
import re


class Descriptions:
    """
    Filehandler class that provides support for file and directory interaction.
    """
    def __init__(self, descriptions):
        self.descriptions = descriptions

    descriptions = {"welcome":
                        """
                        <h4 align='justify'>Welcome: Get started with your
                        Proteinquantifcation!</h4>
                        <div align='justify'>This application performs a 
                        ProteomicsLFQ - Proteinquantification. <br>
                        The files, needed to 
                        run the application have to be loaded into
                        <br>XML-Viewer, 
                        Experimental-Design and Fasta-Viewer-Tabs, 
                        respectively. <br>Finally, the mzTab-Viewer-Tab 
                        will show the result.
                        <br>
                        You can look at the spectra used for the 
                        quantification<br>in the Spec-Viewer-Tab.</div>
                        """,
                    "XML-Viewer":
                        """
                        <div align='justify'><b>XML Viewer:</b><br>In this
                        tab you can load, edit
                        and save your experiments config-file.<br>
                        If no config-file is provided, 
                        a default file will be generated,<br>
                        which you can modify for the quantification.<br>
                        This application only accepts '.ini'-files as 
                        config-files.</div>
                        """,
                    "Experimental-Design":
                        """
                        <div align='justify'><b>Experimental 
                        Design:</b><br>The Experimental-Design-Tab
                        enables you to load and edit an 
                        experimental design.<br>
                        You can edit specifics like number<br>
                        of files, fractions or groups.<br>'.tsv'
                        -files can be directly loaded as a 
                        table.<br> You can also add single 
                        '.mzml'-files to the table,<br>either
                        via drag'n'drop, or with the 'add file'
                        -button.<br> You can filter the files 
                        using the textfield in the upper right 
                        corner.</div>
                        """,
                    "Fasta-Viewer":
                        """
                        <div align='justify'><b>Fasta Viewer:</b><br>In 
                        this tab you can load a fasta file<br>and search 
                        for information about the sequences such 
                        as<br>protein-IDs and accession-numbers.</div>
                        """,
                    "Spec-Viewer":
                        """
                        <div align='justify'><b>Spectrum Viewer:</b><br>This
                        tab enables you to look at<br>the mzML-spectra 
                        your Mass-Spectrometer measured for your
                        <br>samples.<br>It loads all spectra files, 
                        which are
                        located in your project folder.</div>
                        """,
                    "mzTab-Viewer":
                        """
                        <div align='justify'><b>MzTab Viewer:</b><br>The 
                        results of your analysis is visualized 
                        in the mzTab-Viewer.<br>
                        Information about the identified sequences, such as
                        retention time, <br>charge or mass to charge ratio
                        are listed in the table.</div>
                        """,
                    }

    def getDescription(self, widgetname:str) -> str:
        """
        Scans a provided directory and returns a list of all
        the mzML files.
        """
        return self.descriptions.widgetname