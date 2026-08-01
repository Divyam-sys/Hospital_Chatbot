# Hospital_Chatbot
This is my project submission for devlabs final task.

This project is implementation of AI Chatbot as a real life assistant of a hospital named AMINITY. 

This AI chatbot uses langgraph and has a basic RE-ACT type graph.

Packages to install:-
1.langgraph:- pip install -U langgraph
2.langchaim_core:- pip install langchain-core
3.langchain_google_genai:- pip install langchain-google-genai
4.langchain_community:- pip install langchain-community
5.langchain_chroma:-pip install langchain-chroma
6.langchain_text_splitters:- pip install langchain-text-splitter

To install packages run these following commands on the right on your terminal where the main.py file is located.

Requirements:-
Google GenAI API keys:- One can obtain these for free in Google Studios for free of cost and paste it in places where it is written "your-api-key".

The data files should be exactly how it is in repo, i.e., in a folder named data which is in the same folder main.py is in.

A stable Internet Connection is really important for API calling.

About The Project:-

This project is about an AI Agent which helps in booking appointments, managing them and most importantly about any queries that an user throws about the hospital.

The AI take help of 7 text files, 6 of which are non-changing while 1 is for appointment of patients.

I am using Gemini Embedding AI (Gemini Embedding 1) as embedder. I used langchain chroma for vectorization of the following contents in 6 txt files.

I splitted those long txt files into chunks so it is easy for AI to understand and also for fast API calling,

In retriever part, the similarity is set to be atmost 3 as it is not a big text file.

Three tools are defined with proper explanation of what they do in the comments for both the reader and AI agent to understand.

I have used Gemini-3.5-flash-lite as in free version of google studios, it has maximum tokens per minute.

After all the nodes and edges are initialized, a function is defined to ask the user and reply.

That is all from my side.













