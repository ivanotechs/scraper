import requests
from bs4 import BeautifulSoup
import csv


prod_list=[] #stores the list of products without descriptions
completed_list = [] # complete product list
for i in range(1, 21):
    URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"+str(i) #variable URL to iterate on all the 20 pages

    r = requests.get(URL)

    print(r)




    soup = BeautifulSoup(r.content, 'lxml')

    
    table = soup.find_all('div', attrs = {'data-component-type':'s-search-result'}) #getting all the products who is of component type search results

    for row in table:
        product = {}
        product['URL'] = "https://www.amazon.in"+str(row.h2.a['href'])
        product['ProductName'] = row.h2.text
        product['price'] = row.find('span', attrs = {'class' : 'a-price'}).text
        product['Rating'] = row.find('span', attrs = {'class' : 'a-icon-alt'}).text
        product['Reviews'] = row.find('span', attrs = {'class':'a-size-base s-underline-text'}).text
        prod_list.append(product)


#collecting URLs of specific products and hiting them to have their details
for product in prod_list:
    URL = product['URL']
    print(URL)


    webpage = requests.get(URL)
    print(webpage)

    soup = BeautifulSoup(webpage.content, "lxml")

    try:
        Description = soup.find("span",
                        attrs={"id": 'productTitle'}).text



        manufacturer = str(soup.find('div', attrs = {'class' : 'a-section a-spacing-none'}).text)
        product['ProductDescription'] = Description
        product['Manufacturer'] = manufacturer
        completed_list.append(product)
    except Exception:
        print(Exception)
        continue

filename = 'products.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['URL','ProductName','price','Rating','Reviews', 'ProductDescription', 'Manufacturer'])
    w.writeheader()
    for prod in completed_list:
        w.writerow(prod)

print("done")