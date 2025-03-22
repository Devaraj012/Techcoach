import os
import requests
import mariadb,pandas as pd
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\devar\Documents\Code\Techcoach\.env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else None,  # Prevent NoneType error
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

cookie_ticket = os.getenv("IBT_COOKIE_TICKET")

conn = mariadb.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)

queries = {
    1: """
        SELECT 
        us.displayname as username, 
        d.creation_date as date, 
        COUNT(DISTINCT d.decision_id) AS decision_count
        FROM 
            techcoach_users AS us
        JOIN 
            techcoach_decision AS d
        ON 
            us.user_id = d.user_id
        GROUP BY 
            us.displayname, d.creation_date
        HAVING
            d.creation_date IS NOT NULL;
    """,
    2:"""
    SELECT
	u.displayname as username,
    c.created_at as date,
    count(c.comment) as total_comments

    FROM 
        techcoach_users as u

    JOIN 
        techcoach_decision as d ON u.user_id=d.user_id
    
    JOIN techcoach_conversations as c on d.decision_id=c.decisionId 
    
    group by u.displayname
    """
}

def fetch_and_upload_data(query_number):
    if query_number in queries:
        query = queries[query_number]
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%m-%d-%Y')
        output_file = f"Query_{query_number}_Data.csv"
        df.to_csv(output_file, index=False)
        print(f"Query {query_number} executed successfully. Data saved to {output_file}")
        
        upload_data(output_file, query_number)
    else:
        print("Invalid query number. Please provide a valid query number.")

def upload_data(file_path, query_number):
    url = "https://greenestep.giftai.co.in/api/v1/csv/upload?d_type=none&"
    
    payloads = {
        1: {
            'collection_id': '106',
            'type': 'Replace',
            'fieldMapped': 'Object'
        },
        2:{
            'collection_id': '107',
            'type': 'Replace',
            'fieldMapped': 'Object'
        }
    }
    
    headers = {
        'Cookie': 'ticket=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRldmFyYWpAaWJhY3VzdGVjaGxhYnMuaW4iLCJpZCI6NCwidHlwZSI6IkFETUlOIiwiaWF0IjoxNzQyNTM4Mzg0LCJleHAiOjE3NDI1ODE1ODR9.M2FXM5VskT1T7VHDouULwiVfOTnlsj5cpcyu0odrvKc'
    }
    
    payload = payloads.get(query_number, {})
    
    with open(file_path, 'rb') as f:
        files = {'csvFile': (file_path, f, 'text/csv')}
        response = requests.post(url, headers=headers, data=payload, files=files)
    
    print(response.text)

for query_num in queries.keys():
    fetch_and_upload_data(query_num)

cursor.close()
conn.close()