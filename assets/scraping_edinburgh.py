import requests
from bs4 import BeautifulSoup

source_code = requests.get('https://www.ed.ac.uk/studying/undergraduate/degrees/index.php?action=degreeList')
soup = BeautifulSoup(source_code.text,'lxml')

BASE_URL = 'https://www.ed.ac.uk'


schools = []

for subject in soup.find('div',{'class':'list-group'}).find_all('a'):
    source_code = requests.get(BASE_URL+subject['href'])
    soup = BeautifulSoup(source_code.text,'lxml')
    p = "\n".join([p.text for p in soup.find('div',{'id':'proxy_introduction'}).find_all('p')])
    school = soup.find('div',{'id':'proxy_rightSummary'}).find('p')
    if school in [s['title'] for s in schools]:
        for s in schools:
            if(school==s['title']):
                s['subjects'].append({'title':subject.text,'desc':p})
    else:
        schools.append({"title":school,"subjects":[{"title":subject.text,"desc":p}]})
    print(schools)
    
