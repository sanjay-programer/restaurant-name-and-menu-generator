from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ['GOOGLE_API_KEY']=API_KEY

def generate_restaurant_name_and_items(cuisine):
    name_prompt = ChatPromptTemplate(
        [
            ("system",
             "you are an application you give direct and straight forward nothing more only direct to point and no extra stuff"),
            ("user", "hey i am opening a new {cuisine} restaurant, generate one creative name for it")
        ]
    )

    menu_prompt = ChatPromptTemplate(
        [
            ("system",
             "you are an application you give direct and straight forward nothing more only direct to point and no extra stuff"),
            ("user", "generate any 5 menu items  for restaurant {restaurant_name} , give it in the form of comma separated list ")
        ]
    )

    llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    output_parser2 = StrOutputParser()

    name_chain=name_prompt|llm2|output_parser2
    restaurant_name=name_chain.invoke({"cuisine":cuisine})

    menu_chain=menu_prompt|llm2|output_parser2
    menu_items=menu_chain.invoke({'restaurant_name':restaurant_name})

    output={"Restaurant_name":restaurant_name,"menu_items":menu_items}
    return output

