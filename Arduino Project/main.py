import resp
from lxml import html
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape():
    print("Starting Scrap...")


    driver = webdriver.Chrome()

    driver.get("https://aviationweather.gov/api/data/metar?ids=KFDK%2CKIAD%2CPADK&hours=0&order=id%2C-obs&sep=true")

    row_data = driver.find_element(By.XPATH, '/html/body/pre')
    print(row_data.text)

    driver.close()
    time.sleep(2)
    print("Finished")
    
while True:
    scrape()
    print("Mandatory 10 second wait from Robot.txt")
    time.sleep(10)


if __name__ == '__main__':
    scrape()