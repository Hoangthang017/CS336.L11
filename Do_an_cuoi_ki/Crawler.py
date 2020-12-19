import urllib3
from bs4 import BeautifulSoup
import time
links = []
text = ''
t = 0
for i in range (501,600):
    url = 'http://www.bongda.com.vn/tin-moi-nhat/'
    # request = urllib2.Request(url)
    # # req = Request(url, headers={'User-User-Agent': 'XYZ/3.0'})
    # request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
    # req = urllib2.urlopen(request)
    # page = urlopen(req)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'html.parser')
    # soup = BeautifulSoup(page, 'html.parser')
    for head in soup.find_all('div', class_='col630 fr'):
        for h in head.find_all('a', class_='expthumb thumb630x330 thumbblock mar_bottom15'):
            links.append(h.get('href'))
        for h in head.find_all('ul', class_='list_top_news list_news_cate'):
            for link_bai in h.find_all('a', class_='title_list_top_news'):
                links.append(link_bai.get('href'))
    url = 'http://www.bongda.com.vn/tin-moi-nhat/p' + str(i+2);
for link in range(len(links)):
    if t==17:
        time.sleep(1)
        t = 0
    url_data= 'data/' + str(link + 8999) +'.txt'
    # req = Request(links[link], headers={'User-User-Agent': 'XYZ/3.0'})
    # page = urlopen(req)
    # soup = BeautifulSoup(page, 'html.parser')
    http = urllib3.PoolManager()
    response = http.request('GET', links[link])
    soup = BeautifulSoup(response.data, 'html.parser')
    i = 0
    txt= ''
    for head in soup.find_all('div', class_='exp_content news_details'):
        for h in head.find_all('p'):
            if i == 0:
                i = 1
            else:
                txt+=h.text
    if txt == '':
        continue
    else:
        with open(url_data, 'a+', encoding ='utf-8') as file:
            file.write(txt)
            file.close()
    t += 1