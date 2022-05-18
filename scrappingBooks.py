"""/* ######################################################### */
/* @author                                                   */
/* @Lucas Santiago Rodrigues -- lucas1613@gmail.com          */
/* ######################################################### */"""

get_ipython().system(' pip install selenium')
get_ipython().system(' pip install pandasql')


import pandas as pd
from glob import glob ## to search and list downloaded files
from selenium import webdriver ## to get links and ROI pages
from selenium.webdriver.common.by import By

import numpy as np

from pandasql import sqldf ## make possible to run SQL statements over pandas dataframe equally a PostgreSQL or equivalent environment

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


# ## Script to scrape data from Internet giving a URL source -> Save a txt file with all book links from URL
def getLinksPages():
    
    print('\n\n\nScrapping from https://books.toscrape.com/ ...\n\n\n')
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument('log-level=3')

    path_to_chromedriver = "chromedriver"

    driver = webdriver.Chrome(executable_path=path_to_chromedriver,options=chrome_options)

    # go to website
    links = open("./links.txt","w")
    
    driver.get(f"https://books.toscrape.com/index.html")
    sizeItems  = int(driver.find_elements_by_xpath(f"//body[@id='default']/div/div/div/div/form/strong[1]")[0].text) ### get number of total itens in bookstore
    pagNumber  = int(driver.find_elements_by_xpath(f"//body[@id='default']/div/div/div/div/form/strong[3]")[0].text) ### number of elements per page
    
    for i in range(1,int(sizeItems/pagNumber)+1):
        driver.get(f"https://books.toscrape.com/catalogue/page-{i}.html")

        size_of_list  = driver.find_elements_by_xpath(f"//body[@id='default']/div/div/div/div/section/div[2]/ol/li")
        
        for li in size_of_list[1:len(size_of_list)]:
            article = li.find_elements(By.TAG_NAME, "article")[0]
            h3 = article.find_element_by_xpath('.//preceding::h3[1]')
            a = h3.find_elements(By.TAG_NAME, "a")
            links.write(str(a[0].get_attribute('href'))+'\n')
           

    links.close()
    driver.close()
    print('DONE... Saved in ./links.txt file')
    
    sys.exit(0)
    
#################################
#################################
#################################
if __name__ == '__main__':
    getLinksPages() ### function to scrapped data on demand (daily or when requested -- CRON Function)
