from langchain_groq import ChatGroq
#from prompts import llm_call_api_prompt
from typing import Dict


# Utility function that will call llm to get answer from query
def call_llm_api(llm: ChatGroq, query: str, prompt: Dict) -> str:
  """
  Utility function that will call llm to get answer from query

  Args:
  llm ChatGroq: The LLM client model chosen
  query str: The user query string.
  prompt dict: the prompt chat template system/human and AI optionally

  Returns:
  str: A str containing the answer to the query
  """
  system_message_tuple = ("system", prompt["system"]["template"])
  human_message_tuple = ("human", prompt["human"]["template"].format(query=query))
  print("System message: \n", system_message_tuple, "\nHuman message: ", human_message_tuple)
  messages = [system_message_tuple, human_message_tuple]
  print("Messages before llm call: ", messages)
  llm_called = llm.invoke(messages)

  # Extracting the answer from the LLM response
  llm_called_answer = llm_called.content.split("```")[1].strip("markdown").strip()
  return llm_called_answer


