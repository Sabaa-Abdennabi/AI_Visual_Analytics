# main.py
from scraper import scrape
import json

url = "https://www.zalando.fr/puma-cassia-baskets-basses-rosebay-white-rose-quartz-vapor-gray-sugared-almond-pu111a0s5-j11.html"
data = scrape(url)

print(json.dumps(data[:5], indent=2))  # print first 5 elements
# Save the data to a text file
with open("outputs/output_chat2.txt", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print("Data saved to output.txt")