from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import pandas as pd

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_experimental_option("detach", True)


list_addresses = []
details = []
whole_price = []
titles= []
web_links = []

# Get number of pages that i want to scrape 
driver = webdriver.Chrome(options=chrome_opt)
driver.get("https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/wiele-lokalizacji?limit=48&ownerTypeSingleSelect=ALL&areaMin=30&areaMax=80&locations=%5Bmalopolskie%2Fkrakow%2Fkrakow%2Fkrakow%2Fgrzegorzki%2Cmalopolskie%2Fkrakow%2Fkrakow%2Fkrakow%2Fpodgorze%2Cmalopolskie%2Fkrakow%2Fkrakow%2Fkrakow%2Fdebniki%5D&by=LATEST&direction=DESC&viewType=listing&page=")
time.sleep(1)
num_of_listenings  = driver.find_element(by= By.CSS_SELECTOR, value=".css-15svspy").text
pages = num_of_listenings.split(" ")[-1]
pages = math.ceil(int(pages)/48)
driver.quit()

# Scrape data from websites 
def get_data():
    names = driver.find_elements(by=By.CSS_SELECTOR, value=".css-u3orbr")
    for title in names:
        titles.append(title.text)
    addresses = driver.find_elements(by=By.CSS_SELECTOR, value=".css-42r2ms")
    for adres in addresses:
        list_addresses.append(adres.text)
    flat_price = driver.find_elements(By.CSS_SELECTOR, value= ".css-2bt9f1")
    for price in flat_price:
        whole_price.append(price.text)
    rooms_m_price_floor = driver.find_elements(by=By.CSS_SELECTOR, value=".css-12dsp7a")
    for data in rooms_m_price_floor:
        details.append(data.text)
    links = driver.find_elements(by=By.CSS_SELECTOR, value= ".css-13gthep a")
    for link in links:
        web_links.append(link.get_attribute("href"))
        
    time.sleep(3)

# Mechanism for opening next pages and calling data scraping 
for i in range(1,pages+1):
    driver = webdriver.Chrome(options=chrome_opt)
    next_url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/wiele-lokalizacji?limit=48&ownerTypeSingleSelect=ALL&areaMin=30&areaMax=80&locations=%5Bmalopolskie%2Fkrakow%2Fkrakow%2Fkrakow%2Fgrzegorzki%2Cmalopolskie%2Fkrakow%2Fkrakow%2Fkrakow%2Fpodgorze%2Cmalopolskie%2Fkrakow%2Fkrakow%2Fkrakow%2Fdebniki%5D&by=LATEST&direction=DESC&viewType=listing&page={i}"
    driver.get(next_url)
    time.sleep(2)
    cookies = driver.find_element(By.CSS_SELECTOR, value = "#onetrust-accept-btn-handler")
    cookies.click()
    time.sleep(1)
    get_data()
    time.sleep(1)
    # print(f"Navigated to: {driver.current_url}")
    driver.quit()
    time.sleep(1)

# Breakdown details info into separate values. There is 1 string that is being split into 4 values 
rooms = []
living_area = []
price_m = []
floor = []
for i in range(len(details)):
    record = details[i].split("\n")
    rooms.append(record[1]) if len(record) > 1 else rooms.append("n/a") 
    living_area.append(record[3].split(" ")[0]) if len(record) > 1 else living_area.append("n/a") 
    price_m.append(record[5].replace("zł/m²", "").replace(" ", "").replace(",", ".")) if len(record) > 1 else price_m.append("n/a") 
    floor.append(record[-1]) if len(record) == 8 else floor.append("n/a")


whole_price_fin = [price.replace("zł", "").replace(" ", "").replace(",", ".") for price in whole_price]

# Combine data into key values 
data = {"Links": web_links, "Title" : titles , "Adress": list_addresses, "Price":whole_price_fin, "Price per m2": price_m, "Floor":floor, "Living area": living_area, "Rooms" : rooms, }

# Data cleansing 
df = pd.DataFrame(data)
df = df.drop_duplicates(["Title", "Adress"], keep='last')
df = df.replace(['', 'n/a'], pd.NA)
df = df.dropna()
df["Living area"] = df["Living area"].astype(float)
df["Price"] = df["Price"].astype(float)
df["Price per m2"] = df["Price per m2"].astype(float)
df.to_excel("apartmets.xlsx", index=False)
