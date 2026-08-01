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
    model="gemini-embedding-001",
    api_key="your_api_key"
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
def query_hospital(query: str) -> str:
    """Useful for retrieving information from the hospital database but it strictly does not access appointments by patients.
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

    """This tool is used only to book appointments.It does not manage appointments. Returns Success or Failure.
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
        f.write(f"{otp}|{patient_name}|{doctor_name}|{date}|{time}\n")

    return f"Appointment Booked Successfully for {patient_name} with {doctor_name} on {date} at {time}. Your OTP for this booking is {otp}. Thank You."


@tool
def manage_appointment(patient_name:str, action:str, otp:int,new_date:str="",new_time:str=""):
    """This tool is strictly for managing Appointments. Cancel/Modify or retrieve data.
    Args:
    patient_name:name of the patient.
    action: 'cancel','modify' or 'retrieve'.
    otp:one time password for that booking.
    new_date:New Date of the appointment.
    new_time:New time of the appointment."""

    with open (APPOINTMENT_FILE,"r") as f:
        appointments=f.readlines()
    for appointment in appointments:
        fields=appointment.strip().split("|")
        patient=fields[1]
        booked_date=fields[3]
        booked_time=fields[4]
        one_time_password=fields[0]
        if int(one_time_password)==otp and patient==patient_name:
            if action=="retrieve":
                return f"The details of the booking are {patient_name} with {fields[2]} on {fields[3]} at {fields[4]}."
            elif action=="cancel":
                with open(APPOINTMENT_FILE,"r")as f:
                    lines=f.readlines()
                updated_lines = []
                found = False
                for line in lines:
                    cleaned_line=line.strip()
                    if not cleaned_line:
                        continue
                    fields= cleaned_line.split("|")
                    line_otp=fields[0].strip()
                    if str(line_otp)==str(otp):
                        found=True
                        continue
                    else:
                        updated_lines.append(cleaned_line)
                if not found:
                    return "No such data exist in the database. Try Again."
                formatted_output="\n\n".join(updated_lines)+"\n"
                with open (APPOINTMENT_FILE,"w") as f:
                    f.writelines(formatted_output)
                return f"Appointment for {patient_name} has been cancelled."
            elif action=="modify":
                if not (new_date or new_time):
                    return "Please provide at least a new date or new time to modify the appointment."
                with open(APPOINTMENT_FILE, "r") as f:
                    lines = f.readlines()
                updated_lines = []
                found = False
                for line in lines:
                    cleaned_line = line.strip()
                    if not cleaned_line:
                        continue
                    fields=cleaned_line.split("|")
                    print(fields[0])
                    if len(fields) < 5:
                        updated_lines.append(cleaned_line)
                        continue
                    line_otp=fields[0]
                    if str(line_otp) == str(otp):
                        found = True
                        updated_date = new_date if new_date else fields[3]
                        updated_time = new_time if new_time else fields[4]

                        modified_line=f"{line_otp}|{patient_name}|{fields[2]}|{updated_date}|{updated_time}"
                        updated_lines.append(modified_line)
                    else:
                        updated_lines.append(cleaned_line)
                if not found:
                    return f" No appointment found with otp{otp} and name {patient_name}"
                formatted_output='\n\n'.join (updated_lines)+'\n'
                with open (APPOINTMENT_FILE,"w") as f:
                    f.write(formatted_output)
                return f"Successfully updated appointment for {patient_name}."
            else:
                return "Not a valid action. Try Again."
        else:
            return "Try Again. Please check either otp or patient name."
    return "Error! Try again."
                                               
tools = [query_hospital,book_appointment,manage_appointment]


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key="your_api_key"
).bind_tools(tools)


system_prompt="You are an intelligent, empathetic and efficient AI Agent for Amenity Hospital." \
"You have three tools in your arsenel." \
"1. query_hospital(query:str):- You can use this tool to retrieve answers regarding hospital rules, visiting hours, doctors, about hospital, and many more." \
"2. manage_appointment:- you can manage appointments, cancel, modify or retrieve details of patients." \
"3. book_appointment:- you can book appointment through this tool." \
"Rules:-" \
"- For general hospital questions, always search using query_hospital." \
"-To manage an appointment, you MUST ask the user for" \
"1. Patient Name" \
"2.OTP" \
"3.Action" \
"- Do NOT run the manage_appointments tool until the user provides with pateint name and valid otp which is always 6 digits." \
"- For modification, make sure you get new date and time." \
"-Always be polite, professional , and clear."


def call_agent(state: AgentState) -> AgentState:
    """Calls the model with the current conversation context."""
    messages=list(state["messages"])
    messages=[SystemMessage(content=system_prompt)]+messages
    response = llm.invoke(state["messages"])
    # Returning a dictionary updates the state via 'add_messages'
    return {"messages": [response]}

def should_continue(state:AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("\n" + "="*40)
        print("🔧 TOOL CALL DETECTED!")
        
        for tool_call in last_message.tool_calls:
            print(f"📌 Tool Name  : {tool_call['name']}")
            print(f"⚙️ Parameters : {tool_call['args']}")
            print(f"🆔 Call ID    : {tool_call['id']}")
        print("="*40 + "\n")
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

def running_agent():
    print("\n===AMINITY AI ===")
    print("HOW MAY I HELP YOU TODAY?")
    while True:
        user_input=input("\n User:- ")
        if user_input.lower() in ["exit","quit"]:
            break
        messages=[HumanMessage(content=user_input)]
        result=app.invoke({"messages":messages})

        print("\n=====Answer=====")
        print(result["messages"][-1].text)


running_agent()