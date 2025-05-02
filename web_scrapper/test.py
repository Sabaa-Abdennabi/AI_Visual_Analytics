# main.py
from scraper import scrape
import json
#url = "https://www.zalando.fr/puma-cassia-baskets-basses-rosebay-white-rose-quartz-vapor-gray-sugared-almond-pu111a0s5-j11.html"
#url = "https://www.ikea.com/fr/fr/p/besta-rangement-tv-vitrines-blanc-lappviken-blanc-verre-transparent-s79411013/"
url="https://www.automobile.tn/fr/neuf/mercedes-benz/classe-e"
data = scrape(url)

print(json.dumps(data[:5], indent=2))  # print first 5 elements
# Save the data to a text file
with open("outputs/scraping_outputmercedes.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print("Data saved to output.txt")