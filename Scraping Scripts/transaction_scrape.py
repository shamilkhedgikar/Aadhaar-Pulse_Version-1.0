import urllib
import urllib.request
import requests
import csv
import os
import pandas as pd
from bs4 import BeautifulSoup
#list
tablelist = []
#table_lists for transaction tablelist
columns_more_1 = 19
rangelist_0 = list(range(0,columns_more_1,1))
print(rangelist_0)#THESE ARE THE NUMBER OF COLUMNS IN THE DATA. VERIFY
listOfLists = [[] for i in range(columns_more_1)]
#----lists of lists works better here due to subsequent looping on lists (there are 19 columns!)
#x = 5 # amount of lists you want to create
#for i in range(1, x+1):
#    command = "" # this line is here to clear out the previous command
#    command = "column" + str(i) + " = []"
#    exec(command)
#------
#table_lists for bank details tablelist
#downloads = 216
#This is just the output on the way the tables  are structured and located!
#rangelist_1 = list(range(8,len(stat_table),10))
#print(rangelist_1)
#rangelist_2 = list(range(9,len(stat_table),10))
#print(rangelist_1)
#make the soup!
#------
headers = {'User-Agent': 'Mozilla/5.0'}
soup =  BeautifulSoup(open("RAMTEK.html"), "html.parser")#give the merged html here.
stat_table = soup.findAll('table')
print(len(stat_table))#FIRST RUN CODE ONLY TILL HERE. Note the output.
#print((stat_table[9]))
#print(sample_multiple)
for iteration in range(8,955,10):#enter the output above as the second value
    rows = stat_table[iteration].findAll('tr')
    for row in rows:
        for range in rangelist_0:
            listOfLists[range].append(str(row.find_all('td')[range].text))
cols = {
'column1:' : listOfLists[0],
'column2:' : listOfLists[1],
'column3:' : listOfLists[2],
'column4:' : listOfLists[3],
'column5:' : listOfLists[4],
'column6:' : listOfLists[5],
'column7:' : listOfLists[6],
'column8:' : listOfLists[7],
'column9:' : listOfLists[8],
'column10:' : listOfLists[9],
'column11:' : listOfLists[10],
'column12:' : listOfLists[11],
'column13:' : listOfLists[12],
'column14:' : listOfLists[13],
'column15:' : listOfLists[14],
'column16:' : listOfLists[15],
'column17:' : listOfLists[16],
'column18:' : listOfLists[17],
'column19:' : listOfLists[18],
} #use custom labels  if required. Headers are off currently
df = pd.DataFrame(cols)
#print(listOfLists[0])
#print(rangelist_0)
#print(df)
df.to_csv('RAMTEK_transactions.csv', index=True, header=False)#change name of district herere
