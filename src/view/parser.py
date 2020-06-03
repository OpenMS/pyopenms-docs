def parser(file):
    PRT = []
    PSM = []

    with open(file) as inp:
        for line in inp:
            if line.startswith("PRH"):
                PRT.append(line.strip().split('\t'))
            elif line.startswith("PRT") and not line.endswith("protein_details\n"):
                PRT.append(line.strip().split('\t'))
            elif line.startswith("PSH") or line.startswith("PSM"):
                PSM.append(line.strip().split('\t'))

