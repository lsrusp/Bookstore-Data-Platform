"""/* ######################################################### */
/* @author                                                   */
/* @Lucas Santiago Rodrigues -- lucas1613@gmail.com          */
/* ######################################################### */"""

import pandas as pd
import numpy as np
from pandasql import sqldf ## make possible to run SQL statements over pandas dataframe equally a PostgreSQL or equivalent environment

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    
import psycopg2

from prettytable import PrettyTable
import textwrap


# ## What is the average price of books by rating (in stars)?
def avgPrinceByRating(dbName = 'cayenaDB', user = 'postgres', pwd = 'postgres'):
    try:
        conn = psycopg2.connect(
           database=str.lower(dbName), user=user, password=pwd, host='127.0.0.1', port= '5432'
        )
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        #Querying SQL to create table
        cursor.execute("""SELECT Rating AS "Rating (Stars)", ROUND(AVG(price),2) as "AVG Price (£)" 
                              FROM books
                              GROUP BY Rating;""")

        data = cursor.fetchall()

        ##Create a dataframe
        if (data):
            cols = []
            for elt in cursor.description:
                cols.append(elt[0])

        result = pd.DataFrame(data = data, columns = cols)

        table = PrettyTable()

        table.field_names = cols
        for row in range(len(result)):
            table.add_row([result.iloc[row,0],result.iloc[row,1]])
            
    except psycopg2.Error as e:
        print(e)
                    
    return table


# ## How many books have 2 or less copies on a specific day?
def amountCopiesBooks(dbName = 'cayenaDB', user = 'postgres', pwd = 'postgres'):
    
    try:
        conn = psycopg2.connect(
           database=str.lower(dbName), user=user, password=pwd, host='127.0.0.1', port= '5432'
        )
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        try:
            cursor.execute("""CREATE TABLE logCopiesQuery (currentDate timestamp, copies integer);""")
            
        except psycopg2.Error as e:
            pass

        #Querying SQL to create table
        cursor.execute("""INSERT INTO logCopiesQuery SELECT  CURRENT_TIMESTAMP, COUNT(*)
                            FROM books 
                            WHERE Availability <=2 
                            """)
        
        cursor.execute('SELECT currentDate AS "Date Log", copies AS "Books have 2 or less copies" FROM logCopiesQuery')

        data = cursor.fetchall()

        ##Create a dataframe
        if (data):
            cols = []
            for elt in cursor.description:
                cols.append(elt[0])

        result = pd.DataFrame(data = data, columns = cols)

        table = PrettyTable()

        table.field_names = cols
        for row in range(len(result)):
            table.add_row([result.iloc[row,0],result.iloc[row,1]])
        
    except psycopg2.Error as e:
        print(e)

    return table

def queryingApp(sqlQuery, dbName = 'cayenaDB', user = 'postgres', pwd = 'postgres', verbose=True):
    
    try:
        conn = psycopg2.connect(
           database=str.lower(dbName), user=user, password=pwd, host='127.0.0.1', port= '5432'
        )
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        cursor.execute(sqlQuery)

        data = cursor.fetchall()
        

        ##Create a dataframe
        if (len(data)>0):
            cols = []
            for elt in cursor.description:
                cols.append(elt[0])

            result = pd.DataFrame(data = data, columns = cols)

            table = PrettyTable()

            table.field_names = cols
            for row in range(len(result)):
                row_insert = []

                for col in range(len(result.columns)):
                    if(type(result.iloc[row,col])== str and len(result.iloc[row,col]) > 70): result.iloc[row,col] = textwrap.fill(result.iloc[row,col], 70)
                    row_insert += [result.iloc[row,col]]

                table.add_row(row_insert)
            if(verbose): print(table)
        else:
            if(verbose): print('\n[Querying App] Empty SQL result\n')

    except psycopg2.Error as e:
        print(e)
        

#################################
#################################
#################################
if __name__ == '__main__':
    value = np.inf
    
    while(value !=0):
        value = input("""\nWelcome to Bookstore Data Platform\n
Choose your command: \n 
    0- Exit the data plataform\n
    1- Query: What is the average price of books by rating (in stars)?\n
    2- Query: How many books have 2 or less copies on a specific day?\n
    3- Insert a SQL query over books table - Attrs: "BookTitle", "Category", "Description", "Price", "Rating" and "Availability"
    
Developed by: Lucas Santiago Rodrigues (lucas1613@gmail.com)

Command number: """)

        if(len(value) == 1):
            
            if(int(value) == 1):
                avgPrinceByRating()
                print('\n\n') 

            elif( int(value) == 2):
                amountCopiesBooks()
                print('\n\n') 

            elif(int(value) == 0):
                print('\nSee you later!\n')
                sys.exit(0)
        else:
            print()
            print(queryingApp(value))
            print()

