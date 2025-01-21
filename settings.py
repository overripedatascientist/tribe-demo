import os.path

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

LANGFLOW_DIR = os.path.join(BASE_DIR, "langflow_jsons")
CONF_DIR = os.path.join(BASE_DIR, "conf")

LANGFLOW_JSON_FILE = os.path.join(LANGFLOW_DIR, "TRIBE for Climate Convos (4).json")
CONF_FILE = os.path.join(CONF_DIR, "config.json")

ASTRADB_BATCH_SIZE: int = 50
ASTRADB_RESULT_SIZE: int = 25
ASTRADB_SEARCH_TYPE: str = "Custom Search"  # "Custom Search" or "Similarity" or "Similarity with score threshold"
ASTRADB_SEARCH_SCORE_THRESHOLD: float = 0.3
ASTRADB_TIMEOUT_MS: int = 10000

TRIBES = {
    "All tribes": "",
    "Activists": 0,
    "Techno-Evangelists": 1,
    "Sustainability Shortcutters": 2,
    "Climate Cynics": 3,
    "Populist Skeptics": 4,
    "Eco-Conscious Trendsetters": 5,
    "Disaster Doomscrollers": 6,
    "Politically-Charged Debators": 7
}

AGE_GROUPS = {
    "All Ages": "",
    "Under 19s": "<=18",
    "19-29": "19_29",
    "30-39": "30_39",
    "Over 39": "40+"
}

COUNTRIES = {
    "Global": "",
    "United Kingdom": "GB",
    "United States": "US",
    "China": "CN",
    "India": "IN",
    "Germany": "DE"
}

PLATFORMS = {
  "All": "",
  "TikTok": "TikTok",
  "Facebook": "Facebook",
  "YouTube": "YouTube",
  "X": "Twitter"
}

# LANGFLOW_TWEAKS = {
#     "AstraDB-wNHGZ": {
#         "batch_size": ASTRADB_BATCH_SIZE,
#         "custom_search_timeout_ms": ASTRADB_TIMEOUT_MS,
#         "number_of_results": ASTRADB_RESULT_SIZE,
#         "search_score_threshold": ASTRADB_SEARCH_SCORE_THRESHOLD,
#         "search_type": ASTRADB_SEARCH_TYPE
#   }
# }

LANGFLOW_TWEAKS = {
  "ChatInput-nM66I": {},
  "AstraDB-wNHGZ": {
  "api_endpoint": "https://4423b0ba-2e75-4dcf-b2ad-d4b7e13218ca-us-east1.apps.astra.datastax.com",
    "batch_size": 50,
    "bulk_delete_concurrency": None,
    "bulk_insert_batch_concurrency": None,
    "bulk_insert_overwrite_concurrency": None,
    "collection_indexing_policy": "",
    "collection_name": "climate_change",
    "custom_search_timeout_ms": ASTRADB_TIMEOUT_MS,
    "metadata_indexing_exclude": "",
    "metadata_indexing_include": "",
    "metric": "cosine",
    "namespace": "",
    "number_of_results": ASTRADB_RESULT_SIZE,
    "pre_delete_collection": False,
    "search_filter": "",
    "search_input": "",
    "search_score_threshold": ASTRADB_SEARCH_SCORE_THRESHOLD,
    "search_type": ASTRADB_SEARCH_TYPE,
    "setup_mode": "Off",
    "token": "ASTRA_DB_APPLICATION_TOKEN"
  },
  "ParseData-obnZv": {},
  "ChatOutput-plpD3": {},
  "AnthropicModel-FvFsG": {},
  "TextOutput-xfM5I": {},
  "ParseJSONData-eeEA0": {},
  "TextInput-n0QkP": {},
  "MetaDataFilterConstructor-vAJyP": {},
  "TextInput-P1BmY": {},
  "TextInput-4wKnt": {},
  "TextInput-wg8O0": {},
  "TextInput-aYfSJ": {},
  "TextInput-WCBMY": {},
  "TextInput-Uk4ri": {},
  "Memory-MeAfJ": {},
  "Prompt-oU1Ym": {},
  "TextInput-JZobh": {},
  "TextInput-UhThw": {},
  "OpenAIModel-wA6hw": {},
  "CombineText-88DLO": {},
  "OpenAIModel-k9HRn": {},
  "Prompt-fJCSt": {},
  "OpenAIEmbeddings-tspex": {}
}

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
# LANGFLOW_TWEAKS = {
#   "ChatInput-nM66I": {
#     "files": "",
#     "background_color": "",
#     "chat_icon": "",
#     "input_value": "feelings about global warming",
#     "sender": "User",
#     "sender_name": "User",
#     "session_id": "",
#     "should_store_message": True,
#     "text_color": ""
#   },
#   "AstraDB-wNHGZ": {
#     "api_endpoint": "https://4423b0ba-2e75-4dcf-b2ad-d4b7e13218ca-us-east1.apps.astra.datastax.com",
#     "batch_size": 50,
#     "bulk_delete_concurrency": None,
#     "bulk_insert_batch_concurrency": None,
#     "bulk_insert_overwrite_concurrency": None,
#     "collection_indexing_policy": "",
#     "collection_name": "climate_change",
#     "custom_search_timeout_ms": ASTRADB_TIMEOUT_MS,
#     "metadata_indexing_exclude": "",
#     "metadata_indexing_include": "",
#     "metric": "cosine",
#     "namespace": "",
#     "number_of_results": ASTRADB_RESULT_SIZE,
#     "pre_delete_collection": False,
#     "search_filter": "",
#     "search_input": "",
#     "search_score_threshold": ASTRADB_SEARCH_SCORE_THRESHOLD,
#     "search_type": ASTRADB_SEARCH_TYPE,
#     "setup_mode": "Off",
#     "token": "ASTRA_DB_APPLICATION_TOKEN"
#   },
#   "ParseData-obnZv": {
#     "sep": "\n",
#     "template": "By a {user_age_group_years} {user_gender} user in {user_country} on {platform}:\\n\n{text}\\n\n(stats: {likes_count} likes, {shares_count} shares, created at: {create_time})\\n\n------------------------------------------\\n"
#   },
#   "ChatOutput-plpD3": {
#     "background_color": "",
#     "chat_icon": "",
#     "data_template": "{text}",
#     "input_value": "",
#     "sender": "Machine",
#     "sender_name": "AI",
#     "session_id": "",
#     "should_store_message": True,
#     "text_color": ""
#   },
#   "AnthropicModel-FvFsG": {
#     "anthropic_api_key": "ANTHROPIC_API_KEY",
#     "anthropic_api_url": "",
#     "input_value": "",
#     "max_tokens": 4096,
#     "model": "claude-3-5-sonnet-latest",
#     "prefill": "",
#     "stream": False,
#     "system_message": "",
#     "temperature": 0.7
#   },
#   "TextOutput-xfM5I": {
#     "input_value": ""
#   },
#   "ParseJSONData-eeEA0": {
#     "query": ".[] | {   text,   likes_count: (.likes // \"0\"),   comments_count: (.comments // \"0\"),   shares_count: (.shares // \"0\"),   create_time: (.create_time // \"Not specified\"),   user_age_group_years: (.age // \"Not specified\"),   user_gender: (.gender // \"Not Specified\"),   user_country: (.country // \"Unknown\"),   user_follower_count: (.follower_count // \"Not specified\"),   platform: .platform }"
#   },
#   "TextInput-n0QkP": {
#     "input_value": "0"
#   },
#   "MetaDataFilterConstructor-vAJyP": {
#     "age": "",
#     "country": "",
#     "datetime_from": "",
#     "datetime_to": "",
#     "followers": "",
#     "gender": "",
#     "likes_minimum": "",
#     "platform": "",
#     "tribe": ""
#   },
#   "TextInput-P1BmY": {
#     "input_value": ""
#   },
#   "TextInput-4wKnt": {
#     "input_value": ""
#   },
#   "TextInput-wg8O0": {
#     "input_value": "GB"
#   },
#   "TextInput-aYfSJ": {
#     "input_value": ""
#   },
#   "TextInput-WCBMY": {
#     "input_value": ""
#   },
#   "TextInput-Uk4ri": {
#     "input_value": ""
#   },
#   "Memory-MeAfJ": {
#     "n_messages": 20,
#     "order": "Descending",
#     "sender": "Machine and User",
#     "sender_name": "",
#     "session_id": "",
#     "template": "{sender_name}: {text}"
#   },
#   "Prompt-oU1Ym": {
#     "template": "Chat history:\n\n{history}\n\n------------------------------\n\nBelow are a number of real, relevant results from 4 social media platforms (TikTok, Facebook, YouTube, and Twitter).\n\nThey are in a variety of languages so when you come across them please translate them into English and pass along your findings.\n\nHere are the snippets:\n\n{context}\n\n------------------------------\n\nUsing the social media posts and comments provided above do your best to answer the below question. (And don't forget in your analysis to also include some direct verbatim quotes from the text snippets from the text snippets where appropriate!)!)\n\nQuestion: {question}\n\nAnswer:\n",
#     "history": "",
#     "context": "",
#     "question": ""
#   },
#   "TextInput-JZobh": {
#     "input_value": ""
#   },
#   "TextInput-UhThw": {
#     "input_value": ""
#   },
#   "OpenAIModel-wA6hw": {
#     "api_key": "OPENAI_API_KEY",
#     "input_value": "",
#     "json_mode": False,
#     "max_tokens": None,
#     "model_kwargs": {},
#     "model_name": "gpt-4o",
#     "openai_api_base": "",
#     "output_schema": {},
#     "seed": 1,
#     "stream": False,
#     "system_message": "",
#     "temperature": 0.7
#   },
#   "CombineText-88DLO": {
#     "delimiter": " \\n\\n-----Chat-GPT----- \\n\\n",
#     "text1": "",
#     "text2": ""
#   },
#   "OpenAIModel-k9HRn": {
#     "api_key": "OPENAI_API_KEY",
#     "input_value": "",
#     "json_mode": False,
#     "max_tokens": None,
#     "model_kwargs": {},
#     "model_name": "gpt-4o-mini",
#     "openai_api_base": "",
#     "output_schema": {},
#     "seed": 1,
#     "stream": False,
#     "system_message": "",
#     "temperature": 0.6
#   },
#   "Prompt-fJCSt": {
#     "template": "Please seamlessly combine these two summaries into a single, coherent, clear and comprehensive written report.\n\n(For background context, these were produced by collecting and analysing social media conversations (posts and comments) across TikTok, Facebook, YouTube and Twitter/X around the topic of \"{topic}\" as it relates to climate change).\n\nHere are the two analyses that need to be merged into a single write-up:\n\n```\n{context}\n```\n",
#     "context": "",
#     "topic": ""
#   },
#   "OpenAIEmbeddings-tspex": {
#     "chunk_size": 1000,
#     "client": "",
#     "default_headers": {},
#     "default_query": {},
#     "deployment": "",
#     "dimensions": None,
#     "embedding_ctx_length": 3072,
#     "max_retries": 3,
#     "model": "text-embedding-3-large",
#     "model_kwargs": {},
#     "openai_api_base": "",
#     "openai_api_key": "OPENAI_API_KEY",
#     "openai_api_type": "",
#     "openai_api_version": "",
#     "openai_organization": "OPENAI_ORGANISATION_ID",
#     "openai_proxy": "",
#     "request_timeout": None,
#     "show_progress_bar": False,
#     "skip_empty": False,
#     "tiktoken_enable": True,
#     "tiktoken_model_name": ""
#   }
# }
