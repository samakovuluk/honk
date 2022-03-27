import requests
import json
import sys
import openpyxl


listing = []


def scrapping(username, amount, session):
    url = f"https://www.carousell.sg/api-service/search/search/3.3/username/{username}/products/"

    payload = "{" + f"\"count\":20,\"countryId\":\"1880251\",\"filters\":[],\"locale\":\"en\", \"session\": \"{session}\"," + "\"sortParam\":{\"ascending\":{\"value\":false},\"fieldName\":\"time_created\"}}"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    data = json.loads(response.text)

    
    products = []
    session = ''
    try:
        session = data['data']['session']
        products = data['data']['results']
    except:
        print(response.text)
        print('finish')
    
    listing.extend(products)
    if(len(listing) < amount and len(products) >= 19 ):
        scrapping(username, amount, session)  
  
def itemParse(item):
    id = item["listingCard"]["id"]
    print(id)
    url = f"https://www.carousell.sg/api-service/listing/3.1/listings/{id}/detail/"

    headers = {
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)

    photos = []
    for group in data['data']['screens'][0]['groups']:
        if group['id'] == 'photo_group':
            photos = group['fields'][0]['meta']['default_value']
            break
    


    data = data['data']['screens'][0]['meta']['default_value']


    resp = {
        'keyword': link,
        'urlSource': 'https://www.carousell.sg/p/'+ id,
        'title': data['title'],
        'description': data['flattened_description'],
        'category': data['collection']['display_name'],
        'price': data['price']
    }

    for i in range(8):
        if(i < len(photos)):
            resp[f"image{i+1}"] = photos[i]['image_url']
        else:
            resp[f"image{i+1}"] = ''

    return resp
   

book = openpyxl.load_workbook('carouscraperesult.xlsx')
sheet = book.active
listSource = []
for index in range(2,10000000):
    if(sheet[f"B{index}"].value != None):
        listSource.append(sheet[f"B{index}"].value)
    else:
        break

args = sys.argv[1:]

link = args[0]
amount = args[1]
username = link.split('/u/')[1].strip('/')
print(username)
try:
    scrapping(username,int(amount),'')
except:
    print(len(listing))
print(len(listing))
items = []
for item in listing:
    try:
        items.append(itemParse(item))
    except:
        print('scrape')

counter = 0
for index in range(2,10000000):
    if(sheet[f"B{index}"].value == None):
        
        if(counter < len(items)):
            while(items[counter]['urlSource'] in listSource):
                    counter+=1
                    if(counter == len(items)):
                        break
            if(counter == len(items)):
                break
            print(counter)
            if(items[counter]['urlSource'] not in listSource):
                sheet[f"A{index}"].value = items[counter]['keyword']
                sheet[f"B{index}"].value = items[counter]['urlSource']
                sheet[f"E{index}"].value = items[counter]['title'] or ''
                sheet[f"H{index}"].value = items[counter]['description'] or ''
                sheet[f"F{index}"].value = items[counter]['price'] or ''
                sheet[f"I{index}"].value = items[counter]['image1'] or ''
                sheet[f"J{index}"].value = items[counter]['image2'] or ''
                sheet[f"K{index}"].value = items[counter]['image3'] or ''
                sheet[f"L{index}"].value = items[counter]['image4'] or ''
                sheet[f"M{index}"].value = items[counter]['image5'] or ''
                sheet[f"N{index}"].value = items[counter]['image6'] or ''
                sheet[f"O{index}"].value = items[counter]['image7'] or ''
                sheet[f"P{index}"].value = items[counter]['image8'] or ''
                sheet[f"AA{index}"].value = items[counter]['category'] or ''
                book.save('carouscraperesult.xlsx')
                counter+=1
        if(counter == len(items)):
            break
        

