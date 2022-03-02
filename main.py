import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#Initialisation du tableau
tableau = []

#URL de la page
tableau.append(url)

#Tire du livre
titre = soup.find("li", class_="active").string
tableau.append(titre)

#Product Description
description = soup.find("div", class_="sub-header")
tableau.append(description.next_element.next_element.next_element.next_element.next_element.next_element.string)

#Product information
table = soup.find_all("td")
tableau.append(table[0].string)
tableau.append(table[2].string)
tableau.append(table[3].string)
tableau.append(table[5].string)

#Category
category = soup.find("ul", class_="breadcrumb")
tableau.append(category.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.string)

#image URL
imgURL = soup.find("img")
imgURL = "http://books.toscrape.com/" + imgURL["src"]
tableau.append(imgURL)

#Stars
stars = soup.find("p", class_="star-rating")
tableau.append(stars["class"][1])

print(tableau)

