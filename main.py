import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#Initialisation du tableau
tableau = []

#URL Page
tableau.append(url)

#title
title = soup.find("li", class_="active").string
tableau.append(title)

#Category
category = soup.find("ul", class_="breadcrumb")
tableau.append(category.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.string)

#Stars
stars = soup.find("p", class_="star-rating")
tableau.append(stars["class"][1])

#image URL
imgURL = soup.find("img")
imgURL = "http://books.toscrape.com/" + imgURL["src"]
tableau.append(imgURL)

#Product Description
description = soup.find("div", class_="sub-header")
tableau.append(description.next_element.next_element.next_element.next_element.next_element.next_element.string)

#Product Information
table = soup.find_all("td")
tableau.append(table[0].string)
tableau.append(table[2].string)
tableau.append(table[3].string)
tableau.append(table[5].string)

print(tableau)

en_tete = ["product_page_url", "title", "category", "review_rating", "image_url", "product_description", "universal_ product_code (upc)", "price_excluding_tax", "price_including_tax", "number_available"]

with open('data.csv', 'w') as fichier_csv:
   writer = csv.writer(fichier_csv, delimiter=';')
   writer.writerow(en_tete)
   writer.writerow(tableau)