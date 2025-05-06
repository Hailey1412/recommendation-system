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
    "Emotional Intelligence": ["Q12", "Q13", "Q14", "Q15"],
    "Communication": ["Q16", "Q17"],
    "Problem Solving Skills": ["Q18", "Q19"],
    "Self-management": ["Q20", "Q21"],
    "Teamwork": ["Q22", "Q23", "Q24"],
    "Professionalism": ["Q25", "Q26", "Q27"]
}

skill_courses = {
    "Decision-Making": "https://www.edx.org/learn/critical-thinking-skills/rochester-institute-of-technology-critical-thinking-problem-solving?utm_source=chatgpt.com",
    "Emotional Intelligence": "https://www.linkedin.com/learning/developing-your-emotional-intelligence",
    "Real-life Experience": "https://www.coursera.org/specializations/introduction-to-learning-experience-design?utm_source=chatgpt.com",
    "Communication": "https://www.coursera.org/learn/wharton-communication-skills?utm_source=chatgpt.com",
    "Self-management": "https://www.linkedin.com/learning/time-management-fundamentals",
    "Teamwork": "https://www.coursera.org/learn/teamwork-skills-effective-communication?utm_source=chatgpt.com",
    "Professionalism": "https://www.edx.org/certificates/professional-certificate/fullbridgex-skills-for-success?utm_source=chatgpt.com"
}   # (your skill_courses dictionary)

courses_names = {
    "The Self-Awareness Journey": "https://theselfawarenessjourney.com/courses/tsaj",
    "Reflection for Experiential Learning – Boston University": "https://www.bu.edu/ctl/ctl_resource/reflection-for-experiential-learning/",
    "Career Planning: A Pathway to Employment – Coursera": "https://www.coursera.org/learn/career-planning",
    "Career Planning Channel – Skillsoft": "https://www.skillsoft.com/channel/career-planning-3c623b30-e71c-11e6-9835-f723b46a2688",
    "Arqus Alumni Talks Series": "https://arqus-alliance.eu/news/arqus-alumni-talks/",
    "SHRM Employer Seminars": "https://www.shrm.org/events-education/education/seminars",
    "Networking and Mentorship – edX": "https://www.edx.org/course/networking-and-mentorship",
    "Employer-Driven Academic Projects Guide – Qollabb": "https://blog.qollabb.com/2025-guide-employer-driven-academic-projects/",
    "Organizational Structure Courses – Coursera": "https://www.coursera.org/courses?query=organizational%20structure",
    "Improve Your Teamwork Skills – LinkedIn Learning": "https://www.linkedin.com/learning/paths/improve-your-teamwork-skills?u=2133116",
    "Presentation Skills Training – Udemy": "https://www.udemy.com/topic/presentation-skills/?srsltid=AfmBOoqD8aAe2Lt4buVBW23bE5LUpKzdwGsmtTKu9NSOilgRr1YZZs5B",
    "Emotional Awareness and Control – Udemy": "https://www.udemy.com/course/awareness-and-emotional-control/?srsltid=AfmBOoormOPq1z4tsNpMYtJB9QjufF0fxs9J7QWR5L2CCTGBJ38IOmZb&couponCode=ST6MT60525G1",
    "Micro Expressions Training Tools – Paul Ekman": "https://www.paulekman.com/micro-expressions-training-tools/",
    "Managing Emotions in Times of Uncertainty & Stress – Coursera": "https://www.coursera.org/learn/managing-emotions-uncertainty-stress",
    "Supporting Others – Center for Emotional Education": "https://www.centerforemotionaleducation.com/supporting-others-1",
    "Teaching Students to Ask Their Own Questions – Harvard": "https://www.gse.harvard.edu/professional-education/program/teaching-students-ask-their-own-questions-best-practices-question",
    "Communication Skills Courses – Coursera": "https://www.coursera.org/courses?query=communication%20skills",
    "Creative Problem Solving – Coursera": "https://www.coursera.org/learn/problem-solving",
    "Work Smarter, Not Harder: Time Management for Personal & Professional Productivity – Coursera": "https://www.coursera.org/learn/work-smarter-not-harder",
    "Time Management Fundamentals – LinkedIn Learning": "https://www.linkedin.com/learning/time-management-fundamentals/welcome?u=2133116",
    "Teamwork Skills: Communicating Effectively in Groups – Coursera": "https://www.coursera.org/learn/teamwork-skills-effective-communication",
    "Inclusive Leadership for a Diverse Workplace – Harvard": "https://pll.harvard.edu/subject/workplace-culture",
    "Essentials of Team Collaboration – LinkedIn Learning": "https://www.linkedin.com/learning/essentials-of-team-collaboration/welcome-to-essentials-of-team-collaboration?u=2133116",
    "Giving and Receiving Feedback – Coursera": "https://www.coursera.org/learn/feedback",
    "Communication in the 21st Century Workplace – Coursera": "https://www.coursera.org/learn/communication-in-the-workplace",
    "Adaptability and Resiliency – Coursera": "https://www.coursera.org/learn/adaptability-and-resiliency"
}

question_courses = {
    "Q1": "https://theselfawarenessjourney.com/courses/tsaj",
    "Q2": "https://www.bu.edu/ctl/ctl_resource/reflection-for-experiential-learning/",
    "Q3": "https://www.coursera.org/learn/career-planning",
    "Q4": "https://www.skillsoft.com/channel/career-planning-3c623b30-e71c-11e6-9835-f723b46a2688",
    "Q5": "https://arqus-alliance.eu/news/arqus-alumni-talks/",
    "Q6": "https://www.shrm.org/events-education/education/seminars",
    "Q7": "https://www.edx.org/course/networking-and-mentorship",
    "Q8": "https://blog.qollabb.com/2025-guide-employer-driven-academic-projects/",
    "Q9": "https://www.coursera.org/courses?query=organizational%20structure",
    "Q10": "https://www.linkedin.com/learning/paths/improve-your-teamwork-skills?u=2133116",
    "Q11": "https://www.udemy.com/topic/presentation-skills/?srsltid=AfmBOoqD8aAe2Lt4buVBW23bE5LUpKzdwGsmtTKu9NSOilgRr1YZZs5B",
    "Q12": "https://www.udemy.com/course/awareness-and-emotional-control/?srsltid=AfmBOoormOPq1z4tsNpMYtJB9QjufF0fxs9J7QWR5L2CCTGBJ38IOmZb&couponCode=ST6MT60525G1",
    "Q13": "https://www.paulekman.com/micro-expressions-training-tools/",
    "Q14": "https://www.coursera.org/learn/managing-emotions-uncertainty-stress",
    "Q15": "https://www.centerforemotionaleducation.com/supporting-others-1",
    "Q16": "https://www.gse.harvard.edu/professional-education/program/teaching-students-ask-their-own-questions-best-practices-question",
    "Q17": "https://www.coursera.org/courses?query=communication%20skills",
    "Q18": "https://www.coursera.org/learn/problem-solving",
    "Q19": "https://www.coursera.org/learn/problem-solving",
    "Q20": "https://www.coursera.org/learn/work-smarter-not-harder",
    "Q21": "https://www.linkedin.com/learning/time-management-fundamentals/welcome?u=2133116",
    "Q22": "https://www.coursera.org/learn/teamwork-skills-effective-communication",
    "Q23": "https://pll.harvard.edu/subject/workplace-culture",
    "Q24": "https://www.linkedin.com/learning/essentials-of-team-collaboration/welcome-to-essentials-of-team-collaboration?u=2133116",
    "Q25": "https://www.coursera.org/learn/feedback",
    "Q26": "https://www.coursera.org/learn/communication-in-the-workplace",
    "Q27": "https://www.coursera.org/learn/adaptability-and-resiliency"
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
    st.title("Skills Assessment")
    st.subheader("Let's assess your skills!")
    
    # Store responses in session state
    if "assessment_responses" not in st.session_state:
        st.session_state.assessment_responses = {}
    
    for qid, question in questions.items():
        st.markdown(
            f"<p style='font-size:18px; font-weight:500; margin-bottom:5px;'>{question}</p>",
            unsafe_allow_html=True
        )
        response = st.slider("", 1, 5, key=qid)  # Empty string disables default label
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
    st.markdown("#### According to your input in the assessment and education details, your skills from strongest to weakest are: "
    )#  f"**{', '.join(sorted_skills)}**."
    
    # Skill descriptions
    skills_description = {
        "Decision-Making": "Decision-making involves engaging in tasks that require choosing between multiple options, analyzing risks, and selecting the most suitable course of action. This could include participating in simulations, case studies, or project-based scenarios that mirror real-world business or technical decisions.",
        "Real-life Experience": "Real-world engagement includes activities that expose students to employment opportunities, helping them make informed career choices. These include alumni talks, employer seminars, and company involvement in student projects and programs.",
        "Work Based Learning": "Work-based learning gives students hands-on experience where they apply academic and technical skills. This includes internships, part-time jobs, self-employment, freelancing, and volunteer work.",
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
            color=alt.Color("Score:Q", scale=alt.Scale(range=["#f5f5dc", "#d2b48c", "#a0522d", "#990000"]))
        )
        .properties(height=400, width=600)
        .configure_axis(labelFontSize=12, titleFontSize=14)
    )

    st.altair_chart(chart, use_container_width=True)

    if st.button("Next"):
        set_page("Career Recommendations")


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
        st.markdown(
            f"<h4 style='color:#990000; font-weight:600;'>{result['title']} ({result['confidence']}%)</h4>",
            unsafe_allow_html=True
        )
        st.caption(result["description"])

    col_l, col_cent1, col_cent2, col_r = st.columns([2, 2, 2, 2])
    with col_l: 
        if st.button("Back"):
            set_page("Skills Results")
    with col_r: 
        if st.button("Next"): 
            set_page("Course Recommendations")

   

else:  
    st.title("🎓 Course Recommendations")
    st.markdown("<h3 style='color:#990000;'>Skill-Based Suggestions</h3>", unsafe_allow_html=True)
    
    # Display low-score skill-based course recommendations
    for skill, url in st.session_state.low_skill_courses.items():
        st.markdown(
        f"""
        <div style='margin-bottom:15px; padding:10px; background-color:#f9f9f9; border-left:5px solid #990000; border-radius:5px;'>
            <p style='margin:0;'><strong style='color:#990000;'>{skill}</strong></p>
            <a href="{url}" target="_blank" style='text-decoration:none; color:#000;'>🔗 View Recommended Course</a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Divider between sections
    st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)
    st.write(assessment_responses)
    st.write(assessment_results)
    
    st.markdown("<h4 style='color:#990000;'>More Personalized Courses Recommendations:</h4>", unsafe_allow_html=True)
    with st.expander("More Courses"):
        low_scores = {course: score for course, score in assessment_results.items() if score <= 3}
        if low_scores:
            for course, score in low_scores.items():
                course_url = questions_urls.get(course, "#")
                st.markdown(f"- [{course}]({course_url})")
        else:
            st.success("Great job! You scored above 3 in all courses.")
    
        
    # Account-based saving
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.current_user == "Guest":
        if st.button("Save Results by Signing Up"):
            set_page("Login / Sign up")
    else:
        st.success("✅ Your results are saved to your profile!")
    
    # Navigation
    col_l, _, _, col_r = st.columns([2, 1, 1, 2])
    with col_l: 
        if st.button("⬅️ Back"):
            set_page("Career Recommendations")

        
    
        
        
            
