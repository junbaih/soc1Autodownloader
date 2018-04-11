from lxml import html
import requests
import urllib.request
import os
from collections import namedtuple


class WebError(Exception):
    pass 
def get_file_urls(url:str="https://eee.uci.edu/18w/69004/readingsummaries")->(namedtuple):
    readingSummaries = namedtuple("readingSummaries", "bookName, summaries, summaires_path")
    Eitzen = readingSummaries("Eitzen Summaries",set(),"Eitzan Reading Summaries")
    Loewen = readingSummaries("Loewen Summaries",set(),"Lowen Summaries")
    Reader = readingSummaries("Reader Summaries",set(),"Reader Summaries")
    response = None
    try:
        response = requests.get(url)
        tree = html.fromstring(response.content)
        Eitzen_Summaries_l = tree.xpath('//*[@id="module2"]')
        Loewen_Summaries_l = tree.xpath('//*[@id="module3"]')
        Reader_Summaries_l = tree.xpath('//*[@id="module4"]')
        #SummaryMapping = dict(Eitzen_Summaries_l=Eitzen,Loewen_Summaries_l=Loewen,Reader_Summaries_l=Reader)
        for booklist, Scol in [(Eitzen_Summaries_l,Eitzen),(Loewen_Summaries_l,Loewen),(Reader_Summaries_l,Reader)]:
            summaries = booklist[0].cssselect('a')
            for i in summaries:
                #Scol[1].add(i.attrib)
                Scol[1].add(i.attrib['href'])
            #        sample = tree.xpath('//div[@ng-repeat="itinerary in sortedResults | limitTo:numItinsOnPage"]/text()')
        #stringtest = tree.xpath('/html[@lang]')
        
        

        
        #sample = tree.xpath('//*[@id="module3"]/ul/li[3]/div[1]') # tree.xpath('//*[@id="body"]/main/div/ui-view[@class="ng=scope"]')#/ui-view/ui-view/div/div/div[1]')
        #sample2 = tree.xpath('//*[@id="module3"]/ul/li[3]/div[1]')#/ui-view/ui-view/div/div/div[1]')
        #sample3 = tree.xpath('//*[@id="module3"]/ul/li[3]/div[1]/a')
        #sample4 = tree.xpath('//*[@id="pricePoint0"]')
        #sample5 = tree.xpath('//@parameter2')
#        sample = tree.cssselect('div[ui-view su-block class = "ng-scope"]')
        #flightlist = tree.find_class("col-md-8")
        #print(stringtest[0].attrib)
        #print(sample)
        #for i in sample:
        #    print(i.body)
        #for i in sample3:
        #    print(i.attrib['href'])
        #print(sample2)
        #print(sample3)
        #print(sample4)
        #print(sample5)
    except:
        raise WebError
    finally:
        return (Eitzen,Loewen,Reader)

def filedownload(url:str,target_path:str)->bool:

    filename = url.split("/")[-1]
    for f in os.scandir(target_path):
        if filename == f.name:
            print("ALREADY EXISTS ",filename)
            return False
    print("DOWNLOADING NOW ========> ",filename)
    urllib.request.urlretrieve(url, target_path+'/'+filename)
    return True
def main():
    print("===================== Downloader Start========================")
    fc = []
    for bookSummariesCollection in get_file_urls():
        folder_path = bookSummariesCollection[2]
        collection = bookSummariesCollection[1]
        for summary_url in collection:
            if filedownload(summary_url, folder_path):
                fc.append(summary_url.split('/')[-1])
    banner = "=============Synchronization Complete=====================\n"
    for newsummary in fc:
        banner+="++ "+newsummary+'\n'
    banner+="=================== 0 New Summary  =======================" if len(fc)==0 else \
    "========================= {} New Summaries=======================".format(str(len(fc)))
    print(banner)
    input("Press any key to exit")
    
if __name__ == "__main__":
    main()
