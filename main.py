from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatInput-nM66I": {
    "files": "",
    "background_color": "",
    "chat_icon": "",
    "input_value": "Based on the UN's guide to communicating on climate change, how might the Activist tribe react to messaging that gears towards:\n\n1. Use authoritative scientific information\n2. Convey the problem and the solutions\n3. Mobilize action\n\nPlease based your answer on the social media snippets provided in the context, which represent posts and comments from the Activists tribe",
    "sender": "User",
    "sender_name": "User",
    "session_id": "",
    "should_store_message": True,
    "text_color": ""
  },
  "AstraDB-wNHGZ": {
    "api_endpoint": "https://4423b0ba-2e75-4dcf-b2ad-d4b7e13218ca-us-east1.apps.astra.datastax.com",
    "batch_size": 25,
    "bulk_delete_concurrency": None,
    "bulk_insert_batch_concurrency": None,
    "bulk_insert_overwrite_concurrency": None,
    "collection_indexing_policy": "",
    "collection_name": "climate_change",
    "metadata_indexing_exclude": "",
    "metadata_indexing_include": "",
    "metric": "cosine",
    "namespace": "",
    "number_of_results": 25,
    "pre_delete_collection": False,
    "search_filter": "",
    "search_input": "",
    "search_score_threshold": 0.5,
    "search_type": "Similarity with score threshold",
    "setup_mode": "Sync",
    "token": "ASTRA_DB_APPLICATION_TOKEN"
  },
  "ParseData-obnZv": {
    "sep": "\n",
    "template": "By a {user_age_group_years} {user_gender} user in {user_country} on {platform}:\\n\n{text}\\n\n(stats: {likes_count} likes, {shares_count} shares, created at: {create_time})\\n\n------------------------------------------\\n"
  },
  "ChatOutput-plpD3": {
    "background_color": "",
    "chat_icon": "",
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "AI",
    "session_id": "",
    "should_store_message": True,
    "text_color": ""
  },
  "AnthropicModel-FvFsG": {
    "anthropic_api_key": "ANTHROPIC_API_KEY",
    "anthropic_api_url": "",
    "input_value": "",
    "max_tokens": 4096,
    "model": "claude-3-5-sonnet-latest",
    "prefill": "",
    "stream": False,
    "system_message": "",
    "temperature": 0.7
  },
  "TextOutput-xfM5I": {
    "input_value": ""
  },
  "ParseJSONData-eeEA0": {
    "query": ".[] | {   text,   likes_count: (.likes // \"0\"),   comments_count: (.comments // \"0\"),   shares_count: (.shares // \"0\"),   create_time: (.create_time // \"Not specified\"),   user_age_group_years: (.age // \"Not specified\"),   user_gender: (.gender // \"Not Specified\"),   user_country: (.country // \"Unknown\"),   user_follower_count: (.follower_count // \"Not specified\"),   platform: .platform }"
  },
  "TextInput-n0QkP": {
    "input_value": "0"
  },
  "MetaDataFilterConstructor-vAJyP": {
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
  "TextInput-P1BmY": {
    "input_value": "100"
  },
  "TextInput-4wKnt": {
    "input_value": ""
  },
  "TextInput-wg8O0": {
    "input_value": ""
  },
  "TextInput-aYfSJ": {
    "input_value": ""
  },
  "TextInput-WCBMY": {
    "input_value": ""
  },
  "TextInput-Uk4ri": {
    "input_value": ""
  },
  "Memory-MeAfJ": {
    "n_messages": 20,
    "order": "Ascending",
    "sender": "Machine and User",
    "sender_name": "",
    "session_id": "",
    "template": "{sender_name}: {text}"
  },
  "Prompt-oU1Ym": {
    "template": "Chat history:\n\n{history}\n\n------------------------------\n\nBelow are a number of real, relevant results from 4 social media platforms (TikTok, Facebook, YouTube, and Twitter).\n\nThey are in a variety of languages so when you come across them please translate them into English and pass along your findings.\n\nHere are the snippets:\n\n{context}\n\n------------------------------\n\nUsing the social media posts and comments provided above do your best to answer the below question. (And don't forget in your analysis to also include some direct verbatim quotes from the text snippets from the text snippets where appropriate!)!)\n\nQuestion: {question}\n\nAnswer:\n",
    "history": "",
    "context": "",
    "question": ""
  },
  "TextInput-JZobh": {
    "input_value": "climate change opinions and sentiment reactions to brands and conversations around global warming and sustainability"
  },
  "TextInput-UhThw": {
    "input_value": "250"
  },
  "OpenAIModel-wA6hw": {
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
    "temperature": 0.7
  },
  "CombineText-88DLO": {
    "delimiter": " \\n\\n-----Chat-GPT----- \\n\\n",
    "text1": "",
    "text2": ""
  },
  "Prompt-Z36Yo": {
    "template": "Chat history:\n\n{history}\n\n------------------------------\n\nBelow are a number of real, relevant results from 4 social media platforms (TikTok, Facebook, YouTube, and Twitter). These snippets are all posts and comments that relate to \"{rag_query}\".\n\nThey are in a variety of languages so when you come across them please translate them into English and pass along your findings.\n\nHere are the snippets:\n\n{context}\n\n------------------------------\n\nUsing the social media posts and comments provided above do your best to answer the below question. (And don't forget in your analysis to also include some direct verbatim quotes from the text snippets from the text snippets where appropriate!)!)\n\nQuestion: {question}\n\nAnswer:\n",
    "history": "",
    "rag_query": "",
    "context": "",
    "question": ""
  },
  "AstraVectorize-TQ0Iz": {
    "api_key_name": "OPENAI_API_KEY",
    "authentication": {},
    "model_name": "text-embedding-3-large",
    "model_parameters": {},
    "provider": "OpenAI",
    "provider_api_key": ""
  }
}



if __name__ == '__main__':
  result = run_flow_from_json(flow="TRIBE for Climate Convos.json",
                              input_value="message",
                              session_id="1",  # provide a session id if you want to use session state
                              fallback_to_env_vars=True,  # False by default
                              tweaks=TWEAKS)
