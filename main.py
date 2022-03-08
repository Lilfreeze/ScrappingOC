import requests, csv, math, os.path, ssl, wget
from bs4 import BeautifulSoup

# Initiate lists
links = []
data = []
pageHome = []
category = []
en_tete = ["product_page_url", "title", "category", "review_rating", "image_url", "product_description",
           "universal_ product_code (upc)", "price_excluding_tax", "price_including_tax", "number_available"]

if not os.path.exists("export"):
    os.mkdir("export")

if not os.path.exists("img"):
    os.mkdir("img")

# Initiate BeautifulSoup
urlSite = "https://books.toscrape.com/index.html"
urlCatalog = "https://books.toscrape.com/catalogue/"
request = requests.get(urlSite)
soup = BeautifulSoup(request.content, 'html.parser')

# Obtain category's page number
nbPage = soup.find("form",
                   class_="form-horizontal").next_element.next_element.next_element.next_element.next_element.string
nbPage = math.ceil(int(nbPage) / 20.0)

while nbPage != 0:
    pageHome.append(urlCatalog + f"page-{nbPage}.html")
    nbPage = nbPage - 1

# Obtain book's page link
for page in pageHome:
    request = requests.get(page)
    soup = BeautifulSoup(request.content, 'html.parser')
    books = soup.find_all("h3")

    for book in books:
        cutLink = book.next_element["href"].replace("../../..", "")
        links.append(urlCatalog + cutLink)

for link in links:
    # Initate BeautifulSoup for loop
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
    category = soup.find("ul", class_="breadcrumb").next_element.next_element.next_element.next_element.next_element. \
        next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element. \
        next_element.next_element.next_element.string
    tableau.append(category)

    # Stars
    stars = soup.find("p", class_="star-rating")
    tableau.append(stars["class"][1])

    # image URL
    imgURL = soup.find("img")
    imgURL = imgURL["src"].replace("../..", "")
    imgURL = urlSite.replace("/index.html", "") + imgURL
    tableau.append(imgURL)

    # Download image
    ssl._create_default_https_context = ssl._create_unverified_context
    file_name = wget.download(imgURL, ".\img")

    # Product Description
    description = soup.find("div", class_="sub-header")
    tableau.append(description.next_element.next_element.next_element.next_element.next_element.next_element.string)

    # Product Information
    table = soup.find_all("td")
    tableau.append(table[0].string)
    tableau.append(table[2].string)
    tableau.append(table[3].string)
    tableau.append(table[5].string)

    # Export in category file
    if os.path.exists(f"export\data-{category}.csv"):
        with open(f"export\data-{category}.csv", 'a', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=';')
            writer.writerow(tableau)

    else:
        with open(f"export\data-{category}.csv", 'w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=';')
            writer.writerow(en_tete)
            writer.writerow(tableau)
