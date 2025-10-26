import os
import time
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Type, List, Optional
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage
from openai import APIConnectionError

from patriot.prompts import DEFAULT_SYSTEM_PROMPT

# Initialize the LLM
# Use Gemini if the API key is provided, otherwise fall back to OpenAI
if os.getenv("GEMINI_API_KEY"):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, api_key=os.getenv("GEMINI_API_KEY"))
else:
    llm = ChatOpenAI(model="gpt-4.1", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    output_schema: Optional[Type[BaseModel]] = None,
    tools: Optional[List[BaseTool]] = None,
) -> AIMessage:
  final_system_prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT
  
  prompt_template = ChatPromptTemplate.from_messages([
      ("system", final_system_prompt),
      ("user", "{prompt}")
  ])

  runnable = llm
  if output_schema:
      runnable = llm.with_structured_output(output_schema, method="function_calling")
  elif tools:
      runnable = llm.bind_tools(tools)
  
  chain = prompt_template | runnable
  
  # Retry logic for transient connection errors
  for attempt in range(3):
      try:
          return chain.invoke({"prompt": prompt})
      except APIConnectionError as e:
          if attempt == 2:  # Last attempt
              raise
          time.sleep(0.5 * (2 ** attempt))  # 0.5s, 1s backoff
