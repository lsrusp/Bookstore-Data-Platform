
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
To execute this program, execute the statement in the python environment: **python main.py**:
Command-List:

 - **0** -> Exit of program
 - **1** -> Execute the query to retrieve the average price by rating the book
 - **2** -> Execute the query retrieving the log records with a date and amount of books with 2 or less copies
 - **3** -> A querying App with receive any over books table with attributes "BookTitle", "Category", "Description", "Price", "Rating" and "Availability". Any SQL statement is available and returns the query result.

### Pipeline to update data using Airflow 
