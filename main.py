import os
import random
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict, Sequence
from langchain_core.messages import BaseMessage,SystemMessage,ToolMessage,HumanMessage,AIMessage
from operator import add as add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import ToolNode

embedding=GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    api_key="your-api-here"
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

DATA_FOLDER = "data"

documents = []

for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".txt") and filename != "aminity_hospital_appointment":
        filepath = os.path.join(DATA_FOLDER, filename)

        loader = TextLoader(filepath, encoding="utf-8")
        docs = loader.load()

        # Store the filename as metadata (optional but useful)
        for doc in docs:
            doc.metadata["source"] = filename

        documents.extend(docs)

print(f"Loaded {len(documents)} documents.")

#slicing

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.")
print(len(documents))
print(len(chunks))
#vector database
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./hospital_db"
)

retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

@tool
def query_hospital_knowledgebase(query: str) -> str:
    """Useful for retrieving information from the hospital database.
    Input should be a clear search query string related to hospital rules, services, or documents.
    """
    # Uses the Chroma 'retriever' object defined in your previous step
    docs = retriever.invoke(query)
    
    if not docs:
        return "No relevant documents found in the database."
    
    # Format the vector DB content to send back to the Gemini model
    context = "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}"
        for doc in docs
    )
    return context


APPOINTMENT_FILE = "data/aminity_hospital_appointment.txt"
@tool
def book_appointment(patient_name:str, doctor_name:str, date:str, time:str):

    """This tool is used only to book appointments. Returns Success or Failure.
    If no specific doctor is named, you should find the best possible doctor for the patient.
    Args:
        patient_name: Name of the patient.
        doctor_name: Name of the doctor.
        date: Appointment date (YYYY-MM-DD).
        time: Appointment time (HH:MM).
    """
    with open(APPOINTMENT_FILE,'r') as f:
        appointments=f.readlines()

    for appointment in appointments:
        fields=appointment.strip().split("|")

        if len(fields)<4:
            continue
        doctor=fields[1]
        booked_date=fields[2]
        booked_time=fields[3]
        if(doctor==doctor_name and booked_date==date and booked_time==time):
            return f"Doctor {doctor_name} is not available at this specified time."
    otp=random.randint(100000,999999)
    with open (APPOINTMENT_FILE,"a") as f:
        f.write(f"{patient_name}|{doctor_name}|{date}|{time}|{otp}\n")

    return f"Appointment Booked Successfully for {patient_name} with {doctor_name} on {date} at {time}. Your OTP for this booking is {otp}. Thank You."


@tool
def manage_appointment(patient_name:str, action:str, date:str, time:str, otp:int,new_date:str,new_time:str):
    """Manages Appointments. Cancel/Modify or retrieve data.
    Args:
    patient_name:name of the patient.
    action: 'cancel','modify' or 'retrieve'.
    date:Date of the appointment.
    time:time of the appointment.
    otp:one time password for that booking."""

    with open (APPOINTMENT_FILE,"r") as f:
        appointments=f.readlines()
    for appointment in appointments:
        fields=appointment.strip().split("|")
        patient=fields[0]
        booked_date=fields[2]
        booked_time=fields[3]
        one_time_password=fields[4]
        if one_time_password==otp and patient==patient_name:
            if action=="retrieve":
                return f"The details of the booking are {patient_name} with {fields[1]} on {date} at {time}."
            elif action=="cancel":
                with open(APPOINTMENT_FILE,"a")as f:

        
tools = [query_hospital_knowledgebase,book_appointment]


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key="your-api-here"
).bind_tools(tools)

def call_agent(state: AgentState) -> AgentState:
    """Calls the model with the current conversation context."""
    response = llm.invoke(state["messages"])
    # Returning a dictionary updates the state via 'add_messages'
    return {"messages": [response]}

def should_continue(state:AgentState):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph=StateGraph(AgentState)
graph.add_node("my_agent",call_agent)

tool_node=ToolNode(tools=tools)
graph.add_node("tools",tool_node)

graph.add_edge(START,"my_agent")
graph.add_conditional_edges(
    "my_agent",
    should_continue,
    {
        "continue":"tools",
        "end":END
    }

)
graph.add_edge("tools","my_agent")
app=graph.compile()

import traceback

try:
    result = app.invoke({
        "messages": [HumanMessage(content="Can you book me a appointment for a Neurosurgeon. My name is Rahul and I want this appointment on 25 July 2026 at 11:30 am.")]
    })
    print(result["messages"][-1].text)
except Exception as e:
    print("--- ERROR TRACEBACK ---")
    traceback.print_exc()