from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatInput-5LGWh": {
    "files": "",
    "input_value": "You are an expert analyst of cultural trends and social dynamics, with a deep understanding of how cultural identity shapes behaviour and narratives.\n\nYour task is to synthesise the following social media content related to climate change and craft a concise narrative that captures the key cultural themes and attitudes.\n\nWe have scraped conversations from TikTok, Facebook, YouTube and Twitter related to the climate conversation and created a massive dataset of posts and comments.\n\nFor each of these posts we also enriched it with profile information of who was posting or commenting and added demographic attributes like age, gender and org (company or brand) or non_org (human being).\n\nBased on the social media data provided, tell me about the 10 most prevalent climate change narratives across Twitter, Facebook, TikTok and YouTube? For each narrative, provide a brief description and note any platform-specific trends.",
    "sender": "User",
    "sender_name": "User",
    "session_id": "",
    "should_store_message": True
  },
  "AstraVectorStoreComponent-Rcqfa": {
    "api_endpoint": "https://bacdd6f7-7e3f-4bf8-b26b-615f2cc60f23-us-east1.apps.astra.datastax.com",
    "batch_size": None,
    "bulk_delete_concurrency": None,
    "bulk_insert_batch_concurrency": None,
    "bulk_insert_overwrite_concurrency": None,
    "collection_indexing_policy": "",
    "collection_name": "climate_change",
    "metadata_indexing_exclude": "",
    "metadata_indexing_include": "create_time,age,platform,country",
    "metric": "cosine",
    "namespace": "",
    "number_of_results": 70,
    "pre_delete_collection": False,
    "search_filter": "",
    "search_input": "",
    "search_score_threshold": 0.5,
    "search_type": "Similarity with score threshold",
    "setup_mode": "Sync",
    "token": "ASTRA_DB_APPLICATION_TOKEN"
  },
  "ParseData-f6T2T": {
    "sep": "\n",
    "template": "By a {user_age_group_years} {user_gender} user in {user_country} on {platform}:\\n\n{text}\\n\n(stats: {likes_count} likes, {shares_count} shares, created at: {create_time})\\n\n------------------------------------------\\n"
  },
  "ChatOutput-e266L": {
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "AI",
    "session_id": "",
    "should_store_message": True
  },
  "AnthropicModel-lI0KY": {
    "anthropic_api_key": "ANTHROPIC_API_KEY",
    "anthropic_api_url": "",
    "input_value": "",
    "max_tokens": 4096,
    "model": "claude-3-opus-20240229",
    "prefill": "",
    "stream": False,
    "system_message": "",
    "temperature": 0.2
  },
  "AstraVectorize-pSLkg": {
    "api_key_name": "OPENAI_API_KEY",
    "authentication": {},
    "model_name": "text-embedding-3-large",
    "model_parameters": {},
    "provider": "OpenAI",
    "provider_api_key": ""
  },
  "TextOutput-lEoht": {
    "input_value": ""
  },
  "ParseJSONData-NfuX4": {
    "query": ".[] | {   text,   likes_count: (.likes // \"0\") | tonumber,   comments_count: (.comments // \"0\") | tonumber,   shares_count: (.shares // \"0\") | tonumber,   create_time,   user_age_group_years: (.age // \"Not specified\"),   user_gender: (.gender // \"Not Specified\"),   user_country: (.country // \"Unknown\"),   user_follower_count: (.follower_count // \"Not specified\"),   platform: .platform }"
  },
  "TextInput-HNm8d": {
    "input_value": ""
  },
  "CustomComponent-ZUC5Q": {
    "age": "",
    "country": "",
    "datetime_from": "",
    "datetime_to": "",
    "followers": "",
    "gender": "",
    "likes_minimum": "",
    "platform": "",
    "tribe": ""
  },
  "TextInput-EEW95": {
    "input_value": "100"
  },
  "TextInput-AfI8L": {
    "input_value": ""
  },
  "TextInput-8imn9": {
    "input_value": ""
  },
  "TextInput-l2OgZ": {
    "input_value": ""
  },
  "TextInput-fe1At": {
    "input_value": ""
  },
  "TextInput-lsRPr": {
    "input_value": ""
  },
  "Memory-Tsu4T": {
    "n_messages": 50,
    "order": "Ascending",
    "sender": "Machine and User",
    "sender_name": "",
    "session_id": "",
    "template": "{sender_name}: {text}"
  },
  "Prompt-fHF9q": {
    "template": "Chat history:\n\n{history}\n\n------------------------------\n\nBelow are a number of real, relevant results from 4 social media platforms (TikTok, Facebook, YouTube, and Twitter). These snippets are all posts and comments that relate to \"{rag_query}\".\n\nThey are in a variety of languages so when you come across them please translate them into English and pass along your findings.\n\nHere are the snippets:\n\n{context}\n\n------------------------------\n\nUsing the social media posts and comments provided above do your best to answer the below question. (And don't forget in your analysis to also include some direct verbatim quotes from the text snippets from the text snippets where appropriate!)!)\n\nQuestion: {question}\n\nAnswer:\n",
    "history": "",
    "rag_query": "",
    "context": "",
    "question": ""
  },
  "TextInput-fZXlW": {
    "input_value": "narratives around climate change global warming sea level rising biodiversity renewable energy sustainability"
  },
  "TextInput-AugGK": {
    "input_value": ""
  },
  "ConditionalRouter-a2dPn": {
    "case_sensitive": False,
    "input_text": "",
    "match_text": "disabled",
    "message": "",
    "operator": "equals"
  },
  "OpenAIModel-ZQvE3": {
    "api_key": "OPENAI_API_KEY",
    "input_value": "",
    "json_mode": False,
    "max_tokens": None,
    "model_kwargs": {},
    "model_name": "gpt-4o",
    "openai_api_base": "",
    "output_schema": {},
    "seed": 1,
    "stream": False,
    "system_message": "",
    "temperature": 0.2
  },
  "CombineText-FVWkQ": {
    "delimiter": " \\n\\n-----Chat-GPT----- \\n\\n",
    "text1": "",
    "text2": ""
  }
}

if __name__ == '__main__':
  result = run_flow_from_json(flow="Climate Change RAG Test 2024140700.json",
                              input_value="message",
                              fallback_to_env_vars=True, # False by default
                              tweaks=TWEAKS)
