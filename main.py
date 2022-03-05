import requests
from bs4 import BeautifulSoup
import csv

#Initate CSV file
en_tete = ["product_page_url", "title", "category", "review_rating", "image_url", "product_description", "universal_ product_code (upc)", "price_excluding_tax", "price_including_tax", "number_available"]

with open('data.csv', 'w') as fichier_csv:
   writer = csv.writer(fichier_csv, delimiter=';')
   writer.writerow(en_tete)

#Initiate lists
links = []

#Initiate BeautifulSoup
#url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html"
urlCatalog = "https://books.toscrape.com/catalogue"
urlSite = "https://books.toscrape.com"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#Obtain book's page link
books = soup.find_all("h3")
for book in books:
   cutLink = book.next_element["href"].replace("../../..", "")
   links.append(urlCatalog + cutLink)

print(links)

for link in links:
   #Initate BeautifulSoup for loop
   page = requests.get(link)
   soup = BeautifulSoup(page.content, 'html.parser')

   # Initialisation du tableau
   tableau = []

   # URL Page
   tableau.append(link)

   # title
   title = soup.find("li", class_="active").string
   tableau.append(title)

   # Category
   category = soup.find("ul", class_="breadcrumb")
   tableau.append(
      category.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.string)

   # Stars
   stars = soup.find("p", class_="star-rating")
   tableau.append(stars["class"][1])

   # image URL
   imgURL = soup.find("img")
   imgURL = imgURL["src"].replace("../..", "")
   imgURL = urlSite + imgURL
   tableau.append(imgURL)

   # Product Description
   description = soup.find("div", class_="sub-header")
   tableau.append(description.next_element.next_element.next_element.next_element.next_element.next_element.string)

   # Product Information
   table = soup.find_all("td")
   tableau.append(table[0].string)
   tableau.append(table[2].string)
   tableau.append(table[3].string)
   tableau.append(table[5].string)

   print(tableau)

   with open('data.csv', 'a') as fichier_csv:
      writer = csv.writer(fichier_csv, delimiter=';')
      writer.writerow(tableau)
