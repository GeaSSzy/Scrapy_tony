import requests
from bs4 import BeautifulSoup
import re

with open('/Users/geass/Desktop/test1.html','r') as test:
    soup = BeautifulSoup(test,'html.parser')




    testP = soup.find_all('span')
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('',str(test))
    print(dd)


    '''
    for a in testP:
        #print(a.get_text())

        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', a.get_text())
        print(dd[0:5])
    
    print(soup.get_text())
    '''
