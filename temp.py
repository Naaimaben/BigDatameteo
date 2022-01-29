# -*- coding: utf-8 -*-

import datetime
import json
import requests
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS

print ("please insert a station name")
station = input()

print ("welcome to:", station.upper())

def check_date():
    date_format = '%Y-%m-%d'
    my_date = input('Enter a date (YYYY-MM-DD)) : ')
    try :
        datetime.datetime.strptime(my_date, date_format)
    except ValueError:
        return -1
    return 0

while check_date() == -1:
    print ("Not a valid date!")
print("valid date")

#question 6: importer depuis URL
station = station.upper()
refine = "&refine.nom=" + station
read = requests.get('https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q=&sort=date&facet=date&facet=nom&facet=temps_present&facet=libgeo&facet=nom_epci&facet=nom_dept&facet=nom_reg'+refine)
data = read.json()

#question 7 
print(json.dumps(data, indent = 4, sort_keys=False))

#Question 8: creation d'un dossier

path ="/Users/lenovo/.spyder-py3/data"

"""
try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)
"""

#9: write data in json file
with open(path+"/data.json", 'w') as json_file:
    json.dump(data, json_file, indent = 4, sort_keys=False)
    

#10-11: json data & csv file
sites = data["records"]

with open('city.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Hour", "Temperature", "type_de_tendance_barometrique"])
    for elt in sites:
        print(elt["fields"]["nom"])
        #la fonction round car la valeur a plusieurs données apres virgule
        temp = round(elt["fields"]["tc"])
        print("    |",temp,"c")
        date=elt["fields"]["date"]
        print("    |",date[0:10])
        print("    |",elt["fields"]["coordonnees"])
        print()
        writer.writerow([date[11:13],temp])

#Question 12 
table = pd.read_csv("city.csv", encoding="latin-1")
file = open("city.csv")
reader = csv.reader(file)
#calculer le nombre des lignes 
lines = len(list(reader))
#height contient les axes des Y  (temperature)
plt.bar(x=np.arange(1, lines), height=table['Temperature'])
table.head()

plt.title("Clermont-Ferrand Temperatures")
#L'axe x (hour), rotation pour les chaines des caracteres
plt.xticks(np.arange(1,lines), table['Hour'], rotation='33', fontsize=5)
plt.yticks(rotation='50', fontsize=8)
plt.xlabel("Hours")
plt.ylabel("Temperatures")
plt.show()


#13: wordcloud: création d'un nuage des mots
table = pd.read_csv("city.csv", encoding="latin-1")
file = open("city.csv")
reader = csv.reader(file)
string=""
for row in reader:
    if row[0]!="type_de_tendance_barometrique":
        string=string+"\n"+row[2]
wordcloud = WordCloud(max_words=5, stopwords= STOPWORDS, background_color='white',width=1200, height=1000).generate(string)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
