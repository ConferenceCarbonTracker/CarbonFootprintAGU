import glob

listofcountries = open("/local/home/kloewer/agu/list_of_countries.txt","r")
countries = [country[:-1] for country in listofcountries.readlines()]
listofcountries.close()

path = "/local/home/kloewer/agu/data/Day5/"

all_txt = glob.glob(path+"abstracts*")

for txt in all_txt:

    txtfile = open(txt,"r")
    txtout = open(path+"lead_authors"+txt.split("/")[-1][9:],"w")

    for i,line in enumerate(txtfile.readlines()):

        affiliation = "0\n"
        lead_author = "0"

        if '<span class="topDisplay">' in line:
            authors = line[29:]     # cut off <span ... play">

            # FIND LEAD AUTHOR BY <b>...</b

            j0 = authors.find("<b>")
            j1 = authors.find("</b>")

            if j0 == -1 or j1 == -1:
                println("Lead author not found in line {:d} of ".format(i+1)+txt)

            lead_author = authors[j0+3:j1]

            # FIND LEAD AUTHORS AFFILIATION

            j2 = authors[j1:].find("<sup>")     # first occurence of <sup> after lead author
            j3 = authors[j1:].find("</sup>")     # same for </sup>

            if j2 != -1 and j3 != -1:           # sup exists

                affiliation_index = authors[j1:][j2+5:j3].split(",")[0]     # pick the first in case of several

                # find affiliation in whole string
                j_aff0 = authors.find("({:s})".format(affiliation_index))
                j_aff1 = authors.find("({:d})".format(int(affiliation_index)+1))

                affiliation = authors[j_aff0+3:j_aff1]

                # cut off comma at the end
                if affiliation[-2:] == ", ":
                    affiliation = affiliation[:-2]

                aff_split = affiliation.split(",")

                if aff_split[-2].isupper():     # if second last is capital means city, state for US/postcode for UK, country
                    affiliation = ",".join(aff_split[-3:])      # take 3
                else:                                           # city, country

                    # THE SOUTH KOREA CASE
                    if aff_split[-1] == " Republic of (South)":
                        affiliation = aff_split[-3] + ", South Korea"
                    else:
                        affiliation = ",".join(aff_split[-2:])

            else:

                rest_string = authors[j1+5:].split(",")

                for k,part in enumerate(rest_string):
                    if part.strip() in countries:
                        if rest_string[k-1].isupper():
                            affiliation = ",".join(rest_string[k-2:k+1])
                        elif part.strip() == "Republic of (South)":
                            affiliation = " ,".join([rest_string[k-2].strip(),"South Korea\n"])
                        else:
                            affiliation = ",".join(rest_string[k-1:k+1])
                        break

                    if part == rest_string[-1]:
                        country = part.split(" and ")[0].strip()

                        if country in countries:
                            if rest_string[-2].isupper():
                                affiliation = ",".join(rest_string[-3:-1]) + ", "+country
                            else:
                                affiliation = rest_string[-2] + ", " + country

                        else:
                            print(rest_string)


            try:
                if affiliation[-1] == "\n":
                    affiliation = affiliation[:-1]
            except:
                affiliation = "0\n"

            txtout.write(lead_author+","+affiliation + "\n")

    txtfile.close()
    txtout.close()