import urllib
import urllib.request
import requests
import csv
import os
import pandas as pd
from bs4 import BeautifulSoup
#lists
panchayat_list=[]
data = []
data1 = []
data2 = []
data3 = []
#make some soup!
list_soup = BeautifulSoup(open("panchayat_list.html"), "html.parser") #keep Panchayat list in script folder
panchayat_list = [a['value'] for a in list_soup.find_all('option', value=True)]
panchayat_list_trial = panchayat_list[60:70] #list for trial run
print(panchayat_list_trial)
for panchayat_number in panchayat_list:
    url = 'http://nregasp2.nic.in/Netnrega/writereaddata/state_out/jobcardreg_' +str(panchayat_number)+ '_local.html'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers = headers)
    response.content
    soup = BeautifulSoup(response.content, 'lxml')
    stat_table = soup.findAll('table')
    print(len(stat_table))
    if len(stat_table) == 0:
        continue
    else:
        rows = stat_table[len(stat_table) - 2].findAll('tr')
    link_list = [a['href'] for a in soup.find_all('a', href=True)]
    for row in rows:
        data.append(str(row.find_all('td')[2].text))
        data1.append(str(row.find_all('td')[1].text))
    for row in link_list:
        data3.append(str(row))
cols = {'Field:' : data, 'Data:' : data1,'Data3:' :data3}
df = pd.DataFrame(cols)
df.columns = ['Field', 'Data', 'Data3']
#----------------------------------------------#
#df.columns = df.iloc[0]
#df = df[1:]
df['Field']=df['Field']
df['Data']=df['Data']
df['Data3']=df['Data3']
#df['Field']=df['Field'].str.decode('utf-8')
#df['Data']=df['Data'].str.decode('utf-8')
#df['Data3']=df['Data3'].str.decode('utf-8')
df.to_csv('NREGA_jobcards_Nagpur_District.csv', index=True, header=False, encoding = 'utf-8')

#-------------------------------------------------#Scrape without hidden ref
#print(type(stat_table_data))
#append_final = ""
#with open ('pythonscrape.csv', 'w', encoding='utf-8') as r:
#    for row in stat_table_data.find_all(['tr']):
#        append = ""
#        for cell in row.find_all('td')[1:3]:
#            append = append+","+ cell.text
#        if len(append) != 0:
#            append_final = append_final + append[1:]
#file = open(os.path.expanduser("pythonmagic_new.csv"), "wb")
#file.write(bytes(append_final, encoding = 'utf-8'))
#------------------------------------------------# Cascaded csv
#rows = stat_table_data.findAll("tr")
#csvfile = open("pythonmagic.csv", 'wt', newline='', encoding='utf-8')
#writer = csv.writer(csvfile)
#try:
#    for row in rows:
#        csvrow = []
#        for cell in row.findAll(['td']):
#            csvrow.append(cell.get_text())
#        writer.writerow(csvrow)
# finally:
#    csvfile.close()
#------------------------------------------------# Print the output
#print(cell.text.encode('utf-8'))
