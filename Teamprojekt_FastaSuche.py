




# Zusammenstellung des dictionaries und der 3 Listen zum suchen für die a) und b)
def protein_dictionary (fastaFile):
    dictKeyAccession = {}
    proteinList = []
    proteinNameList = []
    proteinOSList = []
    with open(fastaFile) as file_content:
        for seqs in file_content:
            if seqs.startswith('>'):           
                bounds = find_all_indexes(seqs, '|')
                if len(bounds) != 0:
                    key = (seqs[bounds[0]+1:bounds[1]])
                    descr_upper_index = seqs.find('OS')
                    # herausfinden bis zu welchem index das OS geht 
                    os_upper_index = seqs.find('(')
                    os = ''
                    if (os_upper_index == -1):
                        zwischenergebnis = seqs[descr_upper_index+3:]
                        zwischenergebnis1 = zwischenergebnis.split()
                        os = zwischenergebnis1[0] + ' ' + zwischenergebnis1[1]
                    name = (seqs[bounds[1]+1:descr_upper_index])
                    stringValue = ""
                    nextLine = next(file_content)
                    while not nextLine.startswith('>'):
                        stringValue += nextLine
                        nextLine = next(file_content)
                    dictKeyAccession[key] = stringValue
                    proteinList.append(stringValue)
                    proteinNameList.append(name)
                    if (os_upper_index == -1):
                        proteinOSList.append(os)
                    else:
                        proteinOSList.append((seqs[descr_upper_index+3:os_upper_index]))
    return dictKeyAccession, proteinList, proteinNameList, proteinOSList


# wird für die Methode protein_dictionary benötigt (suche von mehreren Indizes)
def find_all_indexes(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1
 


def main():

    # a)
    dictKeyAccession, proteinList, proteinNameList, proteinOSList = protein_dictionary("C:/Users/Alex/Desktop/iPRG2015_target_decoy_nocontaminants.fasta")

    # hier kommt die eingegeben protein accession (oder nur ein Teil davon) rein
    # z.B.: 'P00761'
    protein_accession_maybe_sub_sequence = input("Bitte Protein accession angeben: ")

    # index beginnt mit 0 (für das dictionary und die Liste)
    # Suche nach dem key (a)
    for protein_accession in dictKeyAccession:
        if protein_accession_maybe_sub_sequence in protein_accession:
            index = list(dictKeyAccession).index(protein_accession)
            print("Protein: " + dictKeyAccession.get(protein_accession))
            print("ID: " + list(dictKeyAccession.keys())[index]) 
            print("Proteinname: " + proteinNameList[index]) 
            print("OS: " + proteinOSList[index])

    # b)
    # hier kommt die eingegene Sequenz des Proteins rein 
    # z.B.: FPTDDDDKIVGGYTCAANSIPYQVSLNSGSHFCGGSLINSQWVVSAAHCYKSRIQVRLGEHNIDVLEGNEQFINAAKIIT
    
    protein_sub_sequence = input("Bitte Protein Sequenz angeben: ")

    for protein_sequence in proteinList:
        if protein_sub_sequence in protein_sequence:
            index = proteinList.index(protein_sequence)
            print("ID: " + list(dictKeyAccession.keys())[index])
            print("Protein: " + proteinList[index])
            print("Proteinname: " + proteinNameList[index])
            print("OS: " + proteinOSList[index])
            
    # c)
    # Suche nach Name 
    # z.B: TRYP_PIG Trypsin

    protein_sub_name = input("Bitte Protein Namen eingeben: ")

    for protein_name in proteinNameList:
        if protein_sub_name in protein_name:
            index = proteinNameList.index(protein_name)
            print("ID: " + list(dictKeyAccession.keys())[index])
            print("Protein: " + proteinList[index])
            print("Proteinname: " + proteinNameList[index])
            print("OS: " + proteinOSList[index])

    


if __name__ == "__main__":
    main()



