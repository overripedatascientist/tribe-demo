import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv(".env")

response = requests.post(
    url="https://api.langflow.astra.datastax.com/lf/ac53383d-4ff8-409f-8aac-f9ce96e24391/api/v1/run/d3a9f490-03e9-42b7-9a96-c184c0445231",
    headers={
        "Authorization": f"Bearer {os.getenv('ASTRA_DB_VECTOR_TOKEN')}",
        "Content-Type": "application/json"
    }
)

pprint(response.content)