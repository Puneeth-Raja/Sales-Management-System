# import mysql.connector

# def get_connection ():
#     return mysql.connector.connect( 
#         host='localhost',
#         user='root',
#         password='Puneeth@16',
#         database= 'sales_intelligence_hub'
#     )
       
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("db_host"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        database=os.getenv("db_database")
    )
