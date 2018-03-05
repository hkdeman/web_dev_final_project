import requests
from bs4 import BeautifulSoup
import json


source_code = requests.get("https://www.thecompleteuniversityguide.co.uk/league-tables/rankings")
soup = BeautifulSoup(source_code.text,"lxml")

universities = []

for uni in soup.find_all('td',{'class':'league-table-institution-name'})[:50]:
    universities.append(uni.a.text)

with open('top_50_university_data.json','w') as f:
    json.dump(universities,f)
