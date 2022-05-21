## Bookstore Data Platform - Documentation 

### Description
This project provides a command-line tool to support data analysis based on SQL functions over scrapped data from a web source. Besides using the Airflow structure, the tool executes background routines to update the data between defined intervals, such as daily or hourly. The tool was based on Python programming language, storing the scrapped into an environment PostgreSQL to be executed SQL statements.

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
To execute this program, execute the statement in the CMD/Terminal: `python main.py`:
Command-List:

 - **0** -> Exit of program
 - **1** -> Execute the query to retrieve the average price by rating the book
 - **2** -> Execute the query retrieving the log records with a date and amount of books with two or fewer copies
 - **3** -> A querying App with receive any over books table with attributes "BookTitle", "Category", "Description", "Price", "Rating" and "Availability". Any SQL statement is available and returns the query result.

### Pipeline to update data using Airflow 
I'm using Apache Airflow to schedule a DAG with four tasks scrapping, transforming, and updating data into the PostgreSQL database. The steps of this orchestration are:

![Pipeline with Airflow](https://github.com/lsrusp/cayenaTest/blob/main/pipeline.jpg)

 - **Scrapping**:  scripts related to extracting data from web source to local platform
 - **CheckDatabase**: scripts based on SQL statements to check database schema and consistency model
 - **TransformData**: scripts to read and process web source to be inserted into PostgreSQL, using python and SQL functions
 - **GetCopiesBooks**: SQL scripts to update a log table related to the number of copies into the bookstore platform.

#### Author
Lucas Santiago Rodrigues 
- Contato: 17 992487365 / [lucas1613@gmail.com](lucas1613@gmail.com)
