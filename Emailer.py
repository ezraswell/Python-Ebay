key = 'EzraSwel-SwellSne-PRD-ced5cedf3-2214bf5d'
import json
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

searches = []

def sendemail(url, title, condition, price):
    msg= MIMEMultipart()
    password = "swellsneakers1!"
    msg["From"]= "swellsneakers@gmail.com"
    msg["To"]= "swellsneakers@gmail.com"
    msg ["Subject"]= "Item Found"
    body = "<a href=\""+ url +"\">" + title + "</a><br><p>Condition: " + condition +"</p><p>Price:" +price +"</p>"
    msg.attach(MIMEText(body, "html"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

with open("searches.txt", "r") as searchfile:
  searches = searchfile.readlines()
with open ("itemid.txt", "r") as itemfile:  
     itemids= itemfile.read().splitlines()
for item in searches:
  search = item.split(',')[0]
  MaxPrice = item.split(',')[1]
  negative = item.split(',')[2]
  url = ('http://svcs.ebay.com/services/search/FindingService/v1\
?OPERATION-NAME=findItemsByKeywords\
&sortOrder=PricePlusShippingLowest\
&buyerPostalCode=07760&SERVICE-VERSION=1.13.0\
&SECURITY-APPNAME=' + key +
'&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&itemFilter(0).name=Condition\
&itemFilter(0).value=New\
&itemFilter(1).name=MaxPrice\
&itemFilter(1).value=' + MaxPrice+\
'&itemFilter(1).paramName=Currency\
&itemFilter(1).paramValue=USD\
&keywords=' + search+ " " + str(negative))
  url = url.replace(" ", "%20")
  apiResult = requests.get(url)
  parseddoc = apiResult.json()
  
  for item in (parseddoc["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]):
        itemid= item["itemId"][0]
        url= item["viewItemURL"][0]
        title = item["title"][0]
        condition = item['condition'][0]['conditionDisplayName'][0]
        price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']
        if itemid in itemids:
            print("Item Already Alerted")
        else: 
            sendemail(url, title, condition, price)
            with open("itemid.txt", "a") as itemfile:
              itemfile.write(itemid + "\n") 
