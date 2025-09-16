from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://aviationweather.gov/api/data/metar?ids=KFDK%2CKIAD&hours=0&order=id%2C-obs&sep=true")

row_data = driver.find_element(By.XPATH, '/html/body/pre')
print("Row 1: ", row_data.text)
driver.close()