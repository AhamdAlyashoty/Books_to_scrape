import requests
from bs4 import BeautifulSoup
import csv

books_details = []
links = []
types = []

page = requests.get("https://books.toscrape.com/index.html")
src = page.content 
soup = BeautifulSoup(src , 'lxml')

links_types = soup.find("ul" , {'class' : 'nav nav-list'}).contents[1].ul.find_all("li")

for i in links_types :
    links.append(i.a.attrs["href"])
    types.append(i.text.strip())
#print(types)

for i in range (len(links)) :
###################
    page = requests.get(f"https://books.toscrape.com/{links[i]}")
    src = page.content
    soup = BeautifulSoup(src,"lxml")

    all_books = soup.find('ol' , {'class' : 'row'}).find_all('li')

    for book in all_books :
        #get name
        book_name = book.find('h3').text.strip()
        #get price
        book_price = book.find('p' , {'class' : 'price_color'}).text.strip()
        #in stock availability
        in_stock = book.find('p' , {'class' : 'instock availability'}).text.strip()
        #add information
        books_details.append({'type' : types[i] , 'Book Name' : book_name , 'Book Price' : book_price , 'Availability' : in_stock })
    
    print("next type")

keys = books_details[0].keys()
with open ("Books_details.csv" , 'w') as file :
    wr = csv.DictWriter(file , keys)
    wr.writeheader()
    wr.writerows(books_details)
    print("file created")
