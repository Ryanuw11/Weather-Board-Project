import re
import time
from idlelib.textview import ViewFrame

from selenium import webdriver
from selenium.webdriver.common.by import By




print("Starting Scrap...")

URL = "https://aviationweather.gov/api/data/metar?ids=KFDK%2CKIAD%2CKBFR&hours=0&order=id%2C-obs&sep=true"
driver = webdriver.Chrome()
driver.get(URL)

vis_pattern = re.compile(r'\b(M?\d{1,2}(?:/\d+)?SM)\b')
sky_pattern = re.compile(r'\b(?:FEW|SCT|BKN|OVC|VV)\d{3}\b')

def vis_sky(metar_text):
    txt = " ".join(metar_text.split())

    vis_m = vis_pattern.search(txt)
    vis = vis_m.group(1) if vis_m else None

    skies = sky_pattern.findall(txt)
    chosen_sky = [s for s in skies if s.startswith(("BKN", "OVC"))]

    return vis, chosen_sky
CATEGORIES = {
    "VFR" : 1,
    "MVFR" : 2,
    "IFR" : 3,
    "LIFR" : 4,
    "NA" : 5
}

row_data = driver.find_element(By.XPATH, '/html/body/pre').text.strip()

results = {}

for line in row_data.splitlines():
    if not line.startswith(("METAR", "SPECI")):
        continue

    vis, sky = vis_sky(line)


    if vis:
        if vis.startswith("10SM"):
            category = "VFR"
    elif vis.startswith(("5SM","4SM","3SM")):
        category= "MVFR"
    elif vis.startswith(("2SM", "1SM")):
        category = "IFR"
    elif vis.startswith("0SM"):
        category = "LIFR"
    else:
        category = "NA"
else:
    category = "NA"

    category_label = CATEGORIES[category]

    station_id = line.split()[1]

    results[station_id] = {
        "visibility": vis if vis else "N/A",
        "sky": sky if sky else ["N/A"],
        "category_label": category,
        "category_value": category_label
    }

    print (f"{station_id}: {vis or 'No Vis'} | Sky: {' '.join(sky) if sky else 'None'} | Category: {category} ({category_label})")

driver.quit()


    



