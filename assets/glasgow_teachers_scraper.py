import pip
import json
import time

try:
    import requests
    from bs4 import BeautifulSoup 
    from tqdm import tqdm       
except(ImportError):
    pip.main(['install',"requests","lxml","bs4","tqdm"])
    import requests
    from bs4 import BeautifulSoup 
    from tqdm import tqdm

#https://www.gla.ac.uk/schools/ take the subjects and their course teachers

source_code = requests.get('https://www.gla.ac.uk/schools/')
soup = BeautifulSoup(source_code.text,'lxml')

schools = []

for school in soup.find('div',{'class':'maincontent'}).find('ul').find_all('a'):
   schools.append({"title":school.text,"url":school['href']})

BASE_URL = "https://www.gla.ac.uk"
STAFF_URL = "staff/"

all_contacts = {}


for school in tqdm(schools,desc="Schools"):
    if(schools.index(school)==14 or schools.index(school)==17):
        continue 
    source_code = requests.get(BASE_URL+school['url']+STAFF_URL)
    soup = BeautifulSoup(source_code.text,'lxml')
    if not school['title'] in all_contacts.keys():
        all_contacts[school['title']] = []
    for teacher in tqdm(soup.find('ul',{'class':'longlist'}).find_all('li'),desc="teachers"):
        teacher_source_code = requests.get(BASE_URL+teacher.a['href'])
        teacher_soup = BeautifulSoup(teacher_source_code.text,'lxml')
        has_image = True
        image =  None
        try:
            image = BASE_URL+teacher_soup.find("div",{"id":"sp_staffphoto"}).find('img')['src']
        except:
            has_image = False
        
        contact = None
        try:
            contact = [c.split(":") for c in filter(None,teacher_soup.find('div',{'id':'sp_contactInfo'}).text.split("\n"))]
            if len(contact) ==2:            
                all_contacts[school['title']].append({"name":teacher.a.text,"contact":{"email":contact[1][1].strip(),"mobile":contact[0][1].strip()},"image":image})
            else:
                all_contacts[school['title']].append({"name":teacher.a.text,"contact":{"mobile":contact[0][1].strip()},"image":image})                
        except:
            all_contacts[school['title']].append({"name":teacher.a.text,"contact":None,"image":image})
#        time.sleep(5)
    time.sleep(15)

with open('glasgow_university_teacher_data.json', 'w') as outfile:
    json.dump(all_contacts, outfile)


