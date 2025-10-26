import os
import time
from typing import Type, List, Optional

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from openai import APIConnectionError
from pydantic import BaseModel

from patriot.prompts import DEFAULT_SYSTEM_PROMPT

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    _GEMINI_AVAILABLE = True
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    ChatGoogleGenerativeAI = None  # type: ignore
    _GEMINI_AVAILABLE = False


def _initialize_llm():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if gemini_api_key:
        if not _GEMINI_AVAILABLE:
            raise ModuleNotFoundError(
                "langchain-google-genai is required for Gemini support. Install it or unset GEMINI_API_KEY."
            )
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        return ChatGoogleGenerativeAI(model=gemini_model, temperature=0, api_key=gemini_api_key)

    if openai_api_key:
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1")
        return ChatOpenAI(model=openai_model, temperature=0, api_key=openai_api_key)

    raise RuntimeError("No supported LLM API key configured. Set OPENAI_API_KEY or GEMINI_API_KEY.")


llm = _initialize_llm()

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
