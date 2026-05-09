import mysql.connector

def get_connection ():
    return mysql.connector.connect( 
        host='localhost',
        user='root',
        password='Puneeth@16',
        database= 'sales_intelligence_hub'
    )
       
