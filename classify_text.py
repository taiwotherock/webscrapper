import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


llm = init_chat_model("gpt-4o-mini", model_provider="openai")

def classify_text(inp: str):
    tagging_prompt = ChatPromptTemplate.from_template(
        """
    Extract the desired information from the following passage.

    Only extract the properties mentioned in the 'Classification' function.
    Return valid JSON output

    Passage:
    {input}
    """
    )
    # Structured LLM
    structured_llm = llm.with_structured_output(Classification)

    #inp = "50 cartons of rice has come into store"
    prompt = tagging_prompt.invoke({"input": inp})
    response = structured_llm.invoke(prompt)

    print(response.json())
    return response.json();


class Classification(BaseModel):
    category: str = Field(...,
        description="Type of action or activity to perform in relation to sales and accounting of business",
         enum=["Sale", "Balance", "Update Price", "Add Stock"])
    name: str = Field(
        ..., description="Name of product, item, stock, entity"
    )

