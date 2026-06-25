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
            log_file.writelines(logs)
        return f'The conversation log has been saved in {filename}'
    
    except Exception as e :
        return f'Conversation logs were not updated due {e}'

@tool
def Clock_tool(use : str, duration : int, purpose : str, break_time = 0, iterations=1):  #  
    """
    This tool can set up a timer, reminder or a pomodoro time in case of productive mode according
    to the user needs.

    Args : 
        - use :
            - Timer : 
            - Reminder
            - Pomodoro-Timer : 
        
        - duration : This is the duration in case of the timer and pomodoro timer and is the
                     time to set the reminder in case of reminder. The duration must be entered in minutes.

        - purpose : This could be a purpose of reminder, the purpose of time or the purpose for pomodoro-timer.

        - break_time : This will be the break time in between the pomodoro sessions. It is 0 if there is no information
                        regarding the break duration.
       
        - iterations : The number of pomodoro sessions required by the user, It is 1 if there is no 
                       information regarding that.

    """
    from threading import Timer
    import time 

    duration_in_seconds = duration * 60 
    break_time_in_seconds = break_time * 60

    if use == "Timer" :  
        def timer_function():
            return f"The timer is done for {purpose}"
        timer = Timer(duration_in_seconds, timer_function)
        print(f'Your timer for the purpose {purpose} has started.')
        timer.start()
    
    elif use == "Pomodoro-Timer" : 
        def Productive_end(last_session : str):
            if last_session == "Productive":
                return f'The Produtive session for {duration} minutes has ended, Take a break for {break_time}'
            if last_session == "Break" : 
                return f'Break session for {break_time} mins has ended, back to productive sessions.'
            
        session_count = 1
        pomodoro_timer = Timer(duration_in_seconds, Productive_end, args=("Productive",))
        break_timer = Timer(break_time_in_seconds, Productive_end, args=("Break",))
        print(f"Pomodoro session is started for {iterations} iterations for {duration} each with a break of {break_time} time.")
        print(f'STARTED !!')
        while session_count <= iterations : 
            if session_count == iterations : 
                pomodoro_timer.start()
                print("Pomodoro Iterations ends, Congrats !!, have a nice time.")
            else : 
                pomodoro_timer.start()
                #break_timer.start()
                #time.sleep(break_time_in_seconds)
            session_count+=1

    elif use == "Reminder" : 
        pass


vault_filepath = r"D:\Note WorkFlow\Workflow\Notes from the Agent"

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
    description. The result will be the similarity score, vault_filename, vaultpath, resume_text, JD_text.
    You must summarize the text from resume and text from JD and pass it to the notes_tool. 
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
    resume_embeddings = model.encode(resume_text, convert_to_tensor=True)
    JD_embeddings = model.encode(JD_text, convert_to_tensor=True)
    
    semantic_similarity = util.cos_sim(resume_embeddings, JD_embeddings)

    similarity_score = 0.1 * fuzz_similarity + 0.9 * semantic_similarity
    print(f'Similarity Score : {similarity_score}')

    return similarity_score, vault_filename, vault_path, resume_text, JD_text, f'The similarity score is {similarity_score}'

@tool
def Productivity_mode(work : str, duration : str, iteration : int, break_duration : str):
    """
    This tool is set up everything for the user to work lock in and work productively. This productivity 
    periods works iteratively with a duration for each period and a break in between them. The work is to be added to the todo list 
    using the Todo tool. Then the clock tool is to be called iteratively with breaks according to the number of sessions and duration
    period with breaks is wanted by the user. 
    The iterations will be the number of pomodoro sessions the user wants to focus for.
    The duration is the length of each pomodoro session.
    Break duration will a timer of that duration for break in between the pomodoro sessions.
    All these have to implemented using the clock tool.

    Args : 
        - Work : This is the work to be added to the to do list.
        - duration : The duration of one productivity period.
        - iteration : Number of iterations of this productivity period.
        - break_duration : The duration of break between each productivity period.
    """
    return


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

def Talkback_mode(response : str, Goat : str, ):
    """
    This tool is basically to turn on Speech mode so the conversation with the LLM can take place using Speech. There are few voices the LLM model can
    choose from to talk back to the user with the response to the query. The voice of goat argument will take care of that.


    Args : 
        - response : This is the response that the model want to be converted to Audio to be played back to the user. This is 
        - Voice_of_Goat : Either of the four given names should be passed in as the input.
                - Jarvis : 
                - Optimus Prime : 
                - Johnny Lawrence : 
                - Yoda : 
        - 
    """

    return 


@tool
def Messenger_tool(message : str, platform : str, receiver_details : str):
    """
    This tool will send messages via platforms such as telegram and email, the platform is to and receiver details is to be extracted from
    the user's prompt to the LLM. The sender's details is already coded into the tool, LLM does not have to ask for sender details to the User.

    Args : 
        - message : This is the message to be sent to the receiver through any of the platforms mentioned.
        - platform : This is the platform through which the message will be sent. 
            - email -  
            - telegram - 
            - whatsapp - 
            - sms - 
        - receiver_details : This contains the receiver's details. This could be an email address in case of an email platform, an number
                             in case of sms or whatsapp or telegram platform.
    
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


tool_filepath = r"C:/Users/Nithish/Agents From Scratch Using Langgraph/Search Engine Agent/tool_check.py"

@tool 
def MakeYourOwn_tool(docstring : str, name : str, code : str, tool_filepath = tool_filepath):
    """
    The User can create a custom tool using this tool.

    Args : 
        - docstring : This has the description about the tool to be made so it can be called by the LLM.
                      This is the doc string description and all the arguments should be clearly explained
                      in this.
        - name : This is the name of the tool to be created, it should be one or two words at max separated by _,
                 the name itself should reflect the tool's working.
        - code : This is the code to be written inside the tool for it to do the itended working.
                 This should be in the form of a function definition with even imports present inside the 
                 function. 
        - tool_filepath : This is the filepath where the tool code is to be added to.
    
    """
    #tool_filepath_with_name = os.path.join(tool_filepath, name)
    name = name + "_tool"
    #tool_template = 
    f"""
    @tool
    def {name}()
    """
    with open(tool_filepath, "+a") as toolfile : 

        toolfile.writelines("\n@tool\n")
        toolfile.writelines(code)
        toolfile.writelines("\n")
    return print(f'The tool is coded into the itended python file with the name {name}.')



