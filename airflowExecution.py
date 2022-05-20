#!/usr/bin/env python
# coding: utf-8

# In[5]:


import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import functools

from datetime import datetime, timedelta  

import scrappingBooks
import processingBooks
import main

import warnings
warnings.filterwarnings("ignore")


# In[11]:


#DAG setup
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    # Example: Initiate at may/20/2022
    'start_date': datetime(2022, 5, 20),
    # In case of errors, try to run again just 1 time
    'retries': 1,
    # Try again after 30 seconds after the error
    'retry_delay': timedelta(seconds=30),
    # Run once every day at midnight
    'schedule_interval': '@daily'}

with DAG(dag_id='update_books', 
        default_args=default_args, 
        schedule_interval=None,
        tags=['books']
        ) as dag:
    
    
    #tasks to scrappe new data from web source
    t1 = PythonOperator(
        task_id='scrapping',
        python_callable= functools.partial(scrappingBooks.getLinksPages),
        dag=dag
    )
    
    #check database schema to insert new data
    t2 = PythonOperator(
        task_id='checkDatabase',
        python_callable= processingBooks.createDatabase,
        dag=dag
    )

    #transform and insert data into postgres table
    t3 = PythonOperator(
        task_id='transformUpdateData',
        python_callable= processingBooks.insertData,
        dag=dag
    )
    
    #get amount of books with 2 and less copies and save in log table
    t4 = PythonOperator(
        task_id='getCopiesBooks',
        python_callable= main.amountCopiesBooks,
        dag=dag
    )
    
    #dependências entre as tarefas
    t1 >> t2 >> t3 >> t4

