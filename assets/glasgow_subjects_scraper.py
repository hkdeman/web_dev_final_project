import requests
from bs4 import BeautifulSoup
import json

#https://www.gla.ac.uk/schools/ take the subjects and their course teachers

source_code = requests.get('https://www.gla.ac.uk/coursecatalogue/browsebydepartment/')
soup = BeautifulSoup(source_code.text,'lxml')

fields = []
BASE_URL = "https://www.gla.ac.uk"

for field in soup.find('div',{'class':'maincontent fullwidth'}).find_all('a'):
    source_code = requests.get(BASE_URL+field['href'])
    soup = BeautifulSoup(source_code.text,'lxml')
    subjects = []
    for year in soup.find('div',{'class':'maincontent fullwidth'}).find_all('ul'):
        for a in year.find_all('a'):
            subject_source_code = requests.get(BASE_URL+a['href'])
            soup = BeautifulSoup(subject_source_code.text,'lxml')
            desc = list(filter(None, [l.text for l in soup.find_all('p')]))[4]
            subjects.append({"url":a['href'],"title":a.text.strip(),"description":desc.strip()})
    fields.append({"link":field['href'],"title":field.text,'subjects':subjects})

with open('glasgow_university_data.json', 'w') as outfile:
    json.dump(fields, outfile)
