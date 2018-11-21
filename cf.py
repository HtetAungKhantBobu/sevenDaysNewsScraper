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
f=open('C:\\Users\\G4\\Desktop\\seno\\7dayCrwalRawData.csv','a',encoding='utf-8')
writer=csv.writer(f, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL, lineterminator='\n')

##download and save news data from news page */story/\d$

def getDetails(nl):
    
    pag=BeautifulSoup(scraper.get(nl).text, 'html.parser')
    title=pag.find('h1').text
    detailDate=pag.find('div',{'class':'story-detail-date'}).text
    location=pag.find('div',{'class':'field field-name-field-ref-location field-type-node-reference field-label-hidden'})
    if location is not None:
        location=location.text
    else:
        location='no location'
    issueNo=pag.find('div',{'class':'field field-name-field-ref-issue-no field-type-node-reference field-label-hidden'}).text
    imgdata=pag.find('div',{'class':'story-photo-inner'})
    if imgdata.find('img',src=True) is not None and imgdata.find('div',{'class':'photo-caption'}).text is not None:
        imgLoc=imgdata.find('img',src=True)['src']
        photographer=imgdata.find('div',{'class':'photo-caption'}).text
    else:
        imgLoc='No Image Included'
        photographer='No Photographer'
    body=pag.find('div',{'class':'field field-name-body field-type-text-with-summary field-label-hidden'}).text
    resultList=[title,detailDate,location,issueNo,imgLoc,photographer,body]
    #f.write(nl+"\n"+title+'\n'+detailDate+'\n'+location+'\n'+issueNo+'\n'+imgLoc+'\n'+photographer+'\n'+body)
    writer.writerow(resultList)


#please change to appropriate category link O_o 
soup=BeautifulSoup(scraper.get("http://www.7daydaily.com/news").text, 'html.parser')
#for urljoin(). I'm too lazy T_T
aDomain="http://www.7daydaily.com"
#flag is for scraping all pagers!
flag=True
count=0
#scrap first 25 pagers approx 500 news
while count<25:
    print("pager "+str(count)+".......")
    newsTitle=soup.find_all('div',{'class':'taxonomy_title'})
    for i in newsTitle:
        at=i.find('a',href=True)['href']
        print("Downloading "+str(at))
        getDetails(urljoin(aDomain,at))
        time.sleep(3)
        print("Done")
    nextLink=soup.find('li',{'class':'pager-next'}).find('a',href=True)['href']
    soup=BeautifulSoup(scraper.get(urljoin(aDomain,nextLink)).text, 'html.parser')
    count+=1
    print("Done")
f.close()



