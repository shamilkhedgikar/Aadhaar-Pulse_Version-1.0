from bs4 import BeautifulSoup
import requests as r
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, TimeoutException, WebDriverException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import time
import os
from lxml import etree
from lxml.etree import tostring

driver = webdriver.Chrome("C:\\Users\\31106\\PycharmProjects\\ClassTest\\chromedriver_win32\\chromedriver.exe") #Set the path for your webdriver here
chromeoptions = webdriver.ChromeOptions()


def get_fto_details (driver, i):
    fto_element = driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/table[5]/tbody/tr[' + i + ']/td[2]/a')
    driver.get("http://mnregaweb4.nic.in/netnrega/FTO/fto_reprt_detail.aspx?lflag=&flg=W&page=d&state_name=MAHARASHTRA&state_code=18&district_name=NAGPUR&district_code=1827&fin_year=2018-2019&typ=pb&mode=b&source=national&Digest=wjzxUmDb9vV/8ZuyJfYOWg")
    fto_element.click()
    time.sleep(30)
    excel_trans_element = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_LinkButton2"]')
    excel_trans_element.click()
    time.sleep(30)

    fto_name_temp = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Label1"]/b').text
    print(fto_name_temp)
    str1 = fto_name_temp.replace(" ", "")
    str2 = str1.replace(".", "")
    str3 = str2.replace(":", "")
    print(str3)

    filetype = ".xls"
    rep = str(ftorep)
    new_name = str3 + "_REP" + rep + filetype
    old_file = os.path.join("C:\\Users\\31106\\Downloads", "fto_trasction_dtl.xls") #Reset this to your Downloads folder
    new_file = os.path.join("C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\ftos_raw_jh\\ftos_partialprocessed_jh", new_name) #Reset this to wherever you want to save the data
    os.rename(old_file, new_file)



fto_num = range(2, 6881)
ftorep = 0

for num in fto_num:
    print(num)
    while True:
        try:
            i = str(num)
            get_fto_details(driver, i)
            num = num + 1
            break
        except NoSuchElementException:
            driver.quit()
            driver = webdriver.Chrome("D:\Downloads\chromedriver_win32\\chromedriver.exe", chrome_options=chromeoptions)
            continue
        except TimeoutException:
            driver.quit()
            driver = webdriver.Chrome("D:\Downloads\chromedriver_win32\\chromedriver.exe", chrome_options=chromeoptions)
            continue
        except WebDriverException:
            driver.quit()
            driver = webdriver.Chrome("D:\Downloads\chromedriver_win32\\chromedriver.exe", chrome_options=chromeoptions)
            continue
        except FileExistsError:
            ftorep = ftorep + 1
            driver.quit()
            driver = webdriver.Chrome("D:\Downloads\chromedriver_win32\\chromedriver.exe", chrome_options=chromeoptions)
            continue


##### Code to save the downloaded files as CSVs ####

fto_path = "C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\ftos_raw_jh\\ftos_fullyprocessed_jh"
fto_list = os.listdir(fto_path)

for each_file in fto_list:
    filename = fto_path + "\\" + str(each_file)
    data = pd.read_html(filename)
    df = data [0]
    print(type(df))
    df.to_csv("C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\ftos_csv_jh\\jh_ftos_csv_processed\\"+ str(each_file)+ ".csv")


fto_csv_path = "C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\ftos_csv_jh\\jh_ftos_csv_processed"
fto_csv_list = os.listdir(fto_csv_path)

for each_csv_file in fto_csv_list:
    csv_filename = fto_csv_path + "\\" + str(each_csv_file)
    name_to_append = str(each_csv_file)
    dfcsv = pd.read_csv(csv_filename)
    dfcsv.insert(3, column='fto_num', value=name_to_append, allow_duplicates='true')
    #print(type(dfcsv))
    dfcsv.to_csv("C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\ftos_csv_nameappended_jh\\jh_ftos_csv_name_processed" + "\\" + str(each_csv_file)+ ".csv")
    continue


##### Code to append all CSVs ####

path = "C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\ftos_csv_nameappended_jh\\jh_ftos_csv_name_processed"
files = os.listdir(path)

merged = []

for each in files:
    f = "C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\ftos_csv_nameappended_jh\\jh_ftos_csv_name_processed\\" + str(each)
    read = pd.read_csv(f)
    merged.append(read)

result = pd.concat(merged)
result.to_csv("C:\\Users\\31106\\Documents\\MGNREGA\\scraped_data\\Jharkhand\\ftos_jh\\jh_fto_processed_merged.csv")
