import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By




print("Starting Scrap...")

URL = "https://aviationweather.gov/api/data/metar?ids=KFDK%2CKIAD&hours=0&order=id%2C-obs&sep=true"
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

row_data = driver.find_element(By.XPATH, '/html/body/pre').text.strip()

for line in row_data.splitlines():
    if not line.startswith(("METAR", "SPECI")):
        continue

    vis, sky = vis_sky(line)

    if vis and sky:
        print(vis, " ".join(sky))
    elif vis:
        print(f"{vis} (no BKN or OVC")
    elif sky:
        print(" ".join(sky))
    else:
        print("No visibility or sky layer found:")

driver.quit()
    



