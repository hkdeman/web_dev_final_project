import requests
from bs4 import BeautifulSoup
import json

#https://www.gla.ac.uk/schools/ take the subjects and their course teachers

source_code = requests.get('https://www.gla.ac.uk/schools/')
soup = BeautifulSoup(source_code.text,'lxml')

schools = []

for school in soup.find('div',{'class':'maincontent'}).find('ul').find_all('a'):
    schools.append({"title":school.text,"url":school['href']})

BASE_URL = "https://www.gla.ac.uk"
STAFF_URL = "staff/"

for school in schools:    
    source_code = requests.get(BASE_URL+school['url']+STAFF_URL)
    soup = BeautifulSoup(source_code.text,'lxml')
    teachers = []
    for teacher in soup.find('ul',{'class':'longlist'}).find_all('li'):
        teachers.append(teacher.text)
    school['teachers']=teachers
    break




