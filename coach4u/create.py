import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

auth=os.getenv('TOKEN')

url = "https://greenestep.giftai.co.in/api/v1/csv"

headers = {
  'Cookie': 'ticket=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNoYXJlX2RldmFyYWpAdGVjaGNvYWNoNHUuY29tIiwiaWQiOjMsInR5cGUiOiJBRE1JTiIsImlhdCI6MTc0MTg0MjM0NiwiZXhwIjoxNzQxODg1NTQ2fQ.XaZpUndQnjGtx4G35G0L1Bmb7z_MXzxga5SanfkAo9c',
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {auth}'
}

Collections=[
  {
  "collection_description": "Techcoach_Dashboard",
  "collection_name": "Skills added by user",
  "collection_permission": "READ",
  "collection_type": "PUBLIC"
  }
]

for collection in Collections:
  payload = json.dumps(collection)
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)