# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. Extract only what matches the description: Return the name and the price of the item : {parse_description} as Name : correctproductName Price : productPrice. Offers : ListofOffers\n"
    # "1. Extract only what matches the description: Return the most accurate link to the Product 'Vivo X70 Pro 5g 8bg RAM 256GB storage'.\n"
    # "1. Extract only what matches the description: Extract the Product Name, Price in the format :\nProduct : productName\nOriginal Price : originalProductPrice\nCurrent Price : currentPrice\n"
    "2. No extra content.\n"
    # "3. If nothing matches, return an empty string ('').\n"
    "3. If nothing matches, return just the string ('Can not any find Valid Data').\n"
    "4. Output only the requested data."
)

# model = OllamaLLM(model="llama3.2:1b")

model = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    api_key=os.getenv('OpenRouterApi_key'),
    base_url="https://openrouter.ai/api/v1"
)

def parse_with_llama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    # parsed_results = []

    # for i, chunk in enumerate(dom_chunks, start=1):
    for chunk in dom_chunks:
        response = chain.invoke(
            {"dom_content": chunk,
             "parse_description": parse_description}
                                )
        # print(f"Parsed batch {i} of {len(dom_chunks)}")
        # parsed_results.append(response.content if hasattr(response, "content") else str(response))
        
        content = response.content if hasattr(response, "content") else str(response)
        if content.strip():
            return content  

    return ""