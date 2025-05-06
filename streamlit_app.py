import streamlit as st
import pandas as pd
import os
import numpy as np
import joblib
import altair as alt


#Load the AI models for the career recommendation
model = joblib.load("best_model1.pkl")
mlb_degree = joblib.load("mlb_degree1.pkl")
mlb_field = joblib.load("mlb_field1.pkl")
le = joblib.load("label_encoder1.pkl")

# Load the job descriptions
job_descriptions_df = pd.read_excel("Job_descriptions.xlsx")  # <-- Adjust the path if needed
job_descriptions_dict = dict(zip(job_descriptions_df["Job Title"], job_descriptions_df["Description"]))

# Skill order for model input
model_skill_order = [
    "Decision-Making",
    "Emotional Intelligence",
    "Real-life Experience",
    "Communication",
    "Self-management",
    "Teamwork",
    "Professionalism"
]

questions = {
    "Q1": "I have self-awareness of my skills and track progress towards goals",
    "Q2": "I reflect on and assess myself on acquired learning experiences",
    "Q3": "I seek new opportunities and review available options",
    "Q4": "I have a clear vision of my career path and long-term goals",
    "Q5": "I have attended alumni talks about career paths",
    "Q6": "I have attended employer seminars on job opportunities and skills",
    "Q7": "I have experienced employer participation in academic projects",
    "Q8": "I have gained work experience through internships or placements",
    "Q9": "I understand workplace structures and practices",
    "Q10": "My degree offered many teamwork opportunities",
    "Q11": "I gave many presentations during my degree",
    "Q12": "I recognize my emotions in real time",
    "Q13": "I read others' emotions through voice and facial expressions",
    "Q14": "I control my emotions well",
    "Q15": "I help people feel better when they are down",
    "Q16": "I ask questions or seek help when needed",
    "Q17": "I communicate my ideas clearly and confidently",
    "Q18": "I identify problems and find multiple solutions",
    "Q19": "I consider others and consequences in decision-making",
    "Q20": "I prioritize my time effectively",
    "Q21": "Deadlines motivate me to stay focused",
    "Q22": "I keep teams engaged and communicate regularly",
    "Q23": "I value diversity of opinions in teams",
    "Q24": "I contribute actively and complete my group tasks",
    "Q25": "I apply feedback to improve future work",
    "Q26": "I handle sensitive info with confidentiality",
    "Q27": "I adapt my attitude and behavior to situations"
}  # (existing 27 questions dictionary here)

#Define skills and questions
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

skills_description = {
    "Decision-Making": "Decision-making is... ",
    "Real-life Experience": "It is...",
    "Work Based Learning": "It is...",
    "Teamwork Courses": "It is...",
    "Presentation Courses": "It is...",
    "Emotional Intelligence": "It is...",
    "Communication": "It is...",
    "Problem Solving Skills": "It is...",
    "Self-management": "It is...",
    "Teamwork": "It is...",
    "Professionalism": "It is..."}

skill_courses = {
    "Decision-Making": "https://www.edx.org/course/critical-thinking-problem-solving",
    "Emotional Intelligence": "https://www.linkedin.com/learning/developing-your-emotional-intelligence",
    "Real-life Experience": "https://www.coursera.org/learn/experiential-learning",
    "Communication": "https://www.coursera.org/learn/successful-communication",
    "Self-management": "https://www.linkedin.com/learning/time-management-fundamentals",
    "Teamwork": "https://www.coursera.org/learn/teamwork-skills",
    "Professionalism": "https://www.edx.org/course/professional-skills-for-the-workplace"
}   # (your skill_courses dictionary)
question_courses = {
    "Q1": "https://www.coursera.org/specializations/career-success",
    "Q2": "https://www.coursera.org/specializations/career-success",
    "Q3": "https://www.coursera.org/specializations/career-success",
    "Q4": "https://www.coursera.org/specializations/career-success",
    "Q5": "https://www.edx.org/course/networking-and-mentorship",
    "Q6": "https://www.edx.org/course/networking-and-mentorship",
    "Q7": "https://www.edx.org/course/networking-and-mentorship",
    "Q8": "https://www.coursera.org/learn/internship-career-preparation",
    "Q9": "https://www.coursera.org/learn/internship-career-preparation",
    "Q10": "https://www.futurelearn.com/courses/collaborative-working-in-a-remote-team",
    "Q11": "https://www.edx.org/course/effective-presentation-and-communication-skills",
    "Q12": "https://www.futurelearn.com/courses/emotional-intelligence-at-work",
    "Q13": "https://www.futurelearn.com/courses/emotional-intelligence-at-work",
    "Q14": "https://www.futurelearn.com/courses/emotional-intelligence-at-work",
    "Q15": "https://www.futurelearn.com/courses/emotional-intelligence-at-work",
    "Q16": "https://www.edx.org/course/communication-skills-for-bridging-divides",
    "Q17": "https://www.edx.org/course/communication-skills-for-bridging-divides",
    "Q18": "https://www.coursera.org/learn/creative-problem-solving",
    "Q19": "https://www.coursera.org/learn/creative-problem-solving",
    "Q20": "https://www.coursera.org/learn/work-smarter-not-harder",
    "Q21": "https://www.coursera.org/learn/work-smarter-not-harder",
    "Q22": "https://www.coursera.org/learn/teamwork-skills",
    "Q23": "https://www.coursera.org/learn/teamwork-skills",
    "Q24": "https://www.coursera.org/learn/teamwork-skills",
    "Q25": "https://www.edx.org/course/professional-skills-for-the-workplace",
    "Q26": "https://www.edx.org/course/professional-skills-for-the-workplace",
    "Q27": "https://www.edx.org/course/professional-skills-for-the-workplace"
}  # (your question_courses dictionary)


# File to store users
USER_CSV = "users.csv"

# Load or create user data
if os.path.exists(USER_CSV):
    users_df = pd.read_csv(USER_CSV)
else:
    users_df = pd.DataFrame(columns=["username"])
    users_df.to_csv(USER_CSV, index=False)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Homepage"
if "education_blocks" not in st.session_state:
    st.session_state.education_blocks = []
if 'skill_scores' not in st.session_state:
    st.session_state.skill_scores = {}
if 'career_results' not in st.session_state:
    st.session_state.career_results = []
if 'course_progress' not in st.session_state:
    st.session_state.course_progress = {}

def set_page(selected):
    st.session_state.page = selected

# Sidebar navigation
st.sidebar.title("Navigation")
sidebar_selection = st.sidebar.radio("Go to", 
    ["Homepage", "Login / Sign up", "Profile", "Assessment", "Recommendations"],
    index=["Homepage", "Login / Sign up", "Profile", "Assessment", "Recommendations"].index(st.session_state.page),
    key="sidebar_page"
)

if sidebar_selection != st.session_state.page:
    st.session_state.page = sidebar_selection

# Routing
if st.session_state.page == "Homepage":
    st.title("Empowering UAE Youth for the Future of Work")
    st.subheader("Discover your strengths. Choose your path.")
    st.markdown("""
    We have created a personalized AI-powered platform designed to help youth in the UAE discover their strengths, explore careers, and find courses to grow.  
    Take our skills-based assessment and receive career and course recommendations tailored to your profile.
    """)
    st.markdown("#### Skills →  Assessment → Career →  Courses")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start as Guest"):
            st.session_state.current_user = "Guest"
            set_page("Assessment")
    with col2:
        if st.button("Login / Sign Up"):
            set_page("Login / Sign up")

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
                set_page("Assessment")

    elif auth_mode == "Log In":
        if st.button("Log In"):
            if username.strip() == "":
                st.warning("Please enter a username.")
            elif username in users_df["username"].values:
                st.session_state.current_user = username
                st.success(f"Welcome back, {username}!")
                set_page("Assessment")
            else:
                st.error("User not found. Please sign up first.")
    
elif st.session_state.page == "Assessment":
    st.title("Assessment")
    st.write("Let's assess your skills!")

    # Store responses in session state
    if "assessment_responses" not in st.session_state:
        st.session_state.assessment_responses = {}

    for qid, question in questions.items():
        response = st.slider(question, 1, 5, key=qid)
        st.session_state.assessment_responses[qid] = response

    # Ask for education info
    st.header("🎓 2. Add Your Education")
    
    degree_options = ["High School Diploma", "Associate's", "Certification", "Bachelor's", "Master's", "PhD"]
    field_options = list(mlb_field.classes_)
    
    # Add Education Entry Button
    if st.button("➕ Add Education"):
        st.session_state.education_blocks.append({"degree": "", "field": ""})
    
    # Display Education Inputs
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
    
        # Update session state
        if i < len(st.session_state.education_blocks):
            st.session_state.education_blocks[i] = {"degree": degree, "field": field}
    
    st.markdown("---")
    
    # Submit Button
    if st.button("✅ Submit Assessment"):
        # Skill averaging
        skill_scores = {}
        for skill, q_ids in skill_groups.items():
            skill_scores[skill] = np.mean([st.session_state.assessment_responses[q] for q in q_ids])

        st.session_state.skill_scores = skill_scores

        # Prepare model input
        skill_input = [skill_scores[skill] for skill in model_skill_order]
        degrees = [edu["degree"] for edu in st.session_state.education_blocks]
        fields = [edu["field"] for edu in st.session_state.education_blocks]
        degree_encoded = mlb_degree.transform([degrees])
        field_encoded = mlb_field.transform([fields])

        final_input = np.hstack([skill_input, degree_encoded[0], field_encoded[0]])
        predictions = model.predict_proba([final_input])[0]
        top5_idx = predictions.argsort()[-5:][::-1]
        job_titles = le.inverse_transform(top5_idx)
        confidences = predictions[top5_idx]

        st.session_state.career_results = [
            {"title": job, "confidence": round(conf*100, 2), "description": job_descriptions_dict.get(job, "No description")}
            for job, conf in zip(job_titles, confidences)
        ]

        # Prepare low-score skills and questions
        low_skill_courses = {s: skill_courses[s] for s, score in skill_scores.items() if score <= 3 and s in skill_courses}
        low_q_courses = {
            q: question_courses[q]
            for q, score in st.session_state.assessment_responses.items() if score <= 3 and q in question_courses
        }
        st.session_state.low_skill_courses = low_skill_courses
        st.session_state.low_q_courses = low_q_courses

        set_page("Recommendations")


elif st.session_state.page == "Recommendations":
    st.title("Career & Skill Recommendations")

    st.header("Your Skill Assessment Results:")

# Convert scores to percentage and sort
results_df = pd.DataFrame({
    "Skill": list(st.session_state.skill_scores.keys()),
    "Score": [round(score * 20, 2) for score in st.session_state.skill_scores.values()]  # out of 100%
})
results_df.sort_values(by="Score", ascending=False, inplace=True)

# Summary sentence
sorted_skills = results_df["Skill"].tolist()
st.markdown(
    f"According to your input in the assessment and education details, your skills from strongest to weakest are: "
    f"**{', '.join(sorted_skills)}**."
)

# Skill descriptions
skills_description = {
    "Decision-Making": "Decision-making is the ability to choose between alternatives and make sound judgments.",
    "Real-life Experience": "This refers to your practical exposure and application of knowledge in real situations.",
    "Work Based Learning": "It is a learning approach where students gain skills through real work environments.",
    "Teamwork Courses": "These enhance collaboration and cooperation through structured learning experiences.",
    "Presentation Courses": "These focus on improving public speaking and visual communication skills.",
    "Emotional Intelligence": "This is your ability to understand and manage your emotions and those of others.",
    "Communication": "This refers to your ability to clearly express ideas and understand others.",
    "Problem Solving Skills": "Your ability to identify issues, analyze situations, and find effective solutions.",
    "Self-management": "Your capability to manage your time, tasks, and responsibilities efficiently.",
    "Teamwork": "Your effectiveness in working within groups to achieve shared goals.",
    "Professionalism": "Your demonstration of ethical behavior, responsibility, and workplace etiquette."
}

# Display each skill with color highlight
for _, row in results_df.iterrows():
    skill = row["Skill"]
    score = row["Score"]
    st.markdown(
        f'<div style="background-color:#e0f0ff;padding:10px;border-radius:8px;margin-bottom:10px">'
        f'<h4 style="color:#0066cc;margin-bottom:5px;">{skill} — {score}%</h4>'
        f'<p style="margin:0;">{skills_description.get(skill, "No description available.")}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    
    
    
    # Display text results on top
    with st.expander("See Detailed Scores"):
        for skill, score in st.session_state.skill_scores.items():
            st.write(f"**{skill}**: {round(score, 2)}")
    
    # Display bar chart below the text results
    chart = (
        alt.Chart(results_df)
        .mark_bar(size=30)
        .encode(
            x=alt.X("Skill:N", sort="-y", title="Skill"),
            y=alt.Y("Score:Q", scale=alt.Scale(domain=[0, 5]), title="Score"),
            color=alt.Color("Score:Q", scale=alt.Scale(scheme="blues"))
        )
        .properties(height=400, width=600)  # Bigger horizontal chart
        .configure_axis(labelFontSize=12, titleFontSize=14)
    )
    
    st.altair_chart(chart, use_container_width=True)
   
    st.header("Top 5 Career Matches:")
    for result in st.session_state.career_results:
        st.subheader(f"**{result['title']}** ")#({result['confidence']}%)")
        st.caption(result["description"])

    st.subheader("Skill-Based Course Recommendations")

    for skill, url in st.session_state.low_skill_courses.items():
        st.markdown(f"###### {skill} Course: ({url})")


    with st.expander("More Personlized Course Recommendations"):
        for qid, url in st.session_state.low_q_courses.items():
            st.markdown(f"**{questions[qid]}**: [Course Link]({url})")

    if st.session_state.current_user == "Guest":
        if st.button("💾 Save Results by Signing Up"):
            set_page("Login / Sign up")
    else:
        st.success("Your results are saved to your profile!")
    
elif st.session_state.page == "Profile":
    if st.session_state.current_user == "Guest":
        st.warning("You must log in to access the profile page.")
    else:
        st.title(f"Hi {st.session_state.current_user}")
        st.markdown("Welcome to your profile, where you can check your results and progress.")
        
        # Saved Skill Scores
        st.subheader("Saved Skill Scores:")
        for skill, score in st.session_state.skill_scores.items():
            st.write(f"**{skill}**: {round(score, 2)}")
        
        # Career Recommendations with notes
        st.subheader("Career Recommendations:")
        for i, result in enumerate(st.session_state.career_results):
            st.markdown(f"### {result['title']} ({result['confidence']}%)")
            st.caption(result["description"])
            user_note_key = f"{st.session_state.current_user}_note_{i}"
            note = st.text_area(f"Your thoughts about {result['title']}:", key=user_note_key)
            st.session_state[f"note_{result['title']}"] = note
        
        # Course Progress with checkboxes and a progress bar
        st.subheader("Your Course Progress:")
        completed = 0
        total = len(st.session_state.low_skill_courses)
        
        for skill, url in st.session_state.low_skill_courses.items():
            key = f"{st.session_state.current_user}_{skill}"
            completed_course = st.checkbox(f"{skill} Course", key=key, value=st.session_state.course_progress.get(key, False))
            st.session_state.course_progress[key] = completed_course
            if completed_course:
                completed += 1
            st.markdown(f"[Go to Course]({url})")
        
        # Show progress bar
        progress_ratio = completed / total if total > 0 else 0
        st.progress(progress_ratio)
        st.markdown(f"**Progress: {completed}/{total} courses completed**")
        
        
            
