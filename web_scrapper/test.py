# main.py
from scraper import scrape
import json

url = "https://crk.tn/categorie-produit/homme/sacs-homme/"
data = scrape(url)

print(json.dumps(data[:5], indent=2))  # print first 5 elements
# Save the data to a text file
with open("outputs/output_chat2.txt", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print("Data saved to output.txt")