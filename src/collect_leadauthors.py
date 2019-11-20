import glob

pathfolder = "/local/home/kloewer/agu/"
txtout = open(pathfolder+"processed/all_authors.txt","w")

all_lines = []
no_dupl_lines = []

for day in [1,2,3,4,5]:

    path = "/local/home/kloewer/agu/data/Day{:d}/".format(day)
    all_txt = glob.glob(path+"lead_authors*")

    for txt in all_txt:

        txtfile = open(txt,"r")

        for i,line in enumerate(txtfile.readlines()):

            if line not in all_lines:
                no_dupl_lines.append(line)

            all_lines.append(line)

        txtfile.close()


for line in no_dupl_lines:
    txtout.write(line)

txtout.close()
