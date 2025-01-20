import os
from astrapy import DataAPIClient
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langflow.schema.data import Data
from langchain_core.documents.base import Document

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