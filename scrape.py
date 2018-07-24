#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import urllib
import json
import time

url = 'https://www.facebook.com/careers/jobs/?q=integrity&page={}'
base_url = 'https://www.facebook.com/'

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)

for page in range(1,25):
    driver.get(url.format(page))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for job_link in soup.find(id='search_result').find_all('a', href=re.compile('/careers/jobs/')):
        job_url = job_link['href']
        job_url = urllib.parse.urljoin(base_url, job_url)
        driver.get(job_url)

        job_soup = BeautifulSoup(driver.page_source, 'lxml')
        title_el = job_soup.find('h4')
        if title_el is None:
            time.sleep(5)
            driver.refresh()
            job_soupp = BeautifulSoup(driver.page_source, 'lxml')
            title_el = job_soup.find('h4')
        title = title_el.get_text()
        location = title_el.next_sibling.span.get_text()
        all_text = job_soup.find(href='/careers/jobs/').parent.next_sibling.get_text(" ")
        print(json.dumps({'url': job_url, 'title': title, 'location': location, 'description': all_text}))



#search_results = driver.find_elements(By.XPATH, '//div[@id="search_result"]/a')
#for link in search_results:
#    print(link.get_attribute('href'))
#    link.click()
#    job_soup = BeautifulSoup(driver.page_source, 'lxml')
#    print(job_soup.get_text())
#    driver.execute_script("window.history.go(-1)")
    
