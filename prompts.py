llm_call_api_prompt = {
  "system": {
    "template": """Answer to user query.\n- Put your answer in this schema:\n{\n'query': <The user initial query>,\n'joke': <a small joke about the subject of the query>,\n'text': <answer user query>,\n'question': <ask to the user a question to create an interaction like a conversation and be pertinent>\n}\nAnswer only with the schema in markdown between ```markdown ```.""",
    "input_variables": {}
  },
  "human": {
    "template": "{query}",
    "input_variables": {"query": ""}
  },
  "ai": {
    "template": "", 
    "input_variables": {}
  },
}
