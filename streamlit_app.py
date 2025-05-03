import streamlit as st
import pandas as pd
import os
import numpy as np
import joblib
import altair as alt

# Load data

# Dataset with job info
df = pd.read_csv("Data_job-skills-degree.csv")

# Load models and encoders
model = joblib.load("best_model1.pkl")
mlb_degree = joblib.load("mlb_degree1.pkl")
mlb_field = joblib.load("mlb_field1.pkl")
le = joblib.load("label_encoder1.pkl")

# Load job descriptions
job_descriptions_df = pd.read_excel("Job_descriptions.xlsx")
job_descriptions_dict = dict(zip(job_descriptions_df["Job Title"], job_descriptions_df["Description"]))

# Skill and question mapping
model_skill_order = [
    "Decision-Making", "Emotional Intelligence", "Real-life Experience",
    "Communication", "Self-management", "Teamwork", "Professionalism"
]

questions = {"Q1": "I have self-awareness of my skills and track progress towards goals", ...}  # Add all 27 Qs here

skill_groups = {
    "Decision-Making": ["Q1", "Q2", "Q3", "Q4"],
    "Real-life Experience": ["Q5", "Q6", "Q7"],
    "Work Based Learning": ["Q8", "Q9"],
    "Teamwork Courses": ["Q10"],
    "Presentation Courses": ["Q11"],
    "Emotional Intelligence": ["Q12", "Q13", "Q14", "Q15"],
    "Communication": ["Q16", "Q17"],
    "Problem Solving Skills": ["Q18", "Q19"],
    "Self-management": ["Q20", "Q21"],
    "Teamwork": ["Q22", "Q23", "Q24"],
    "Professionalism": ["Q25", "Q26", "Q27"]
}

skill_courses = {"Decision-Making": "https://...", ...}  # Add actual links
question_courses = {"Q1": "https://...", ...}  # Add actual links

# User storage
USER_CSV = "users.csv"
if os.path.exists(USER_CSV):
    users_df = pd.read_csv(USER_CSV)
else:
    users_df = pd.DataFrame(columns=["username"])
    users_df.to_csv(USER_CSV, index=False)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Homepage"
if "education_blocks" not in st.session_state:
    st.session_state.education_blocks = []

def set_page(selected):
    st.session_state.page = selected

# Sidebar navigation
st.sidebar.title("Navigation")
sidebar_selection = st.sidebar.radio("Go to", ["Homepage", "Login / Sign up", "Profile", "Assessment", "Recommendations"], index=["Homepage", "Login / Sign up", "Profile", "Assessment", "Recommendations"].index(st.session_state.page), key="sidebar_page")

if sidebar_selection != st.session_state.page:
    st.session_state.page = sidebar_selection

# Homepage
if st.session_state.page == "Homepage":
    st.title("Empowering UAE Youth for the Future of Work")
    st.subheader("Discover your strengths. Choose your path.")
    st.markdown("""
    We have created a personalized AI-powered platform designed to help youth in the UAE discover their strengths, explore careers, and find courses to grow.  
    Take our skills-based assessment and receive career and course recommendations tailored to your profile.
    """)
    st.markdown("#### 🧠 Skills → 📝 Assessment → 💼 Career → 🎓 Courses")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start as Guest"):
            st.session_state.current_user = "Guest"
            set_page("Assessment")
    with col2:
        if st.button("Login / Sign Up"):
            set_page("Login / Sign up")

# Login / Sign up
elif st.session_state.page == "Login / Sign up":
    st.title("Login / Sign Up")
    auth_mode = st.radio("Choose an option:", ["Sign Up", "Log In"], horizontal=True)
    username = st.text_input("Enter your username:")
    if auth_mode == "Sign Up":
        if st.button("Create Account"):
            if username.strip() == "":
                st.warning("Username cannot be empty.")
            elif username in users_df["username"].values:
                st.error("Username already exists. Try another one.")
            else:
                new_user = pd.DataFrame([[username]], columns=["username"])
                users_df = pd.concat([users_df, new_user], ignore_index=True)
                users_df.to_csv(USER_CSV, index=False)
                st.session_state.current_user = username
                st.success(f"Welcome, {username}! Your account has been created.")
                set_page("Profile")
    elif auth_mode == "Log In":
        if st.button("Log In"):
            if username.strip() == "":
                st.warning("Please enter a username.")
            elif username in users_df["username"].values:
                st.session_state.current_user = username
                st.success(f"Welcome back, {username}!")
                set_page("Profile")
            else:
                st.error("User not found. Please sign up first.")

# Assessment Page
elif st.session_state.page == "Assessment":
    st.title("Assessment")
    st.write("Let's assess your skills!")
    if "assessment_responses" not in st.session_state:
        st.session_state.assessment_responses = {}
    for qid, question in questions.items():
        response = st.slider(question, 1, 5, key=qid)
        st.session_state.assessment_responses[qid] = response

    st.header("🎓 2. Add Your Education")
    degree_options = ["High School Diploma", "Associate's", "Certification", "Bachelor's", "Master's", "PhD"]
    field_options = list(mlb_field.classes_)
    if st.button("➕ Add Education"):
        st.session_state.education_blocks.append({"degree": "", "field": ""})
    for i in range(len(st.session_state.education_blocks)):
        edu = st.session_state.education_blocks[i]
        st.markdown(f"##### 🎓 Education {i+1}")
        col1, col2, col3 = st.columns([4, 4, 1])
        with col1:
            degree = st.selectbox(f"Select Degree {i+1}", degree_options, key=f"degree_{i}")
        with col2:
            if degree != "High School Diploma":
                field = st.selectbox(f"Select Field of Study {i+1}", field_options, key=f"field_{i}")
            else:
                field = None
        with col3:
            remove = st.button("X", key=f"remove_{i}")
            if remove:
                st.session_state.education_blocks.pop(i)
        if i < len(st.session_state.education_blocks):
            st.session_state.education_blocks[i] = {"degree": degree, "field": field}

    st.markdown("---")
    if st.button("Submit Assessment"):
        if not st.session_state.education_blocks:
            st.error("❗ Please add at least one education entry.")
            st.stop()
        user_degrees = list({edu["degree"] for edu in st.session_state.education_blocks})
        user_fields = list({edu["field"] for edu in st.session_state.education_blocks if edu["field"]})
        st.success("Assessment submitted successfully!")

        st.write("Your responses:")
        st.write(st.session_state.assessment_responses)

        skill_scores = {}
        for skill, qid_list in skill_groups.items():
            values = [st.session_state.assessment_responses[qid] for qid in qid_list if qid in st.session_state.assessment_responses]
            skill_scores[skill] = round(np.mean(values), 2) if values else None

        st.subheader("Your Skill Assessment Results:")
        skill_df = pd.DataFrame(skill_scores.items(), columns=["Skill", "Average Score"])
        st.dataframe(skill_df)

        st.session_state.user_skills_vector = [skill_scores[skill] for skill in model_skill_order]
        st.session_state.user_degrees = user_degrees
        st.session_state.user_fields = user_fields
        set_page("Recommendations")
