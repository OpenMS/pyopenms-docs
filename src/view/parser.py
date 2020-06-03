def parser(file):
    PRT = []
    PSM = []
    counter1 = 0
    counter2 = 0

    with open(file) as inp:
        for line in inp:
            if line.startswith("PRH"):
                PRT.append(line.strip().split('\t'))
                counter1 + 1
            elif line.startswith("PRT"):
                PRT.append(line.strip().split('\t'))
                counter1 + 1
            elif line.startswith("PSH") or line.startswith("PSM"):
                PSM.append(line.strip().split('\t'))
                counter2 + 1

    l = len(PRT[0]) - 1
    for i in PRT:
        if i[l] == 'protein_details':
            PRT.remove(i)
