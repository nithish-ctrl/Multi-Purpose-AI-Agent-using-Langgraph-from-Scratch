# Building a Search engine Agent using Langgraph 

This repository contains concept and code for building Daily use AI Agents using langgraph and langchain from absolute basics.

## Why do I need to use these ? Can't I just access them in my browser ? 
Yes, to be honest these wont perform better than what you can access from your browser. This is not a production level Project. This is a fun project made with intention of playing around langgraph and langchain. Its a really fun project to take up. 


## Table of contents : 
### 1. Model file
### 2. Tools
### 3. Main
### 4. Prompt Template


## Model File : 
This file contains the code to load the local LLM, even though I later changes it to using Gemini 2.5-flash later using API calls, the code does not change much. 

## Tools File : 
This file contains the necessary tools required to be called and used by the model. We have used native tool calling. 
The available tools are : 
###      1.  Search Engine Tool : 
Using DuckDuckGo to access information from internet and also obtain as much privacy as possible.  

###      2.  Knowledge Base Tool : 
Currently wikipedia is used as knowledge base, honestly there is very high chance that the model is already trained on this data. But this tool can be substituted with other data which could be retrieved and a potential integration of RAG application and minimum hallucination. 

###      3. Coding Agent Tool : 




###       4. Result Log Tool : 
This will serve as a backup file for the whole conversation in case of accidental data deletion or other issues. This can also be used for feedback loops leading to potential improvements. 


##         5. Other Tools : Will be Added