from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
import os

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
    This tool is to add or delete tasks to my To Do list in my obsisidan vault. 

    Args : 
        - task : This is the name of the task to be added or removed from the To Do list. 
        - Action : This is the action to be carried, this could be either add or remove according what the
                    user needs to do. 
                    - Add : Add the task to the To DO List
                    - Remove : Remove the task from the TO DO List 
        - filepath :  This is the path of the TO DO List vault file.
    """
    try : 
        with open(filepath, "r+") as todo:
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
                task = "- [ ] " + task
                updated_content = content.replace(task, "").replace("\n\n", "\n")
                todo.seek(0)
                todo.write(updated_content)
                todo.truncate()
            else : 
                #return f'Invalid Action {Action} is passed.'
                return f'Action is {Action} but task is not present in the to do list.'
        return f'The Task {task} is {Action}ed.'
    except Exception as e : 
        return f'{Action} Action failed due to {e}'


doc_dir = "C:/Users/Nithish/Agents From Scratch Using Langgraph/Search Engine Agent"
@tool 
def Notes_from_Documents(notes_filename : str, document_name : str, vault_path = vault_filepath, document_dir = doc_dir):  # Connected with Obsidian
    """
    This tool is make notes from documents. Extraction of the content, keywords are made.
    Then along with the content, the keywords are searched and made notes using Notes_tool. 
    The file is also summarised in the end. 
    Document to be read is present in the document_dir with name as document_name.

    Args : 
        - vault_path : This is the filepath of the vault on which the extracted text, notes and summary is to be updated.
        - notes_filename: This is the filename for the notes content to be saved, use the filename given by user for this
                    or else choose the best keyword as the filename.
        - document_name : This is the name of the document from which the text will be extracted from, this is passed by the user exactly.
                          No need to ask the user for confirmation, can use it directly.
        - document_dir : This is the dirctory of the file to be read.
    """

    import fitz
    notes_filename = notes_filename if notes_filename.endswith(".md") else notes_filename + ".md"
    full_doc_path = os.path.join(document_dir, document_name)
    doc = fitz.open(full_doc_path)
    doc_content = "\n".join([str(page.get_text()) for page in doc]) 
    filename_with_vault = os.path.join(vault_path, notes_filename) 
    try :
        with open(filename_with_vault, "w+") as content : 
            content.write(doc_content)
        return f'The content is extracted and {notes_filename} is created with notes in the vault folder.'
    except Exception as e : 
        return f'The content extraction from the document failed due to {e}.'


resume_JD_vaultpath = "D:/Note WorkFlow/Workflow/Resume-JD-Vault"
resume_JD_dir = "D:/Inputs for Agent"
@tool
def Resume_Analyzer(Resume_name : str, Job_desc_name : str, vault_filename : str, Resume_and_JD_path = resume_JD_dir , vault_path = resume_JD_vaultpath):
    """
    This tool is to compare the resume and job decription documents and give suggestions about them and 
    improvements to the user about what they should focus on to prepare for the job specified in the job
    description. The result will be the similarity score, vault_filename, vaultpath which you will pass to the notes file to update everything to the vault.
    Make sure to add it with labels, 
    Summary of the resume "Resume summary", Summary of the JD as "JD Summary" and then Similarity score.
    Args : 
    - Resume_name : This is the name of the resume file from which the text will be extracted from, this is passed by the user exactly.
                    No need to ask the user for confirmation, can use it directly.

    - Job_desc_name : This is the name of the Job desciption file from which the text will be extracted from, this is passed by the user exactly.
                      No need to ask the user for confirmation, can use it directly.

    - Resume_and_JD_path : This is the dirctory of both the Resume and Job description.

    - vault_filename : This is the filename for the notes content to be saved, use the filename given by user for this
                        or else choose the best keyword as the filename.

    - vault_path : This is the filepath of the vault on which the extracted text, and similarity score is to be updated.
    """

    import fitz
    from thefuzz import fuzz
    from sentence_transformers import SentenceTransformer, util

    if not vault_filename.endswith(".md") : vault_filename += ".md"

    resume_path = os.path.join(Resume_and_JD_path, Resume_name)
    JD_path = os.path.join(Resume_and_JD_path, Job_desc_name)
    notes_path = os.path.join(vault_path, vault_filename)

    resume_doc = fitz.open(resume_path)
    JD_doc = fitz.open(JD_path)

    resume_text = "\n".join([str(page.get_text()) for page in resume_doc])
    JD_text = "\n".join([str(page.get_text()) for page in JD_doc])
    fuzz_similarity = fuzz.ratio(resume_text, JD_text)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    resume_encoding = model.encode(resume_text, convert_to_tensor=True)
    JD_encoding = model.encode(JD_text, convert_to_tensor=True)
    
    semantic_similarity = util.cos_sim(resume_encoding, JD_encoding)

    similarity_score = 0.1 * fuzz_similarity + 0.9 * semantic_similarity
    print(f'Similarity Score : {similarity_score}')

    return similarity_score, vault_filename, vault_path, f'The similarity score is {similarity_score}'

@tool
def Drafter():
    """
    This tool is used to draft content. 

    Args : 
        - 
        - 
        - 
        - 
    """
    return

def Jarvis_mode():
    """


    Args : 
        - 
        - 
        - 
    """
    return 

def tranformers_mode() : # Either with Jarvis or separately.
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
    Or Bulk emailing can be done too.
    """
    return 

@tool 
def Coding_tool():
    """
    
    """
    return 



