def parser(file):
    PRT = []
    PSM = []

    with open(file) as inp:
        for line in inp:
            if line.startswith("PRH"):
                PRT.append(line.strip().split('\t'))
            elif line.startswith("PRT"):
                PRT.append(line.strip().split('\t'))
            elif line.startswith("PSH") or line.startswith("PSM"):
                PSM.append(line.strip().split('\t'))

    l = len(PRT[0]) - 1
    for i in PRT:
        if i[l] == 'protein_details':
            PRT.remove(i)
