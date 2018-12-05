##this python script uses cfscrape
##so cfscrape module and node.js should be imstalled first
##gomenyasei for inconvenience >_<

import cfscrape
from bs4 import BeautifulSoup
from urllib.request import urljoin
import time
import csv

scraper = cfscrape.create_scraper()
##prox={
##    'http': 'http://188.127.233.134:60077'
##    }

##please change file path >_<
f=open('7dayCartoons.csv','a',encoding='utf-8')
writer=csv.writer(f, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL, lineterminator='\n')

logfile=open('7daylog.txt','r',encoding='utf-8')
seen=set([i.rstrip() for i in logfile.readlines()])
logfile.close()
logfile=open('7daylog.txt','a',encoding='utf-8')



##download and save news data from news page */story/\d$

def getDetails(nl):
    
    pag=BeautifulSoup(scraper.get(nl).text, 'html.parser')
    
    footer=pag.find('footer',{'class':'submitted'})
    spans=footer.findAll('span')
    Date=spans[0].text
    cartoonist=spans[1].text

    divs=pag.find_all('div',{'class':'field-item even'})
    issueNo=divs[0].text
    imgtag=divs[1].find('img',src=True)
    imglink=imgtag['src']
            
    resultList=[Date,cartoonist,issueNo,imglink]
    #f.write(nl+"\n"+title+'\n'+detailDate+'\n'+location+'\n'+issueNo+'\n'+imgLoc+'\n'+photographer+'\n'+body)
    writer.writerow(resultList)
    #save the link in seen and cache
    seen.add(nl)
    logfile.write(nl+"\n")


#please change to appropriate category link O_o 
soup=BeautifulSoup(scraper.get("http://www.7daydaily.com/cartoons").text, 'html.parser')
#for urljoin(). I'm too lazy T_T
aDomain="http://www.7daydaily.com"
#flag is for scraping all pagers!
flag=True
count=0
#scrap first 25 pagers approx 500 news
while flag:
    print("pager "+str(count)+".......")
    imglinks=soup.find('div',{'class':'view-content'})
    newsTitle=imglinks.findAll('a',href=True)
    print(len(newsTitle))
    for i in newsTitle:
        at=i['href']
        print("... "+str(at))
        nurl=urljoin(aDomain,at)
        if nurl not in seen:
            getDetails(nurl)
        else:
            print(" ")
        time.sleep(3)
        print("Done")
    nextLink=soup.find('li',{'class':'pager-next'}).find('a',href=True)['href']
    if nextLink is not None:
        soup=BeautifulSoup(scraper.get(urljoin(aDomain,nextLink)).text, 'html.parser')
    else:
        flag=False
    count+=1
    print("Done")
writer.close()
f.close()
f.close()




