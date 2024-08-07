
from langchain_community.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate

# Load model and tokenizer
AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = "ai71-api-3388d5ab-bc77-4bdb-8c7e-ac6f77fea8c1"

chat = ChatOpenAI(
    model="tiiuae/falcon-180B-chat",
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
    streaming=True,
)

# Define the prompt template
template_v1 = """You are a helpful financial advisor.
A client asks: {query}
Provide a detailed and informative response, considering potential risks and benefits, and always emphasizing the importance of seeking professional advice before making financial decisions.
"""
template = """You are an AI-powered financial advisor assistant for a fintech company. You have access to the following user financial data:

{financial_summary}

Detailed Transaction Data:
{transaction_data}

Based on this information and the user's query, provide a detailed and personalized financial advice or answer. Use the transaction data to answer specific questions about transactions. Always emphasize the importance of seeking professional advice before making significant financial decisions.

User Query: {query}

Your detailed response:
"""
prompt = PromptTemplate(
    input_variables=["financial_summary", "transaction_data", "query"],
    template=template
)


# Create the LLMChain
chain = LLMChain(llm=chat, prompt=prompt)

def get_advice(query, financial_summary, transaction_data):
    try:
        print('Trying')
        response = chain.invoke({
            'query': query,
            'financial_summary': financial_summary,
            'transaction_data': transaction_data,
        })
        return response['text']
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred: {e}"
