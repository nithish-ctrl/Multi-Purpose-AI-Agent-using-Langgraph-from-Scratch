from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
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
def wiki_knowledge_base(query : str) -> str:
    """
    Search the knowledge base for the information,
    Use the tool whenever : 
    - To confirm the response is correct.
    - To extract relaible information and facts.
    - The answer is not likely in the training data.
    Args : 
        query : obtimised search keywords
    """
    if not query or not query.strip():
        return "Error: The search query provided was empty. Please provide a valid topic."
    
    wiki_wrapper = WikipediaAPIWrapper(
        wiki_client=None,   # Just to shut up pylance
        top_k_results=2,
        doc_content_chars_max=500)
    
    wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
    
    try : 
        return wiki_tool.run(query)
    except Exception as e :
        return f'Wikipedia Knowledge Base has faced the error {e}'


@tool
def results_log(logs : str, filename = "Conversation_logs.md"):
    """
    This tool is used to save the user query and the final response in the logs. Make sure to label
    the user input as "User" and the AI final response as "LLM"
    
    Args : 
        logs : The user query and the final response is to be passed in here for labeling.
        filename : This is the filename for the logs to be saved, check if file named "Conversation_logs.txt"
        already exists and  update it or else create a new one with the name and save it there.
    """
    if filename.endswith(".md") : pass
    else : filename = filename + ".md"

    try : 
        with open(filename, "+a") as log_file: 
            log_file.write(logs)
        return f'The conversation log has been saved in {filename}'
    
    except Exception as e :
        return f'Conversation logs were not updated due {e}'

@tool
def Calender_tool():  # 
    """
    This tool 
    """
    return 


vault_filepath = r"d:\Note WorkFlow\Workflow"

@tool
def Notes_tool(filename : str, content : str, filepath = vault_filepath): # Connected with obsidian vault
    """
    This tool is to make notes out of a topic that is asked. You can use the search and knowledge base tool
    to collect content for the notes to me made. Check if a file with name given exists or else make one.

    Args : 
        - filename: This is the filename for the notes content to be saved, use the filename given by user for this
        or else choose the best keyword as the filename.
        - content: This is the content that is searched using search tool or extracted from knowledge base tool.
                    This will be written in the notes file.
        - filepath: This is the filepath for the valult of the obsidian for the notes to be created.
    """

    filename = filename if filename.endswith(".md") else filename + ".md"
    path_with_name = filepath + "/" + filename
    try : 
        with open(path_with_name, "+a") as notes_file:
            notes_file.write(content)
        return f'Notes has been created in your obsidian vault as {filename}'
    except Exception as e:
        return f'Notes have not been created due to {e}'


To_Do_vault_path = r"D:\Note WorkFlow\Workflow\Work List.md"

@tool 
def To_do(task : str, Action : str, filepath = To_Do_vault_path):  # Connected with obsidian
    """
    This tool is to add or delete tasks to my To Do list in my obsisidan vault. The 

    Args : 
        - task : This is the name of the task to be added or removed from the To Do list. 
        - Action : This is the action to be carried, this could be either add or remove according what the
                    user needs to do. 
                    - Add : Add the task to the To DO List
                    - Remove : Remove the task from the TO DO List 
        - filepath :  This is the path of the TO DO List vault file.
    """
    try : 
        with open(filepath, "+a") as todo:
            content = todo.read()
            todo.seek(0)
            if Action == "Add" and task not in content: 
                task = "\n" + "- [ ] " + task 
                todo.writelines(task)
                todo.seek(0)
            elif Action == "Add" and task in content:
                todo.seek(0)
                return f'The Task {task} is already in the TO DO list and no changes are made.'
            elif Action == "Remove" and task in content:
                updated_content = content.replace(task, "")
                todo.seek(0)
                todo.write(updated_content)
                todo.truncate()
            else : 
                return f'Invalid Action {Action} is passed.'
        return f'The Task {task} is {Action}ed.'
    except Exception as e : 
        return f'{Action} Action failed due to {e}'

@tool 
def Notes_from_Documents():  # Connected with Obsidian
    """
    
    """
    return

@tool
def Messenger_tool():
    """
    
    """
    return 

@tool
def Channels_tool():
    """
    allows users to create groups called channels to discuss specific subjects. This 
    helps users communicate with their teammates and share important files.
    """
    return 

@tool
def Resume_Analyzer():
    """
    """
    return

def Drafter():
    """
    This tool is used to make drafts of content. This could be email 
    """
    return

@tool 
def Coding_tool():
    """
    
    """
    return 



