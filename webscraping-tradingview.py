from urllib.request import urlopen, Request
from bs4 import BeautifulSoup




##############FOR MACS THAT HAVE ERRORS LOOK HERE################
## https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/

############## ALTERNATIVELY IF PASSWORD IS AN ISSUE FOR MAC USERS ########################
##  > cd "/Applications/Python 3.6/"
##  > sudo "./Install Certificates.command"


url = 'https://www.webull.com/quote/us/gainers'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

stock_data = soup.findAll('div', attrs={'class':'table-cell'})

print(stock_data[1].text)
print(stock_data[3].text)
print(stock_data[4].text)
print(stock_data[1+11].text)
print(stock_data[1+22].text)
print()
counter = 1
for x in range(5):
    name = stock_data[counter].text
    change = float(stock_data[counter + 2].text.strip('+').strip('%'))/100
    lastprice = float(stock_data[counter + 3].text)
    
    prevprice = round(lastprice / (1+change), 2)
    
    print(f"Company Name: {name}")
    print(f"Change %: {change}")
    print(f"Price: {lastprice}")
    print(f"Previous price: {prevprice}")
    print()
    print()

    counter += 11


#SOME USEFUL FUNCTIONS IN BEAUTIFULSOUP
#-----------------------------------------------#
# find(tag, attributes, recursive, text, keywords)
# findAll(tag, attributes, recursive, text, limit, keywords)

#Tags: find("h1","h2","h3", etc.)
#Attributes: find("span", {"class":{"green","red"}})
#Text: nameList = Objfind(text="the prince")
#Limit = find with limit of 1
#keyword: allText = Obj.find(id="title",class="text")

