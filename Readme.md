# Multi Purpose AI Agent using Langgraph 

This repository contains concept and code for building AI Agents using langgraph and langchain from absolute basics.

## Why do I need to use these ? Can't I just access them in my browser ? 
Yes, to be honest these wont perform better than what you can access from your browser. This is not a production level Project. This is a fun project made with intention of playing around langgraph and langchain. Its a really fun project to take up. 


## Table of contents : 
### 1. Model file
### 2. Tools
### 3. Main
### 4. Prompt Template
### 5. Requirements
### 6. Conversation Logs

## Model File : 
This file contains the code to load the local LLM, even though I later changed it to using Gemini 2.5-flash later using API calls, the code does not change much. 

## Tools File : 
This file contains the necessary tools required to be called and used by the model. We have used native tool calling. 
The available tools are : 
###      1.  Search Engine Tool : 
Using DuckDuckGo to access information from internet and also obtain as much privacy as possible.  

###      2.  Knowledge Base Tool : 
Currently wikipedia is used as knowledge base, honestly there is very high chance that the model is already trained on this data. But this tool can be substituted with other data which could be retrieved and a potential integration of RAG application and minimum hallucination. 

###      3. Coding Agent Tool : 
This will serve as a basic coding tool with debugging capabilities, maybe also help in building small projects. The implemenation will be having a smaller model but I will try to make it as modular as possible, so a larger and better model can be substituted in its place without any major code changes.

###       4. Result Log Tool : 
This will serve as a backup file for the whole conversation in case of accidental data deletion or other issues. This can also be used for feedback loops leading to potential improvements. 

###        5. Clock Tool :
This tool will help in making timers, reminders and pomodoro sessions. This tool can be called by the productivity mode tool to create pomodoro sessions iteratively as mentioned by the user with a required
break time in between sessions.

###        6. Notes Tool :
This tool will basically let the LLM search the internet about the topic given and then make notes in my obsidian vault about the topic.

###        7. To Do Tool :
This tool can add or remove tasks to and from my Todo file from my obsidian vault.

###        8. Notes from Document Tool :
This tool can open a pdf document and extract the text from it and paste the text in obsidian vault. 

###        9. Resume Analyzer Tool : 
This tool takes the resume file and Job description file does a basic keyword + Semantic similarity search and gives a similarity score, trying it also give suggestions about what to improve. 
Currently it reads from a particular directory, change it to yours if you are cloning the rep.

###        10. Talk back Mode : 
This tool can make the LLM talk with the user instead of taking ang giving response through the terminal as text. Bascially like Alexa, 
bixby or Jarvis (delulu).
There are various available voices in this which would like to call as the voices of goats :
####                    Jarvis : 
                            Yes, voice of the goat "Jarvis". 
####                    Optimus Prime :
                            Autobots, roll out.
####                    Yoda :
                            Im not sure I could switch the words like how yoda talks but im sure i can get Yoda's voice atleast. Hoping for the best.
####                    Johnny Lawernce : 
                            This is my favourite character from the series "Cobra Kai" along with Miguel Diaz ofc, I will try my best to bring his unique way of answering to questions, Well.. QUIET !!!!!...No promises and No Mercy. 
                            Cobra Kai never dies. 

###        11. Productivity Mode Tool :
This tool is used to help the user with productive tasks, a number of pomodoro sessions can be made with breaks for the user to work.
The work will be added to the task list and will be crossed out at the end of session if the whole period has been reached, or else it
remains in the todo list. The clock tool will be called to make these sessions and the todo tool for adding the removing the tasks. 

## Main File : 
This file contains the main code to be implemented, all the other files are imported and user interaction takes place here.

## Prompt Template : 
This file contains the prompt to be passed as the system prompt to SystemMessages to the model. It contains role of the model, what is it supposed to do and the guidelines it is supposed to follow to improve the output, this can be updates as per the need. 

## Requirement file : 
This file contains all the dependencies and libraries required to be installed. Actually I might have forgotten to add one or two, so do let me if that is so.

## Conversation Logs : 
This file contains the conversation logs, this file is updated by the tool results_log after every prompt and its response, since I have not updated the prompt-response loop yet. 