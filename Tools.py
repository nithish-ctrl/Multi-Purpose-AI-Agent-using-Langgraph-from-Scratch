from langchain.tools import tool
#from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchResults
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper


@tool
def Search_engine(query : str)-> str:
    """
    Search the internet for current information.
    Use this tool whenever:
    - the user asks about current events
    - the user asks for recent information
    - the user asks for live prices
    - the answer is not likely in training data
    Args:
        query: Optimized search keywords
    """
    search = DuckDuckGoSearchAPIWrapper(max_results=3)
    return search.run(query)
    
@tool 
def wiki_knowledge_base():
    """
    
    """

    return 

@tool
def results_log():
    """
    
    """

    return 
  

