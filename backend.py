from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.agents import load_tools,initialize_agent
from  langchain.agents.agent_types import AgentType


os.environ['GOOGLE_API_KEY'] = 'AIzaSyAlFVtdo7fydnGiv5FKB3zfh40aPf_g5Q8'
os.environ['GOOGLE_CSE_ID'] = '8268e1c6e88c94aeb'
search = GoogleSearchAPIWrapper()
google_tool =  Tool(
    name='google-search',
    description='search google for recent results',
    func= search.run,
)

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                   google_api_key = 'AIzaSyAlFVtdo7fydnGiv5FKB3zfh40aPf_g5Q8',
                                   temperature=0,
                                   convert_system_message_to_human=True,
                                   harm_block_threshold={"Derogatory": "BLOCK_NONE"},
                                   search = 'mmr',                                                                     
                                   )


def get_answer(question,history):
    tool = ["google-search"]
    tools = load_tools(tool,llm)
    agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose = True,chat_history = history) 
                  
    # answer = con_chain.invoke({'context':result['related_questions'],'question':query,'chat_history':[]})
    # query=input("Enter question: ")#"where was the 6th edition of International Conference on Disaster Resilient Infrastructure held and give me details on it?"
    # if query.lower()=='exit':
    #     sys.exit()
    answer = agent.invoke(question)
    # print("Answer:",answer)
    return answer
