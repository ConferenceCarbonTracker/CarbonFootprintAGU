import glob

listofcountries = open("/local/home/kloewer/agu/list_of_countries.txt","r")
countries = [country[:-1] for country in listofcountries.readlines()]
listofcountries.close()

for day in [1,2,3,4,5]:

    path = "/local/home/kloewer/agu/data/Day{:d}/".format(day)
    all_txt = glob.glob(path+"lead_authors*")

    for txt in all_txt:

        txtfile = open(txt,"r")

        for i,line in enumerate(txtfile.readlines()):

            line_split = line.split(",")
            author = line_split[0]
            country = line_split[-1]

            if conutry not in countries:
                print(day, txt[-13:], i, author, country)


        txtfile.close()
