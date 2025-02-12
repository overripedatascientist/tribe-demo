from loguru import logger
import json

from langflow.base.vectorstores.model import LCVectorStoreComponent, check_cached_vector_store
from langflow.helpers import docs_to_data
from langflow.inputs import FloatInput, MessageTextInput
from langflow.io import (
    BoolInput,
    DataInput,
    DropdownInput,
    HandleInput,
    IntInput,
    MultilineInput,
    SecretStrInput,
    StrInput,
)

from astrapy import DataAPIClient

from langflow.schema.data import Data
from langchain_core.documents.base import Document

from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from logging import WARNING


class AstraVectorStoreComponent(LCVectorStoreComponent):
    display_name: str = "Astra DB"
    description: str = "Implementation of Vector Store using Astra DB with search capabilities"
    documentation: str = "https://python.langchain.com/docs/integrations/vectorstores/astradb"
    name = "AstraDB"
    icon: str = "AstraDB"

    inputs = [
        StrInput(
            name="collection_name",
            display_name="Collection Name",
            info="The name of the collection within Astra DB where the vectors will be stored.",
            required=True,
        ),
        SecretStrInput(
            name="token",
            display_name="Astra DB Application Token",
            info="Authentication token for accessing Astra DB.",
            value="ASTRA_DB_APPLICATION_TOKEN",
            required=True,
        ),
        SecretStrInput(
            name="api_endpoint",
            display_name="API Endpoint",
            info="API endpoint URL for the Astra DB service.",
            value="ASTRA_DB_API_ENDPOINT",
            required=True,
        ),
        MultilineInput(
            name="search_input",
            display_name="Search Input",
        ),
        DataInput(
            name="ingest_data",
            display_name="Ingest Data",
            is_list=True,
        ),
        StrInput(
            name="namespace",
            display_name="Namespace",
            info="Optional namespace within Astra DB to use for the collection.",
            advanced=True,
        ),
        DropdownInput(
            name="metric",
            display_name="Metric",
            info="Optional distance metric for vector comparisons in the vector store.",
            options=["cosine", "dot_product", "euclidean"],
            advanced=True,
        ),
        IntInput(
            name="custom_search_timeout_ms",
            display_name="Custom Search Timeout (Milliseconds)",
            info="Maximum time to wait for custom search results in milliseconds",
            advanced=True,
            value=1000
        ),
        IntInput(
            name="batch_size",
            display_name="Batch Size",
            info="Optional number of data to process in a single batch.",
            advanced=True,
        ),
        IntInput(
            name="bulk_insert_batch_concurrency",
            display_name="Bulk Insert Batch Concurrency",
            info="Optional concurrency level for bulk insert operations.",
            advanced=True,
        ),
        IntInput(
            name="bulk_insert_overwrite_concurrency",
            display_name="Bulk Insert Overwrite Concurrency",
            info="Optional concurrency level for bulk insert operations that overwrite existing data.",
            advanced=True,
        ),
        IntInput(
            name="bulk_delete_concurrency",
            display_name="Bulk Delete Concurrency",
            info="Optional concurrency level for bulk delete operations.",
            advanced=True,
        ),
        DropdownInput(
            name="setup_mode",
            display_name="Setup Mode",
            info="Configuration mode for setting up the vector store, with options like 'Sync', 'Async', or 'Off'.",
            options=["Sync", "Async", "Off"],
            advanced=True,
            value="Sync",
        ),
        BoolInput(
            name="pre_delete_collection",
            display_name="Pre Delete Collection",
            info="Boolean flag to determine whether to delete the collection before creating a new one.",
            advanced=True,
        ),
        StrInput(
            name="metadata_indexing_include",
            display_name="Metadata Indexing Include",
            info="Optional list of metadata fields to include in the indexing.",
            advanced=True,
        ),
        HandleInput(
            name="embedding",
            display_name="Embedding or Astra Vectorize",
            input_types=["Embeddings", "dict"],
            info="Allows either an embedding model or an Astra Vectorize configuration.",  # TODO: This should be optional, but need to refactor langchain-astradb first.
        ),
        StrInput(
            name="metadata_indexing_exclude",
            display_name="Metadata Indexing Exclude",
            info="Optional list of metadata fields to exclude from the indexing.",
            advanced=True,
        ),
        StrInput(
            name="collection_indexing_policy",
            display_name="Collection Indexing Policy",
            info="Optional dictionary defining the indexing policy for the collection.",
            advanced=True,
        ),
        IntInput(
            name="number_of_results",
            display_name="Number of Results",
            info="Number of results to return.",
            advanced=True,
            value=4,
        ),
        DropdownInput(
            name="search_type",
            display_name="Search Type",
            info="Search type to use",
            options=["Similarity", "Similarity with score threshold", "MMR (Max Marginal Relevance)", "Custom Search"],
            value="Similarity",
            advanced=True,
        ),
        FloatInput(
            name="search_score_threshold",
            display_name="Search Score Threshold",
            info="Minimum similarity score threshold for search results. (when using 'Similarity with score threshold')",
            value=0,
            advanced=True,
        ),
        MessageTextInput(
            name="search_filter",
            display_name="Search Metadata Filter",
            info="Optional JSON dictionary of filters to apply to the search query.",
        ),

    ]

    @check_cached_vector_store
    def build_vector_store(self):
        try:
            from langchain_astradb import AstraDBVectorStore
            from langchain_astradb.utils.astradb import SetupMode
        except ImportError:
            raise ImportError(
                "Could not import langchain Astra DB integration package. "
                "Please install it with `pip install langchain-astradb`."
            )

        try:
            if not self.setup_mode:
                self.setup_mode = self._inputs["setup_mode"].options[0]

            setup_mode_value = SetupMode[self.setup_mode.upper()]
        except KeyError:
            raise ValueError(f"Invalid setup mode: {self.setup_mode}")

        if not isinstance(self.embedding, dict):
            embedding_dict = {"embedding": self.embedding}
        else:
            from astrapy.info import CollectionVectorServiceOptions

            dict_options = self.embedding.get("collection_vector_service_options", {})
            dict_options["authentication"] = {
                k: v for k, v in dict_options.get("authentication", {}).items() if k and v
            }
            dict_options["parameters"] = {k: v for k, v in dict_options.get("parameters", {}).items() if k and v}
            embedding_dict = {
                "collection_vector_service_options": CollectionVectorServiceOptions.from_dict(dict_options)
            }
            collection_embedding_api_key = self.embedding.get("collection_embedding_api_key")
            if collection_embedding_api_key:
                embedding_dict["collection_embedding_api_key"] = collection_embedding_api_key

        vector_store_kwargs = {
            **embedding_dict,
            "collection_name": self.collection_name,
            "token": self.token,
            "api_endpoint": self.api_endpoint,
            "namespace": self.namespace or None,
            "metric": self.metric or None,
            "batch_size": self.batch_size or None,
            "bulk_insert_batch_concurrency": self.bulk_insert_batch_concurrency or None,
            "bulk_insert_overwrite_concurrency": self.bulk_insert_overwrite_concurrency or None,
            "bulk_delete_concurrency": self.bulk_delete_concurrency or None,
            "setup_mode": setup_mode_value,
            "pre_delete_collection": self.pre_delete_collection or False,
        }

        if self.metadata_indexing_include:
            vector_store_kwargs["metadata_indexing_include"] = self.metadata_indexing_include
        elif self.metadata_indexing_exclude:
            vector_store_kwargs["metadata_indexing_exclude"] = self.metadata_indexing_exclude
        elif self.collection_indexing_policy:
            vector_store_kwargs["collection_indexing_policy"] = self.collection_indexing_policy

        try:
            vector_store = AstraDBVectorStore(**vector_store_kwargs)
        except Exception as e:
            raise ValueError(f"Error initializing AstraDBVectorStore: {str(e)}") from e

        self._add_documents_to_vector_store(vector_store)
        return vector_store

    def _add_documents_to_vector_store(self, vector_store):
        documents = []
        for _input in self.ingest_data or []:
            if isinstance(_input, Data):
                documents.append(_input.to_lc_document())
            else:
                raise ValueError("Vector Store Inputs must be Data objects.")

        if documents:
            logger.debug(f"Adding {len(documents)} documents to the Vector Store.")
            try:
                vector_store.add_documents(documents)
            except Exception as e:
                raise ValueError(f"Error adding documents to AstraDBVectorStore: {str(e)}") from e
        else:
            logger.debug("No documents to add to the Vector Store.")

    def _map_search_type(self):
        if self.search_type == "Similarity with score threshold":
            return "similarity_score_threshold"
        elif self.search_type == "MMR (Max Marginal Relevance)":
            return "mmr"
        elif self.search_type =="Custom Search":
            return "custom_search"
        else:
            return "similarity"

    def _build_search_args(self):
        args = {
            "k": self.number_of_results,
            "score_threshold": self.search_score_threshold,
        }

        filter_dict = None
        if self.search_filter:
            try:
                filter_list = json.loads(self.search_filter)
                logger.info(f"Filter list supplied: {filter_list}")

                if isinstance(filter_list, list):
                    filter_conditions = []
                    operator_map = {
                        "eq": None,  # For equality, assign value directly
                        "neq": "$ne",
                        "gt": "$gt",
                        "gte": "$gte",
                        "lt": "$lt",
                        "lte": "$lte",
                        # Add more operators as needed
                    }
                    for item in filter_list:
                        if isinstance(item, dict):
                            field = item.get('field')
                            operator = item.get('operator')
                            value = item.get('value')
                            if field and operator and value is not None:
                                mapped_operator = operator_map.get(operator)
                                if mapped_operator:
                                    # For operators like 'gte', 'lte', etc.
                                    condition = {field: {mapped_operator: value}}
                                else:
                                    # For equality ('eq')
                                    condition = {field: value}
                                filter_conditions.append(condition)
                    if filter_conditions:
                        if len(filter_conditions) == 1:
                            filter_dict = filter_conditions[0]
                        else:
                            filter_dict = {"$and": filter_conditions}
                else:
                    logger.warning("Invalid search filter format. Expected a list of conditions.")
            except json.JSONDecodeError:
                logger.warning("Invalid JSON format for search filter.")
            except Exception as e:
                logger.error(f"Error processing search filter: {str(e)}")

        if filter_dict:
            args["filter"] = filter_dict

        return args

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        before_sleep=before_sleep_log(logger, WARNING),
        retry_error_callback=lambda x: logger.warning(f"Attempt {x.attempt_number} failed.")
    )
    def search_documents(self) -> list[Data]:
        vector_store = self.build_vector_store()

        logger.debug(f"Search input: {self.search_input}")
        logger.debug(f"Search type: {self.search_type}")
        logger.debug(f"Number of results: {self.number_of_results}")

        if self.search_input and isinstance(self.search_input, str) and self.search_input.strip():
            try:
                search_type = self._map_search_type()
                search_args = self._build_search_args()
                filter_dict = search_args.get("filter")
                k = search_args.get("k", self.number_of_results)
                score_threshold = search_args.get("score_threshold")

                if search_type == "similarity_score_threshold":
                    docs_and_scores = vector_store.similarity_search_with_relevance_scores(
                        query=self.search_input,
                        k=k,
                        filter=filter_dict,
                        score_threshold=score_threshold
                    )
                    # Extract documents
                    docs = [doc for doc, score in docs_and_scores]
                elif search_type == "similarity":
                    docs_and_scores = vector_store.similarity_search_with_relevance_scores(
                        query=self.search_input,
                        k=k,
                        filter=filter_dict
                    )
                    # Extract documents
                    docs = [doc for doc, score in docs_and_scores]
                elif search_type == "mmr":
                    docs = vector_store.max_marginal_relevance_search(
                        query=self.search_input,
                        k=k,
                        filter=filter_dict
                    )
                    # No need to extract, already a list of Documents
                elif search_type == "custom_search":
                    if vector_store.embeddings is None:
                        raise ValueError(
                            "No embedding model found. Please ensure an embedding model is provided when initializing the vector store.")
                    embedding_model = vector_store.embeddings
                    query_vector = embedding_model.embed_query(self.search_input)

                    # Amend filter dict to prepend with metadata.
                    def prepend_metadata_to_fields(filter_dict):
                        if not isinstance(filter_dict, dict):
                            return filter_dict
                        result = {}
                        for key, value in filter_dict.items():
                            if key.startswith('$'):
                                # Handle operators ($and, $or, etc.)
                                result[key] = [
                                    prepend_metadata_to_fields(item)
                                    for item in value
                                ] if isinstance(value, list) else prepend_metadata_to_fields(value)
                            else:
                                # Prepend metadata. to field names
                                new_key = f"metadata.{key}"
                                result[new_key] = prepend_metadata_to_fields(value)
                        return result

                    new_filter = prepend_metadata_to_fields(filter_dict)

                    results = self.collection.find(
                        new_filter,
                        sort={"$vector": query_vector},
                        limit=k,
                        include_similarity=True,
                        projection={"*": True},
                        max_time_ms=self.custom_search_timeout_ms
                    )
                    docs = [Document(page_content=doc['$vectorize'], metadata=doc['metadata']) for doc in results
                            if doc['$similarity'] >= score_threshold]
                else:
                    raise ValueError(f"Unknown search_type: {search_type}")

            except Exception as e:
                # filter_dict_str = str(filter_dict) if filter_dict else "No filter dictionary supplied"
                raise ValueError(f"Error performing search in AstraDBVectorStore: {str(e)})") from e

            logger.debug(f"Retrieved documents: {len(docs)}")

            data = docs_to_data(docs)
            logger.debug(f"Converted documents to data: {len(data)}")
            self.status = data
            return data
        else:
            logger.debug("No search input provided. Skipping search.")
            return []

    @property
    def collection(self):
        # Initialize the Astra DB client and get a "Database" object
        client = DataAPIClient(self.token)
        database = client.get_database(self.api_endpoint)
        logger.info(f"* Database: {database.info().name}\n")

        # TODO: Bug fix - getting collection not found error
        collection = database.get_collection(self.collection_name)
        logger.info(f"* Collection: {collection.info().name}\n")

        return collection

    def get_retriever_kwargs(self):
        search_args = self._build_search_args()
        return {
            "search_type": self._map_search_type(),
            "search_kwargs": search_args,
        }


