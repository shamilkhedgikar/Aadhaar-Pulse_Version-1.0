import urllib
import urllib.request
import requests
import csv
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import product
import pandas as pd
import numpy as np
import time
import random
column1 = []
column2 = []
column3 = []
column4 = []
j = [] #list for batching
k = 0 #Naming Files
columns_more_1 = 20 #transactions
columns_more_2 = 7 #seeding
columns_more_3 = 7 #7 column entitlement ()
columns_more_4 = 6
column_headers = str(range(0,columns_more_1,1))
rangelist_1 = list(range(0,columns_more_1,1))
rangelist_2 = list(range(0,columns_more_2,1))
rangelist_3 = list(range(0,columns_more_3,1))
rangelist_4 = list(range(0,columns_more_4,1))
listOfLists_1 = [[] for i in range(columns_more_1)]
listOfLists_2 = [[] for i in range(columns_more_2)]
listOfLists_3 = [[] for i in range(columns_more_3)]
listOfLists_4 = [[] for i in range(columns_more_4)]
chrome_path = "/Users/prakharsharma/Downloads/pulse/code/chromedriver" #CHANGE YOUR chromedriver PATH HERE
driver = webdriver.Chrome(chrome_path)
url = ('https://mahaepos.gov.in/SRC_Trans_Int.jsp')
driver.get(url)
x = ["2720"]
p = ["%03d"% x for x in range(86,87)]
q = ["%05d" % y for y in range(0,100000)]
r = list(map(''.join, product(p, q)))
#Run test by setting SRC values to list below first. CHECK OUTPUT!
# srclist = ['272008522632', '272008522633', '272008522634', '272008522635', '272008522636', '272008522637', '272008522638', '272008522639', '272008522640', '272008522641', '272008522642', '272008522643', '272008522644', '272008522645', '272008522646', '272008522647', '272008522648', '272008522649', '272008522650']
#Disable above line and enable below line:
srclist = list(map(''.join, product(x, r)))
for i in srclist:
    try:
        time.sleep(random.uniform(7, 14))
        k += 1
        print(i)
        textbox = driver.find_element_by_xpath('//*[@id="src_no"]')
        textbox.clear()
        textbox.send_keys(i)
        driver.find_element_by_xpath('//*[@id="container"]/div[1]/button').click()
        html = driver.page_source
        #makesoup!
        soup = BeautifulSoup(html, "lxml")
        tables = soup.findAll('table')
        if len(tables) == 0: #for empty tables, continue to next RC number in list (NO RC Details Found!)
            continue
        else:
            # print(len(tables))
            seeding_table = tables[0]
            seeding_headers = seeding_table.find_all("tr", {'class':'tableheader'})
            for seeding_header in seeding_headers:
                seeding_header.decompose()
                seeding_rows = seeding_table.find_all('tr')
                family_members = seeding_table.find_all('td')
                #print(seeding_rows)
        if len(family_members) > 1: #for empty transaction table; different from no tables(no record!)
            for members in seeding_rows:
                column2.append(i)
                for range_2 in rangelist_2:
                    listOfLists_2[range_2].append(str(members.find_all('td')[range_2].text))
        #-----#
            entitlement_table = tables[1]
            entitlement_headers = entitlement_table.find_all("tr", {'class':'tableheader'})
            for entitlement_header in entitlement_headers:
                entitlement_header.decompose()
                entitlement_rows = entitlement_table.find_all('tr')
                entitlement_columns = entitlement_table.find_all('td')
            if len(entitlement_columns) == 7:
                for entitlement in entitlement_rows:
                    column3.append(i)
                    for range_3 in rangelist_3:
                        listOfLists_3[range_3].append(str(entitlement.find_all('td')[range_3].text))
            elif len(entitlement_columns) == 6:
                for entitlement in entitlement_rows:
                    column4.append(i)
                    for range_4 in rangelist_4:
                        listOfLists_4[range_4].append(str(entitlement.find_all('td')[range_4].text))
        #-----#
            transaction_table = tables[len(tables)-1]
            headers = transaction_table.find_all("tr", {'class':'tableheader'})
            for header in headers:
                header.decompose()
                rows = transaction_table.find_all('tr')
                no_transactions = transaction_table.find_all('td')
        if len(no_transactions) > 1: #for empty transaction table; different from no tables(no record!)
            for row in rows:
                column1.append(i)
                for range in rangelist_1:
                    listOfLists_1[range].append(str(row.find_all('td')[range].text))
        textbox.clear()
        j.append(i)
        print(len(j))
        if len(j) > 1000:

            df = pd.DataFrame(listOfLists_1)
            df2 = pd.DataFrame(listOfLists_2)
            df3 = pd.DataFrame(listOfLists_3)
            df4 = pd.DataFrame(listOfLists_4)
            df = df.T
            df2 = df2.T
            df3 = df3.T
            df4 = df4.T
            df['index'] = column1
            df2['index'] = column2
            df3['index'] = column3
            df4['index'] = column4
            #Attach the below headers to the csv files after they have been created
            #header1 = ["ld.No", "Member Availed", "FPS Shop Id", "Month", "Year", "Availed Date", "Wheat (Kg)", "Rice (Kg)", "Sugar (Kg)", "P Oil (Lt)", "K Oil (Lt) ", "Maize (Kg)", "Jwari (Kg)","Toor Dal (Kg)", "Urad Dal (Kg)", "Channa Dal (Kg)", "Old Toor Dal (Kg)", "Old Urad Dal (Kg)", "Old Chana Dal (Kg)", "Coarse Grain (Kg)", "SRC Id"]
            #header2 = ["Id.No", "Member Name", "Member Name (Local Language)", "Gender", "Age", "Aadhar", "eKYC", "SRC Id"]
            #header3 = ["Wheat (Kg),Rice (Kg), Sugar (Kg), K Oil (LT), Toor Dal (Kg), Urad Dal (Kg),	Channa Dal (Kg)", "SRC Id"]
            #header4 = ["Wheat (Kg)	Rice (Kg), Sugar (Kg), Toor Dal (Kg), Urad Dal (Kg), Channa Dal (Kg)", "SRC Id"]
            df.to_csv('final_scrape_transaction' + str(k) + '.csv', index=True, header = False)#header1 for transactions data
            df2.to_csv('final_scrape_seeding_10' + str(k) + '.csv', index=True, header = False)#header2 for seeding data
            df3.to_csv('final_scrape_entitlement_7_10' + str(k) + '.csv', index=True, header = False)#header3 for 7 column entitlement
            df4.to_csv('final_scrape_entitlement_6_10' + str(k) + '.csv', index=True, header = False)#header4 for 6 column entitlement
            j.clear()
            #fin.
    except Exception as e:
        print(e)