# main.py
from scraper import scrape
import json
#url = "https://www.zalando.fr/puma-cassia-baskets-basses-rosebay-white-rose-quartz-vapor-gray-sugared-almond-pu111a0s5-j11.html"
#url = "https://www.ikea.com/fr/fr/p/besta-rangement-tv-vitrines-blanc-lappviken-blanc-verre-transparent-s79411013/"
#url="https://www.automobile.tn/fr/neuf/mercedes-benz/classe-e"
url="https://fr.shein.com/hotsale/bestsellerfr-sc-003833455.html?adp=44263949&fromPageType=home&src_module=all&src_identifier=on%3DPRODUCT_ITEMS_COMPONENT%60cn%3Dsalezone%60hz%3D0%60ps%3D6_6_1%60jc%3DitemPicking_003833455&src_tab_page_id=page_home1744486667286&ici=CCCSN%3Dall_ON%3DPRODUCT_ITEMS_COMPONENT_OI%3D68347231_CN%3DHORIZONTAL_ITEMS_TI%3D50001_aod%3D0_PS%3D6-6_ABT%3D0"
data = scrape(url)

print(json.dumps(data[:5], indent=2))  # print first 5 elements
# Save the data to a text file
with open("outputs/scraping_shein.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print("Data saved to output.txt")