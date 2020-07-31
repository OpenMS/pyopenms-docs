
import re

class LoadFasta_FastaViewer:

    # Compilation for the ProteinId_dictionary and the lists with its values for each Protein
    def protein_dictionary(fastaFile):
        """Gets fasta File Path and saves all informations about the proteins 
        in separate lists 

        Parameters
        ----------
        fastaFile : path to fasta file

        Returns
        -------
        for all proteins either Decoy or normal Lists/ dictionary.
        """
        dictKeyAccession = {}
        proteinList = []
        proteinNameList = []
        proteinOSList = []
        dictKeyAccessionDECOY = {}
        proteinListDECOY = []
        proteinNameListDECOY = []
        proteinOSListDECOY = []
        indexToStartReadingFrom_InFastaFile = 0

        with open(fastaFile) as file_content:

            # Go through the fasta file, line by line
            for seqs in file_content:

                # if protein declaration (next protein) was found
                if seqs.startswith('>'):

                    # safe information about the protein declaration for when inserting informations into lists
                    protein_declaration = seqs

                    # find upper and lower index of Protein Accession (ID)
                    bounds = [m.start() for m in re.finditer(r'\|', seqs)]

                    # if a Protein Accesion (ID) was found
                    if len(bounds) == 2:
                        key = (seqs[bounds[0]+1:bounds[1]])
                        descr_upper_index = seqs.find('OS=')

                        # find out up to which index the OS goes
                        os_upper_index = seqs.find('(')
                        os = 'not found'

                        # if no upper index for the OS was found use the line from "OS=" till end of line
                        if (os_upper_index == -1):
                            # if "OS=" was found, else stick with "os = not found"
                            if not (descr_upper_index == -1):
                                stringFrom_OS_TillEndOfLine = seqs[descr_upper_index+3:]
                                listOfAllWordsTillEndOfLine = stringFrom_OS_TillEndOfLine.split()
                                os = listOfAllWordsTillEndOfLine[0] + ' ' + listOfAllWordsTillEndOfLine[1]

                        name = 'not found'
                        if not (descr_upper_index == -1):
                            name = (seqs[bounds[1]+1:descr_upper_index])

                        stringValue = ""
                        indexShift = 0
                        nextLine = next(file_content)

                        # read file line by line, till new protein (begins with '>')
                        while not nextLine.startswith('>'):
                            stringValue += nextLine[:-1]
                            try:
                                nextLine = next(file_content)
                            except Exception:
                                break
                            indexShift = indexShift + 1

                        # shift Index inside of the file-reader
                        indexToStartReadingFrom_InFastaFile = indexToStartReadingFrom_InFastaFile + len(stringValue) + len(seqs) + indexShift
                        file_content.seek(indexToStartReadingFrom_InFastaFile, 0)

                        # set the values inside of the dictionary and the lists
                        # is decoy -> use seperate List to safe informations
                        if protein_declaration.startswith('>DECOY'):
                            dictKeyAccessionDECOY[key] = stringValue
                            proteinListDECOY.append(stringValue)
                            proteinNameListDECOY.append(name)

                            if (os_upper_index == -1 or descr_upper_index == -1):
                                proteinOSListDECOY.append(os)
                            else:
                                proteinOSListDECOY.append((seqs[descr_upper_index+3:os_upper_index]))

                        # regular protein -> use regular list 
                        else:
                            dictKeyAccession[key] = stringValue
                            proteinList.append(stringValue)
                            proteinNameList.append(name)

                            if (os_upper_index == -1 or descr_upper_index == -1):
                                proteinOSList.append(os)
                            else:
                                proteinOSList.append((seqs[descr_upper_index+3:os_upper_index]))
                        
                    # if no Protein Accesion (ID) was found
                    else:
                        key = seqs.split("OS=")[0]
                        descr_upper_index = seqs.find('OS=')

                        # find out up to which index the OS goes
                        os_upper_index = seqs.find('(')
                        os = 'not found'

                        # if no upper index for the OS was found use the line from "OS=" till end of line
                        if (os_upper_index == -1):
                            stringFrom_OS_TillEndOfLine = seqs[descr_upper_index+3:]
                            listOfAllWordsTillEndOfLine = stringFrom_OS_TillEndOfLine.split()
                            os = listOfAllWordsTillEndOfLine[0] + ' ' + listOfAllWordsTillEndOfLine[1]

                        name = seqs.split("OS=")[0]
                        stringValue = ""
                        indexShift = 0
                        nextLine = next(file_content)

                        # read file line by line, till new protein (begins with '>')
                        while not nextLine.startswith('>'):
                            stringValue += nextLine[:-1]
                            try:
                                nextLine = next(file_content)
                            except Exception:
                                break
                            indexShift = indexShift + 1

                        # shift Index inside of the file-reader
                        indexToStartReadingFrom_InFastaFile = indexToStartReadingFrom_InFastaFile + len(stringValue) + len(seqs) + indexShift
                        file_content.seek(indexToStartReadingFrom_InFastaFile, 0)

                        # set the values inside of the dictionary and the lists
                        # is decoy -> use seperate List to safe informations
                        if protein_declaration.startswith('>DECODY'):
                            dictKeyAccessionDECOY[key] = stringValue
                            proteinListDECOY.append(stringValue)
                            proteinNameListDECOY.append(name)

                            if (os_upper_index == -1 or descr_upper_index == -1):
                                proteinOSListDECOY.append(os)
                            else:
                                proteinOSListDECOY.append((seqs[descr_upper_index+3:os_upper_index]))

                        else:
                            dictKeyAccession[key] = stringValue
                            proteinList.append(stringValue)
                            proteinNameList.append(name)

                            if (os_upper_index == -1 or descr_upper_index == -1):
                                proteinOSList.append(os)
                            else:
                                proteinOSList.append((seqs[descr_upper_index+3:os_upper_index]))

        return dictKeyAccession, proteinList, proteinNameList, proteinOSList, dictKeyAccessionDECOY, proteinListDECOY, proteinNameListDECOY, proteinOSListDECOY


def main():

    # for testing purposes only
    # use your own path for it
    dictKeyAccession, proteinList, proteinNameList, proteinOSList, dictKeyAccessionDECOY, proteinListDECOY, proteinNameListDECOY, proteinOSListDECOY = LoadFasta_FastaViewer.protein_dictionary(
        "C:/Users/Alex/Desktop/iPRG2015_target_decoy_nocontaminants.fasta")

    proteinnameSub = input("Name: ")

    for protein_name in proteinNameList:
        if proteinnameSub in protein_name:
            print("Proteinname: " + protein_name)

    # here the users enters the protein accession (key), or only a part of it
    # e.g.: 'P00761'
    protein_accession_maybe_sub_sequence = input("Bitte Protein accession angeben: ")

    # index starts with 0 (for the lists and the dictionary)
    # search for key
    for protein_accession in dictKeyAccession:
        if protein_accession_maybe_sub_sequence in protein_accession:
            index = list(dictKeyAccession).index(protein_accession)
            print("ID: " + list(dictKeyAccession.keys())[index])
            print("Protein: " + dictKeyAccession.get(protein_accession))
            print("Proteinname: " + proteinNameList[index])
            print("OS: " + proteinOSList[index])


if __name__ == "__main__":
    main()
