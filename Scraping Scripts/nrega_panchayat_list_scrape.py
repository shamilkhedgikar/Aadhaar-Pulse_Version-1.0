from bs4 import BeautifulSoup
soup = BeautifulSoup(open("panchayat_list.html"), "html.parser")
panchayat_list=[]
panchayat_list = [a['value'] for a in soup.find_all('option', value=True)]
print(panchayat_list)
print(panchayat_list[1])
