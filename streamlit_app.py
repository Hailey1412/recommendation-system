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
job_descriptions_df = pd.read_excel("Job_descriptions.xlsx")  
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
   # "Teamwork Courses": ["Q10"],
   # "Presentation Courses": ["Q11"],
    "Emotional Intelligence": ["Q12", "Q13", "Q14", "Q15"],
    "Communication": ["Q16", "Q17"],
    "Problem Solving Skills": ["Q18", "Q19"],
    "Self-management": ["Q20", "Q21"],
    "Teamwork": ["Q22", "Q23", "Q24"],
    "Professionalism": ["Q25", "Q26", "Q27"]
}

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
#sidebar_selection = st.sidebar.radio("Go to", 
   # ["Homepage", "Login / Sign up", "Profile", "Assessment", "Education Details", "Skills Results", "Career Recommendations", "Course Recommendation"],
   # index=["Homepage", "Login / Sign up", "Profile", "Assessment", "Education Details", "Skills Results", "Career Recommendations", "Course Recommendation"].index(st.session_state.page),
  #  key="sidebar_page"
#)

valid_pages = [
    "Homepage", "Login / Sign up", "Profile", "Assessment",
    "Education Details", "Skills Results", "Career Recommendations", "Course Recommendations"
]

# Use a fallback to "Homepage" if page is missing or invalid
current_page = st.session_state.get("page", "Homepage")
if current_page not in valid_pages:
    current_page = "Homepage"

index = valid_pages.index(current_page)

sidebar_selection = st.sidebar.selectbox(
    "Navigate",
    ["Homepage", "Login / Sign up", "Profile", "Assessment", "Education Details", "Skills Results", "Career Recommendations", "Course Recommendations"],
    index=index
)

if sidebar_selection != st.session_state.page:
    st.session_state.page = sidebar_selection

# Routing
if st.session_state.page == "Homepage":
    if st.session_state.page == "Homepage":
        st.markdown("""
            <style>
                .full-width-image {
                    position: relative;
                    width: 100%;
                    height: 500px;
                    background-image: url('https://uae-voice.net/wp-content/uploads/2023/09/image-2-1.jpg');
                    background-size: cover;
                    background-position: center;
                    border-radius: 10px;
                }
                .overlay-buttons {
                    position: absolute;
                    top: 60%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    text-align: center;
                    background-color: rgba(255, 255, 255, 0.85);
                    padding: 20px;
                    border-radius: 12px;
                    width: fit-content;
                }
                .overlay-buttons h1 {
                    font-size: 30px;
                    color: #003366;
                    margin-bottom: 20px;
                }
            </style>
    
            <div class="full-width-image">
                <div class="overlay-buttons">
                    <h1>Empowering UAE Youth for the Future of Work</h1>
                    <p>Discover your strengths. Choose your path.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        # Create 3 columns: left, center, right
        left_col, center_col1, center_col2, right_col = st.columns([1, 2, 2, 1])
        
        with center_col1:
            if st.button("Start as Guest"):
                st.session_state.current_user = "Guest"
                set_page("Assessment")
        with center_col2:
            if st.button("Login / Sign Up"):
                set_page("Login / Sign up")

    
    # Handle button logic using query params or manual button click detection
   # if 'guest' in st.session_state.get('button_clicked', '') or st.experimental_get_query_params().get("guest"):
     #   st.session_state.current_user = "Guest"
     #   set_page("Assessment")

  #  if 'login' in st.session_state.get('button_clicked', '') or st.experimental_get_query_params().get("login"):
     #   set_page("Login / Sign up")

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
    
elif st.session_state.page == "Assessment": #"Homepage", "Login / Sign up", "Profile", "Assessment", "Education Details", "Skills Results", "Career Recommendations", "Course Recommendation"
    st.title("Assessment")
    st.write("Let's assess your skills!")

    # Store responses in session state
    if "assessment_responses" not in st.session_state:
        st.session_state.assessment_responses = {}

    for qid, question in questions.items():
        response = st.slider(question, 1, 5, key=qid)
        st.session_state.assessment_responses[qid] = response

    if st.button("Next"):
        set_page("Education Details")

elif st.session_state.page == "Education Details": 
    st.title("Add Your Education")

    # Initialize education blocks
    if "education_blocks" not in st.session_state:
        st.session_state.education_blocks = []

    degree_options = ["High School Diploma", "Associate's", "Certification", "Bachelor's", "Master's", "PhD"]
    field_options = list(mlb_field.classes_)

    if st.button("➕ Add Education"):
        st.session_state.education_blocks.append({"degree": "", "field": ""})

    for i in range(len(st.session_state.education_blocks)):
        edu = st.session_state.education_blocks[i]
        st.markdown(f"##### Education {i+1}")
        col1, col2, col3 = st.columns([4, 4, 1])
        
        with col1:
            degree = st.selectbox(f"Select Degree {i+1}", degree_options, key=f"degree_{i}")
        with col2:
            field = None
            if degree != "High School Diploma":
                field = st.selectbox(f"Select Field of Study {i+1}", field_options, key=f"field_{i}")
        with col3:
            if st.button("X", key=f"remove_{i}"):
                st.session_state.education_blocks.pop(i)
                st.experimental_rerun()
        
        if i < len(st.session_state.education_blocks):
            st.session_state.education_blocks[i] = {"degree": degree, "field": field}

    st.markdown("---")

    if st.button("Submit Assessment"):
        # Step 1: Calculate Skill Scores
        skill_scores = {}
        for skill, q_ids in skill_groups.items():
            skill_scores[skill] = np.mean([st.session_state.assessment_responses[q] for q in q_ids])
        st.session_state.skill_scores = skill_scores

        # Step 2: Prepare Model Input
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

        # Step 3: Save Recommendations
        st.session_state.career_results = [
            {"title": job, "confidence": round(conf*100, 2), "description": job_descriptions_dict.get(job, "No description")}
            for job, conf in zip(job_titles, confidences)
        ]

        # Step 4: Save low-score skills
        st.session_state.low_skill_courses = {
            s: skill_courses[s] for s, score in skill_scores.items() if score <= 3 and s in skill_courses
        }
        st.session_state.low_q_courses = {
            q: question_courses[q]
            for q, score in st.session_state.assessment_responses.items() if score <= 3 and q in question_courses
        }

        set_page("Skills Results")

elif st.session_state.page == "Skills Results": #"Homepage", "Login / Sign up", "Profile", "Assessment", "Education Details", "Skills Results", "Career Recommendations", "Course Recommendation"
    st.title("Your Skill Assessment Results")

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
        "Decision-Making": "Decision-making involves engaging in tasks that require choosing between multiple options, analyzing risks, and selecting the most suitable course of action. This could include participating in simulations, case studies, or project-based scenarios that mirror real-world business or technical decisions.",
        "Real-life Experience": "Real-world engagement includes activities that allow students to learn about and understand available opportunities which will allow them to make informed decisions regarding their employment. It includes activities like witnessing alumni visit to talk about their career paths and available opportunities in their company. It may also include listening to employers’ seminars about employment opportunities and skills requirements for these opportunities. Additionally, it could include experiencing employer’s and companies’ participation in project presentations and program delivery.",
        "Work Based Learning": "Work-based learning is an educational strategy that provides students with real-life work experience during while they can apply their technical and academic skills. It is a major opportunity for students to develop their employability. Work-based learning activities include short-term (6-12 weeks) or long-term (full academic year) internship work placement, it also includes part-time jobs, self-employment, freelancing or volunteer work.",
        "Emotional Intelligence": "Emotional intelligence includes participating in group activities, feedback sessions, or mentorship experiences that help students understand emotional responses in themselves and others, regulate behavior in stressful situations, and build empathy and interpersonal sensitivity.",
        "Communication": "Communication skills are developed through activities such as class discussions, group projects, presentations, or report writing, which allow students to articulate their ideas clearly, adapt their message for different audiences, and engage in active listening.",
        "Problem Solving Skills": "Problem-solving is strengthened through hands-on projects, design thinking exercises, and case-based learning where students identify challenges, evaluate options, and implement innovative solutions under constraints.",
        "Self-management": "Self-management involves participating in time-sensitive assignments, goal-setting workshops, or multi-tasking activities that train students to organize workloads, meet deadlines, and maintain motivation and accountability without constant supervision.",
        "Teamwork": "Teamwork skills are fostered through collaborative projects, peer-led tasks, and group decision-making exercises where students coordinate responsibilities, resolve conflicts, and contribute toward shared goals.",
        "Professionalism": "Professionalism is demonstrated through structured interactions such as mock interviews, workplace etiquette training, or project-based work with external partners, allowing students to practice reliability, ethical behavior, and respectful communication in professional settings."
    }
    
    # Display each skill with color highlight
    for _, row in results_df.iterrows():
        skill = row["Skill"]
        score = row["Score"]
        st.markdown(
            f'<h4 style="color:#990000;margin-bottom:5px;">{skill} — {score}%</h4>'
            f'<p style="margin:0;">{skills_description.get(skill, "No description available.")}</p>',
            unsafe_allow_html=True
        ) # f'<div style="background-color:#e0f0ff;padding:10px;border-radius:8px;margin-bottom:10px">'

    st.markdown("---")
    
    # Display bar chart below the text results
    chart = (
        alt.Chart(results_df)
        .mark_bar(size=30)
        .encode(
            x=alt.X("Skill:N", sort="-y", title="Skill"),
            y=alt.Y("Score:Q", scale=alt.Scale(domain=[0, 100]), title="Score (%)"),
            color=alt.Color("Score:Q", scale=alt.Scale(range=["#f5f5dc", "#d2b48c", "#a0522d"]))
        )
        .properties(height=400, width=600)
        .configure_axis(labelFontSize=12, titleFontSize=14)
    )

    if st.button("Next"):
        set_page("Education Details")


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
        
elif st.session_state.page == "Career Recommendations":
    st.header("Top 5 Career Matches:")
    for result in st.session_state.career_results:
        st.subheader(f"**{result['title']}** ")#({result['confidence']}%)")
        st.caption(result["description"])

    col_l, col_cent1, col_cent2, col_r = st.columns([2,2,2,2])
    with col_l: 
        if st.button("Back"):
            set_page("Skills Results")
    with col_r: 
        if st.button("Next"): 
            set_page("Course Recommendations")
   

else: 
    st.title("Course Recommendations")
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

    col_l, col_cent1, col_cent2, col_r = st.columns([2,2,2,2])
    with col_l: 
        if st.button("Back"): 
            set_page("Career Recommendations")
        
        
    
        
        
            
