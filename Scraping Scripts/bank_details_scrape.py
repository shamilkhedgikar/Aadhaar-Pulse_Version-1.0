import urllib
import urllib.request
import requests
import csv
import os
import pandas as pd
from bs4 import BeautifulSoup
#list
tablelist = []
columns_more_1 = 7
rangelist_1 = list(range(0,columns_more_1,1))
print(rangelist_1)#THESE ARE THE NUMBER OF COLUMNS IN THE DATA. VERIFY
listOfLists_2 = [[] for i in range(columns_more_1)]
headers = {'User-Agent': 'Mozilla/5.0'}
soup =  BeautifulSoup(open("SAVNER.html"), "html.parser")#give the merged html here.
stat_table = soup.findAll('table')
print(len(stat_table))#FIRST RUN CODE ONLY TILL HERE. Note the output.
for iteration in range(9,1620,10):#enter the output above as the second value
    rows = stat_table[iteration].findAll('tr')
    for row in rows:
        for range in rangelist_1:
            listOfLists_2[range].append(str(row.find_all('td')[range].text))
cols2 = {
'column1:' : listOfLists_2[0],
'column2:' : listOfLists_2[1],
'column3:' : listOfLists_2[2],
'column4:' : listOfLists_2[3],
'column5:' : listOfLists_2[4],
'column6:' : listOfLists_2[5],
'column7:' : listOfLists_2[6],
} #use custom labels  if required. Headers are off currently
df = pd.DataFrame(cols2)
df.to_csv('SAVNER_banks.csv', index=True, header=False)#change name of district here
