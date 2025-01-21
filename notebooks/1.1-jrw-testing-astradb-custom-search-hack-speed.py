import os
from astrapy import DataAPIClient
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langflow.schema.data import Data
from langchain_core.documents.base import Document
from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

load_dotenv(".env")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Generate vector embedding for the search query
search_query = "how do people feel about global warming?"
query_vector = embeddings.embed_query(search_query)

token = os.environ['ASTRA_DB_VECTOR_TOKEN']
endpoint = "https://4423b0ba-2e75-4dcf-b2ad-d4b7e13218ca-us-east1.apps.astra.datastax.com"
collection_name = "climate_change"
client = DataAPIClient(token)
database = client.get_database(endpoint)
collection = database.get_collection(collection_name)

filter_dict = {
    '$and':
        [
            {'metadata.likes': {'$gte': 100}},
            {'metadata.tribe': 0}
        ]
}

results = collection.find(
    filter_dict,
    sort={"$vector": query_vector},
    limit=25,
    include_similarity=True,
    projection={"*": True},
)
docs = list(results)

print(docs)

# Parse documents
document = Document(
    page_content=docs[0]['$vectorize'],
    metadata=docs[0]['metadata']
)
data = Data.from_document(document)

connection_options = {
    "driver.advanced.connection.pool.local.size": 16
}


def fetch_in_batches(collection, filter_dict, query_vector, total_size=1000, batch_size=100):
    results = []
    last_created_at = None
    last_id = None

    while len(results) < total_size:
        current_filter = filter_dict.copy() if filter_dict else {}
        if last_created_at and last_id:
            current_filter["$or"] = [
                {"created_at": {"$lt": last_created_at}},
                {"$and": [
                    {"created_at": {"$eq": last_created_at}},
                    {"_id": {"$lt": last_id}}
                ]}
            ]

        batch = collection.find(
            current_filter,
            sort=[("created_at", -1), ("_id", -1)],
            limit=batch_size,
            include_similarity=True,
            projection={"*": True},
        )

        batch_docs = list(batch)
        if not batch_docs:
            break

        results.extend(batch_docs)
        last_doc = batch_docs[-1]
        last_created_at = last_doc.get("created_at")
        last_id = last_doc.get("_id")

    return results[:total_size]


results = parallel_search(
    collection,
    filter_dict,
    query_vector,
    100,
    25
)
docs = list(results)