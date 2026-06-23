import streamlit as st
import google.generativeai as genai

genai.configure(api_key="API KEY")
model = genai.GenerativeModel("models/gemini-2.5-flash")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.sidebar.title("AI Productivity Planner")
st.sidebar.write("Plan your day smarter with AI 😄")
st.subheader("Enter Your Daily Routine")

st.title("AI Task Scheduler")
st.write("Welcome to your AI Productivity Planner 😄")
mode = st.selectbox(
    "Choose Productivity Mode",
    ["Student Mode", "Exam Mode", "Work Mode", "Fitness Mode"],
)
wake_time = st.text_input("Wake Up Time")
sleep_time = st.text_input("Sleep Time")
fixed_tasks = st.text_area("Fixed Tasks (college/job/classes)")
flexible_tasks = st.text_area("Flexible Tasks (DSA/gym/coding/etc)")
if st.button("Generate Schedule"):
    user_prompt = f"""
    Selected productivity mode: {mode}
    FIXED CONSTRAINTS:
- Wake up time MUST be : {wake_time}
- Sleep time MUST be : {sleep_time}
- Do NOT change these timings
- Build the schedule only within these timings
    Fixed tasks:
    {fixed_tasks}
    Flexible tasks:
    {flexible_tasks}
    Strictly follow the user's wake-up and sleep times.
    Do not modify them.
    Create a balanced and productive daily schedule.

Format the output clearly with:
- time slots
- task names
- short productivity tips
- breaks where necessary
Make it visually clean and easy to read.
    """
    st.session_state.chat_history.append(f"User Request:\n{user_prompt}")
    response = model.generate_content(user_prompt)
    st.session_state.chat_history.append(f"AI Response:\n{response.text}")
    st.subheader("Your AI Generated Schedule")
    st.success("Schedule Generated Successfully!")
    st.markdown(response.text)
st.subheader("Chat With Your AI Assistant ")

chat_input = st.text_input("Ask something about your schedule/productivity")
if st.button("Send"):
    chat_prompt = f"""
    You are a friendly productivity assistant.

    Previous schedule and context:
    {st.session_state.chat_history}

    User message:
    {chat_input}

    Respond conversationally and helpfully.
    """

    chat_response = model.generate_content(chat_prompt)

    st.markdown(chat_response.text)
