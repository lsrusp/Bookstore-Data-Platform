## Bookstore Data Platform - Documentation 

### Description
This project provides a command-line tool to support data analysis based on SQL functions over scrapped data from a web source. Besides, the tool executes background routines to update the data between defined intervals, such as daily or even hourly, using the Airflow structure. The tool was based on Python programming language, storing the scrapped into an environment PostgreSQL to be executed SQL statements.

### Requirements
 - Python Environment 
 - Selenium, PandaSQL, Prettytable libraries (install with 'pip' command)
 - Airflow library (install with 'pip' command)
 - PostgreSQL (local environment)
 - Chromedriver.exe (executable file in this repository - https://chromedriver.chromium.org/downloads)

### Repository Files - Descriptions
 - **main.py**: executable script of this platform to be retrieve information from database using SQL statements.
 - **scrappingBooks.py**: script with functions to extract data from web source https://books.toscrape.com/.
 - **processingBooks.py**: script with ETL functions to transform and save data into database using SQL statements.

### Command-Line Functions

### Pipeline to update data using Airflow 
