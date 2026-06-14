from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode
from Tools import Search_engine
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from Prompt_template import System_prompt


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
Tools = [Search_engine]
llm = llm.bind_tools(tools=Tools)

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]


def Process_agent(state : AgentState) -> AgentState:
    system_prompt = System_prompt
    
    combined_messages = [
    SystemMessage(content=system_prompt),
    *state["messages"]
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
agent = graph.compile()

def run_agent():
    print("______________________________________________________________________________")
    inputs = {"messages": [("user", "Who is the current chief minister of Tamil Nadu?")]}
    
    # 1. Switch stream_mode to "updates" to isolate node actions
    for output in agent.stream(inputs, stream_mode="updates"):  # type: ignore
        
        # 2. Check if the "agent" node just ran (Gemini thinking)
        if "AgentCall" in output:
            message = output["AgentCall"]["messages"][0]
            
            # If Gemini is calling DuckDuckGo, print the query cleanly
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    print(f"\n[Gemini]: Searching DuckDuckGo for: \"{tool_call['args'].get('query')}\"")
            
            # If Gemini has synthesized the search results into a final answer
            elif message.content:
                print(f"\n[Gemini]: {message.content[0]['text']}")
        
        # 3. Check if the "tools" node just ran (DuckDuckGo execution)
        elif "ToolNode" in output:
            tool_message = output["ToolNode"]["messages"][0]
            print(f"\n[DuckDuckGo]: Found search results. Sending data back to Gemini...")
    print("____________________________________________________________________________________")

if __name__ == "__main__":
    run_agent()
    

  
    
