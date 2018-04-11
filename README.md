# soc1Autodownloader
Python3 script  downloads reading summaries from sociology1 course website


This script downloads reading summaries directly from the course website: https://eee.uci.edu/18w/69004/readingsummaries. Check if the website is still reachable before using this script. 

The script uses external python [requests](http://docs.python-requests.org/en/master/) and [lxml](http://lxml.de) libs
using following commands to install requests and lxml libs: \
*pip3 install lxml* \
*pip3 install requests* \
Requests is used to get the website, and lxml is used to parse the website and find the actually file addresses we need. \
Reading summaries will be downloaded to the corresponding directories. 



  
