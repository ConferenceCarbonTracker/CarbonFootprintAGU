import glob

path = "/local/home/kloewer/agu/raw/Day1/"

all_txt = glob.glob(path+"abstracts*")

for txt in all_txt:

    txtfile = open(txt,"r")
    txtout = open(path+"authors"+txt.split("/")[-1][9:],"w")

    for line in txtfile.readlines():
        if '<span class="topDisplay">' in line:
            authors = line[29:]     # cut off <span ... play">
            txtout.writelines(authors)


    txtfile.close()
    txtout.close()