




# Aufgabe a) + b)
def protein_dictionary (fastaFile):
    thisdict = {}
    protein_dict = {}
    with open(fastaFile) as file_content:
        for seqs in file_content:
            if seqs.startswith('>'):           
                bounds = find_all_indexes(seqs, '|')
                if len(bounds) != 0:
                    key = (seqs[bounds[0]+1:bounds[1]])
                    descr_upper_index = seqs.find('OS')
                    description = (seqs[bounds[1]+1:descr_upper_index])
                    stringValue = "Proteinname: " + description + "\nProtein:\n"
                    stringKeyForProteinDict = ""
                    nextLine = next(file_content)
                    while not nextLine.startswith('>'):
                        stringValue += nextLine
                        stringKeyForProteinDict += nextLine
                        nextLine = next(file_content)
                    thisdict[key] = stringValue
                    protein_dict[stringKeyForProteinDict] = stringValue
    return thisdict, protein_dict


# wird für das protein_dictionary benötigt 
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
    dictionary, protein_dict = protein_dictionary("C:/Users/Alex/Desktop/iPRG2015_target_decoy_nocontaminants.fasta")

    # hier kommt die eingegeben protein accession rein
    # z.B.: 'P00761'
    protein_accession = input("Bitte protein accession angeben:\n")

    print("Gefundenes Protein:")
    if protein_accession in dictionary:
        print(dictionary.get(protein_accession))
    else:
        print('No matching protein accession found in database.')

    # b)
    # hier kommt die eingegene Sequenz des Proteins rein 
    # z.B.: FPTDDDDKIVGGYTCAANSIPYQVSLNSGSHFCGGSLINSQWVVSAAHCYKSRIQVRLGEHNIDVLEGNEQFINAAKIIT
    protein_sub_sequence = input("Bitte Protein Sequenz angeben:\n")

    print("Alle gefundenen Proteine mit der eigegebenen Sequenz:")
    for ps in protein_dict:
        if protein_sub_sequence in ps:
            print(protein_dict.get(ps))



if __name__ == "__main__":
    main()



