from bs4 import BeautifulSoup
import codecs
import csv
import json
from pathlib import Path

#functions
def save_csv(path,name,table):
    with open(path+name+"_officiel.csv", mode='w+' ,newline='') as csv_file:
        csv_file_writer = csv.writer(csv_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in table:
            csv_file_writer.writerow(i)

def clean_list(text):
    new_text = []
    reject_list=['','\n','-']
    for j in text:
        if j not in reject_list:
            new_text.append(j)
    return new_text

def formating_metadata(i):

    text = i.get_text().split("\t")
    new_text =clean_list(text)
    race = clean_list(new_text[0].split(' '))
    dist = race[0]
    race.pop(0)

    if race[-1] == "Séries":
        serie = race[-1]
        lettre = ''
        race.pop(-1)
    elif race[-1] == "Bfb":
        serie = race[-1]
        race.pop(-1)
    else:
        serie = race[-2]
        lettre = race[-1]
        race.pop(-1)
        race.pop(-1)

    sex = race[-1]
    race.pop(-1)
    type =  ''.join(race)



    if sex == 'Dames':
        sex = 'dames'
    elif sex == 'Messieurs':
        sex = 'hommes'
    else:
        print("Error: metadata[sex] unknown: "+ sex)

    if type == 'NageLibre':
        nage = 'freestyle'
    elif type == 'Dos':
        nage = 'dos'
    elif type == 'Papillon':
        nage = 'papillon'
    elif type == 'Brasse':
        nage = 'brasse'
    else:
        print("Error: metadata[type] unknown: "+ type)

    if serie == 'Séries':
        epreuve = 'serie' + lettre # récupérer lettre
    elif serie == 'Finale':
        epreuve = 'finale' + lettre
    elif serie == 'Bfb':
        epreuve = 'departage'

    else:
        print("Error: metadata[serie] unknown: " + serie)

    name = "2021_Chartres_"+nage+"_"+sex+"_"+dist+"_"+epreuve
    return name,nage,epreuve,sex,dist

def find_race_change_idx(list):
    list_idx = [0]
    for i in range(1,len(list)-1):
        if int(list[i][1]) > int(list[i+1][1]):
            list_idx.append(i+1)
    return(list_idx)

def time_to_sec(time_str):
    temp = time_str.split(':')
    if len(temp) > 1:
        timer = float(temp[1])
        timer += float(temp[0])*60
        return round(timer,3)
    else:
        timer = float(temp[0])
        return round(timer,3)


path = "D:/[Chartres]/Scraping résultats/"
name_file = "100_papillon_dames"

# Ouverture du fichier en local (On a enregistré le fichier html de la page au préalable)
page = codecs.open('C:/Users/Simon/Desktop/liveffn.com - Championnats de France Elite.html','r','utf-8')
soup = BeautifulSoup(page.read())

raw = soup.find("div", {"id": "right"})
raw = raw.find("tbody")

# Collecte des métadonnées
metadata_raw = raw.find_all("td", {"class": "epreuve"})
metadata_races = []

for i in metadata_raw:

    name_race,nage,epreuve,sex,dist = formating_metadata(i)
    metadata_races.append([name_race,nage,dist,sex,epreuve])
print(metadata_races)

# Collecte des données
raw = raw.find_all("tr", {"class": "survol"})
data = [] # les id sont définis par les classements

#boucle pour chaque nageur
for i in range(len(raw)):
    bool = True


    list_raw = list(raw[i].children)
    new_raw = []

    for i in range(len(list_raw)):
        if list_raw[i] != '\n':
            new_raw.append(list_raw[i])


    if (len(new_raw[5].find_all("nobr")) == 0):
        ranking = new_raw[0].string[0:-1]
        surname_name = new_raw[1].string.split(" ")
        if len(surname_name)>2:
            surname =""
            list_surname =  surname_name[0:len(surname_name)-1]
            for i in list_surname:
                surname =surname + " "+ i
            name = surname_name[-1]
        else:
            [surname,name] = new_raw[1].string.split(" ")

        date = new_raw[2].string
        nation = new_raw[3].string
        reaction_time = float(new_raw[6].string.replace('+',''))

        dist_raw = new_raw[5].find_all("td", {"class": "distance"})
        distance_list = []
        for i in dist_raw:
            distance_list.append(i.string[0:-5])

        if (new_raw[5]["class"][0] != "temps_sans_tps_passage"):
            time_raw = new_raw[5].find_all("td", {"class": "split"})
            time_list = []
            for i in time_raw:
                time_list.append(time_to_sec(i.string))
            time = time_list[-1]
        else:
            time_list = []
            time = time_to_sec(new_raw[5].string)
            time_list.append(time)
            distance_list = [metadata_races[-1][2]]




        data_swimmer = [ranking, surname, name, date, nation, time, distance_list, time_list, reaction_time] # tout ce qu'on récolte


        data.append([0,ranking,0,"",surname+" "+name])
        for i in range(len(distance_list)):
            data.append([time_list[i],ranking,distance_list[i],"",surname+" "+name])


idx = find_race_change_idx(data)
print(idx)


for i in range(len(idx)-1):
    name_csv = metadata_races[i][0]
    start = idx[i]
    end = idx[i+1]
    data_race = data[start:end]
    data_race.insert(0,["time","id","x","lane","swimmer"])
    save_csv(path,name_csv,data_race)

name_csv = metadata_races[-1][0]
data_race = data[idx[-1]:]
data_race.insert(0,["time","id","x","lane","swimmer"])
save_csv(path,name_csv,data_race)




