from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.messages import trim_messages
from langgraph.graph import StateGraph, START, END, add_messages, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver 
from Tools import Search_engine, wiki_knowledge_base, results_log, To_do, Notes_tool, Notes_from_Documents, Resume_Analyzer, Clock_tool, MakeYourOwn_tool
from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI 
from Prompt_template import System_prompt
from langchain_mistralai import ChatMistralAI


load_dotenv()

llm = ChatMistralAI(model_name="mistral-medium-3-5")
Tools = [Search_engine, wiki_knowledge_base, results_log, To_do, Notes_tool, Notes_from_Documents, Resume_Analyzer, Clock_tool, MakeYourOwn_tool]
llm = llm.bind_tools(tools=Tools)

checkpointer = MemorySaver()

class AgentState(MessagesState):
    # messages : Annotated[Sequence[BaseMessage], add_messages] # this is the same as just using MessageState instead of TypedDict
    pass

def Process_agent(state : AgentState) -> AgentState:
    system_prompt = System_prompt

    trimmed_history = trim_messages(
                state["messages"],
                strategy = "last",
                token_counter="approximate",
                max_tokens=10000,
                start_on="human",
                end_on=("human", "tool")
                )
    
    combined_messages = [
    SystemMessage(content=system_prompt),
    *trimmed_history
    ]
    
    response = llm.invoke(combined_messages)

    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")
    
    return {"messages" : [response]} 

def should_continue(state : AgentState) -> str:
    """
    To decide whether to continue or end it.
    """
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls : 
        return "continue"
    else : return "end"

graph = StateGraph(AgentState)
graph.add_node("AgentCall",Process_agent)


Toolnode = ToolNode(tools=Tools)
graph.add_node("ToolNode", Toolnode)

graph.add_edge(START, "AgentCall")
graph.add_conditional_edges(
    "AgentCall",
    should_continue,
    {
        "end" : END,
        "continue" : "ToolNode"
    }
)
graph.add_edge("ToolNode", "AgentCall")
agent = graph.compile(checkpointer=checkpointer)

def run_agent():
    print("_____________________________________________________________________________________________________________________________")

    config = {"configurable": {"thread_id": "session_1"}}

    while True : 
        user_input = input("Enter the prompt (or type exit or quit): ")
        
        if user_input.lower() == "quit" or user_input.lower() == "exit" : 
            print(f"Alright, Byee until you call me back..See ya !!")
            break

        inputs = {"messages": [("user", user_input)]}

        for output in agent.stream(inputs,config=config, stream_mode="updates"):  # type: ignore
            
            if "AgentCall" in output:
                message = output["AgentCall"]["messages"][0]
                
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        print(f"\n[LLM]: Searching Tools for: \"{tool_call['args'].get('query')}\"")
                
                elif message.content:
                    #print(f"\n[LLM]: {message.content[0]['text']}") This is extract the text from Google Gemini Model
                    print(f'LLM : {message.content}')
            
            elif "ToolNode" in output:
                tool_message = output["ToolNode"]["messages"][0]
                print(f"\n[Tools]: Pretty much done, Sending data back to LLM...")
        
        print("___________________________________________________________________________________________________________________")

if __name__ == "__main__":
    run_agent()
    

  
    
