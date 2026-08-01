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

Sample Run Tests:-
#########################################################################################
User:-I have a very bad knee problem and I want to check if there is any specialist doctor here at the hospital?

AI Agent:-Yes, we do have a specialist for knee problems! 

**Dr. Amara Patel, MD** is the Director of Adult Reconstruction and Joint Replacement in the **Department of Orthopedic Surgery**. 
* **Specialties:** Robotic Knee and Hip Arthroplasty, and Revision Joint Replacement.
* **OPD Schedule:** Wednesdays and Fridays from 09:00 AM to 04:00 PM (Suite 202, South Wing).

Would you like me to help you book an appointment with Dr. Patel?

##########################################################################################
User:-  I have heart problem since I was 5, and my nanny used to say to visit a doctor. My name is Vaibhav and I am now 19 years old. Can you tell me when are they available and if I can book an appointment?

Agent:- Hello Vaibhav! It's great that you are taking charge of your health. 

We have specialized heart doctors (cardiologists and cardiothoracic specialists) available at our hospital. Here are the doctors who can help you with your condition and their OPD schedules:

1. **Dr. Marcus Thorne** (Cardiothoracic Surgery - Chief of Cardiothoracic Surgery / CMO)
   * **Schedule:** Mondays & Wednesdays, 09:00 AM to 01:00 PM (Suite 301, East Wing)

2. **Dr. Sophia Al Mansoor** (Interventional Cardiology - Director of Cardiac Catheterization Lab)
   * **Schedule:** Tuesdays & Thursdays, 10:00 AM to 03:00 PM (Suite 305, East Wing)

3. **Dr. David O Connor** (Pediatric Medicine & Critical Care - Specializes in Congenital Heart Anomalies)
   * **Schedule:** Mondays, Tuesdays, Wednesdays & Fridays, 10:00 AM to 04:00 PM (Children's Pavilion, Floor 1)

Would you like to book an appointment with one of these doctors? If so, please let me know your preferred doctor, date, and time!

User:-Please do Dr Marcus on 23rd july at 12:30 am.

Agent:- Vaibhav, your appointment has been successfully booked! 

Here are the details:
* **Patient Name:** Vaibhav
* **Doctor:** Dr. Marcus Thorne
* **Date:** July 23, 2024
* **Time:** 12:30 PM (Note: OPD hours are from 09:00 AM to 01:00 PM in Suite 301, East Wing)
* **Location:** Suite 301, East Wing
* **Booking OTP:** 378023 *(Please save this OTP in case you need to modify or cancel your appointment later.)*

Take care, and we look forward to seeing you!
#########################################################################################
User:- Can you cancel my appointment with Dr Marcus. My name is Vaibhav and my otp is 378023.

Agent:- Your appointment has been successfully cancelled. Let me know if you need help with anything else!
###########################################################################################
That is all from my side.

Update:- Embedded secret is the otp for patients.













