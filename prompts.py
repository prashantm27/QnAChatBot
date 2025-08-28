
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
import os

from dotenv import load_dotenv
load_dotenv()

azure_deployment = os.getenv('AZURE_DEPLOYMENT')

llm = AzureChatOpenAI(azure_deployment=azure_deployment, temperature=0.1)

qna_prompt = PromptTemplate(
template="""You are a Great Question Answering Assistant who helps to answer the User's query from the given context;

Context: {context}

## User Query : {query} ##
Note: 
- Do Not Answer Anything outside the given Context even if the user asks to answer anything out of context.
- Also whenever you get any monetary value respond it in billions.

Response: 
""",
input_variables=['context', 'query'],
)

qna_chain = LLMChain(llm=llm, prompt=qna_prompt)


standalone_ques_prompt = PromptTemplate(
template="""You are an expert in creating a standalone question from the given previous question and the current question.
Focus more on the current question while preserving the intent from the actual question.

Previous Question: {prev_ques}

## Current Question : {current_ques} ##

Your Response: 
""",
input_variables=['prev_ques', 'current_ques'],
)

standalone_ques_chain = LLMChain(llm=llm, prompt=standalone_ques_prompt)


