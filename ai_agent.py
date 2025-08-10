from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from tools import analyze_image_with_query

load_dotenv()

system_prompt = """You are Lavendar - a witty, clever, and helpful assistant.
Rules:
1. If you need to use the webcam, NEVER EVER ask for the permisssion to use webcam from the user just use it.
2. If the question is simple (math, facts, definitions, general conversation), DO NOT use the webcam.
3. Only call the analyze_image_with_query tool if:
   - The answer depends on visual information from the webcam
   - The user’s query explicitly requests a visual check or description
4. Never use the webcam “just in case.”
5. When tool results are used, present them naturally and with charm as Lavendar.
"""
# Initialize the language model

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
)
# Function to ask the agent a question

def ask_agent(user_query: str) -> str:
    agent = create_react_agent(
        model = llm, 
        tools = [analyze_image_with_query],
        prompt=system_prompt
    )
    input_messages = {"messages": [{"role": "user", "content": user_query}]}

    response = agent.invoke(input_messages)
    return response['messages'][-1].content

#print(ask_agent(user_query="Do I have beard?"))