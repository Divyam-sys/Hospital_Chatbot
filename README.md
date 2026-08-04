# 🏥 Hospital Chatbot (AMINITY Hospital)

> **DevLabs Final Project Submission**  
> An intelligent real-life assistant for **AMINITY Hospital**, powered by **LangGraph** and **Google Gemini AI**.

---

## 📌 Overview

This project implements an AI-driven hospital assistant designed to manage patient queries, book and cancel appointments, and navigate hospital schedules using a **Re-Act agent graph**. 

The implementation is highly inspired by the [FreeCodeCamp LangGraph Tutorial](https://youtu.be/jGg_1h0qzaM?si=4NghvxAW8JtDqTDf).

---

## ✨ Features

* **⚡ Re-Act Agent Architecture:** Built using **LangGraph** for structured reasoning and action execution.
* **🔍 Contextual Knowledge Base:** Vectorized context from 6 static knowledge files using **LangChain Chroma** and **Gemini Embeddings**.
* **📅 Appointment Management:** Interactive booking and cancellation system using patient verification OTPs.
* **🚀 Fast & Efficient Execution:** Optimized using **Gemini-3.5-flash-lite** to maximize tokens per minute (TPM) on free-tier Google AI Studio accounts.

---

## ⚙️ Requirements & Dependencies

### Prerequisites
1. **Google GenAI API Key:** Obtain a free API key from [Google AI Studio](https://aistudio.google.com/) and replace `"your-api-key"` in the script.
2. **Directory Structure:** Ensure the `data/` directory (containing all 7 `.txt` files) is placed in the same folder as `main.py`.
3. **Internet Connection:** Stable connection required for live API calls.

### Package Installation

Run the following command in the directory where `main.py` is located:

```bash
pip install -r requirements.txt
or install the [packages individually
pip install -U langgraph
pip install langchain-core
pip install langchain-google-genai
pip install langchain-community
pip install langchain-chroma
pip install langchain-text-splitter

Sample test cases:-
1.
User:-I have a very bad knee problem and I want to check if there is any specialist doctor here at the hospital?

AI Agent:-Yes, we do have a specialist for knee problems! 

**Dr. Amara Patel, MD** is the Director of Adult Reconstruction and Joint Replacement in the **Department of Orthopedic Surgery**. 
* **Specialties:** Robotic Knee and Hip Arthroplasty, and Revision Joint Replacement.
* **OPD Schedule:** Wednesdays and Fridays from 09:00 AM to 04:00 PM (Suite 202, South Wing).

Would you like me to help you book an appointment with Dr. Patel?

2.
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

3.
User:- Can you cancel my appointment with Dr Marcus. My name is Vaibhav and my otp is 378023.

Agent:- Your appointment has been successfully cancelled. Let me know if you need help with anything else!


