import requests
from bs4 import BeautifulSoup
import csv
import math

#Initiate lists
links = []
data = []
pageHome = []

#Initiate BeautifulSoup
urlSite = "https://books.toscrape.com/index.html"
urlCatalog = "https://books.toscrape.com/catalogue/"
request = requests.get(urlSite)
soup = BeautifulSoup(request.content, 'html.parser')

# Obtain category's page number
nbPage = soup.find("form", class_="form-horizontal").next_element.next_element.next_element.next_element.next_element.string
nbPage = math.ceil(int(nbPage) / 20.0)

while nbPage != 0:
    pageHome.append(urlCatalog + f"page-{nbPage}.html")
    nbPage = nbPage - 1

#Obtain book's page link
for page in pageHome:
     request = requests.get(page)
     soup = BeautifulSoup(request.content, 'html.parser')
     books = soup.find_all("h3")

     for book in books:
        cutLink = book.next_element["href"].replace("../../..", "")
        print(cutLink)
        links.append(urlCatalog + cutLink)

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
    tableau.append(category.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.string)

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

    # Add tableau in data list
    data.append(tableau)
    print(tableau)

#Initate CSV file
en_tete = ["product_page_url", "title", "category", "review_rating", "image_url", "product_description", "universal_ product_code (upc)", "price_excluding_tax", "price_including_tax", "number_available"]

with open('data.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
   writer = csv.writer(fichier_csv, delimiter=';')
   writer.writerow(en_tete)
   for row in data:
      writer.writerow(row)
