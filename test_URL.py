import re
import requests
from bs4 import BeautifulSoup

url = 'http://txzb.miit.gov.cn/DispatchAction.do?efFormEname=POIX14&pagesize=11&page='
req = requests.get(url+'1')
soup = BeautifulSoup(req.text,'html.parser')
soup_utf = soup.decode('utf8')
#print(soup_utf)

#test = soup.select('table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(4)')
page_number = soup.find_all('td', class_ = "page STYLE1 STYLE4")[1]["page"]
print(page_number)


#string1 = 'page="'
#string2 = '" onMouseOver="javascript:this.style.cursor=\'hand\'">尾页'
#page_number = re.findall(r"page(.*?)尾页", soup_utf)
#print(page_number)
'''
rm_soup = re.compile(r'<[^>]+>', re.S)
sub_compile1 = rm_soup.sub('', soup_utf)

rm_space = re.compile(' ')
sub_compile2 = rm_space.sub('', sub_compile1)

print(sub_compile2)
'''