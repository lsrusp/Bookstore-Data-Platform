"""/* ######################################################### */
/* @author                                                   */
/* @Lucas Santiago Rodrigues -- lucas1613@gmail.com          */
/* ######################################################### */"""


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

import psycopg2

##################################
##################################
##################################
##################################

global dbName
dbName = 'cayenaDB'

# ## Data manipulation and ETL: Functions to map attributes from html files -> Return a list with all extract books information
def mapAttributesFromScraping(linksPath = './links.txt'):
    
    print('Data manipulation and ETL in progress...')

    links = open(linksPath,"r")
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument('log-level=3')
    
    path_to_chromedriver = "chromedriver"

    driver = webdriver.Chrome(executable_path=path_to_chromedriver,options=chrome_options)
    
    books = []

    # go to website
    for link in links:
        
        driver.get(link)
        
        try: title = driver.find_elements_by_xpath("//div[@id='content_inner']/article/div/div[2]/h1")[0].text       
        except: title = ''
        
        try: price = float(driver.find_elements_by_xpath("//div[@id='content_inner']/article/div/div[2]/p")[0].text.split('£')[1])
        except: price = 0.0
        
        try: stock = int(driver.find_elements_by_xpath("//div[@id='content_inner']/article/div/div[2]/p")[1].text.split('In stock (')[1].split(' available)')[0])
        except: stock = np.nan
        
        try: rating = driver.find_elements_by_xpath("//div[@id='content_inner']/article/div/div[2]/p")[2].get_property('attributes')[0]['textContent'].split('star-rating ')[1]
        except: rating = np.nan
        
        try: category = driver.find_elements_by_class_name("breadcrumb")[0].text.split(' ')[2]
        except: category = ''
        
        try: description = driver.find_elements_by_xpath("//div[@id='content_inner']/article/p")[0].text
        except: description = ''
        
        if  (rating == "One"):   rating = 1
        elif(rating == "Two"):   rating = 2
        elif(rating == "Three"): rating = 3
        elif(rating == "Four"):  rating = 4
        elif(rating == "Five"):  rating = 5

        
        book = [title, category, description, price, rating, stock]

        if book:
            books.append(book)
            
    driver.close()
    return books



def createDatabase(dbName = 'cayenaDB', user = 'postgres', pwd = 'postgres'):
    try:
        #establishing the connection
        conn = psycopg2.connect(
           database="postgres", user=user, password=pwd, host='127.0.0.1', port= '5432'
        )
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        #Preparing query to create a database
        sql = 'CREATE database {};'.format(dbName)

        #Creating a database
        cursor.execute(sql)
        print('Database {} was created...'.format(dbName))
    except psycopg2.Error as e:
        print('Database {} already exists!!'.format(dbName))
        
def insertData(dbName = 'cayenaDB', user = 'postgres', pwd = 'postgres'):
        
    books = mapAttributesFromScraping("./links.txt")

    booksDF = pd.DataFrame(data=books, columns=["BookTitle", "Category", "Description", "Price", "Rating", "Availability"])
    
    columns = booksDF.columns.tolist()
    columns = [each_string.lower() for each_string in columns]

    sqlCreate =  """DROP TABLE IF EXISTS books;
                    CREATE TABLE books (
                     {}       VARCHAR (256),
                     {}       VARCHAR (256),
                     {}       VARCHAR,
                     {}       NUMERIC, 
                     {}       INTEGER, 
                     {}       INTEGER                   
                    );""".format(columns[0], columns[1], columns[2], columns[3], columns[4], columns[5])

    try:
        #establishing the connection
        conn = psycopg2.connect(
           database=str.lower(dbName), user=user, password=pwd, host='127.0.0.1', port= '5432'
        )
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        #Querying SQL to create table
        cursor.execute(sqlCreate)
        
        #Querying SQL to insert data from books
        insertedBooks = 0
        for i in booksDF.index:
            sqlInsert = """INSERT INTO books VALUES('{}','{}','{}',{},{},{})""".format(booksDF.loc[i,'BookTitle'].replace("'", "''"), 
                                                                                  booksDF.loc[i,'Category'].replace("'", "''"), 
                                                                                  booksDF.loc[i,'Description'].replace("'", "''"), 
                                                                                  booksDF.loc[i,'Price'], 
                                                                                  booksDF.loc[i,'Rating'],
                                                                                  booksDF.loc[i,'Availability'])
                        
            try:
                cursor = conn.cursor()

                cursor.execute(sqlInsert)
                insertedBooks+=1
                
            except psycopg2.Error as e:
                print(e)
                
        print("{} Books inserted".format(insertedBooks))
              
    except psycopg2.Error as e:
            print(e)
    
    
    
#################################
#################################
#################################
if __name__ == '__main__':
  
    createDatabase(dbName) ### function to create a database into PostgreSQL -- default dbName = cayenaDB
    insertData(dbName) ### functions to process scrapped data source and insert into a PostgreSQL table named of """books"""
