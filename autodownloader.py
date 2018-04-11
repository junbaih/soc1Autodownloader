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
       
        for booklist, Scol in [(Eitzen_Summaries_l,Eitzen),(Loewen_Summaries_l,Loewen),(Reader_Summaries_l,Reader)]:
            summaries = booklist[0].cssselect('a')
            for i in summaries:
                #Scol[1].add(i.attrib)
                Scol[1].add(i.attrib['href'])
           
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
