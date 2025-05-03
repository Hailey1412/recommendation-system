import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Load models and encoders
model = joblib.load("/Users/m202109833/Desktop/Py-environment/streamlit try/model/best_model.pkl")
mlb_degree = joblib.load("/Users/m202109833/Desktop/Py-environment/streamlit try/model//mlb_degree.pkl")
mlb_field = joblib.load("/Users/m202109833/Desktop/Py-environment/streamlit try/model/mlb_field.pkl")
le = joblib.load("/Users/m202109833/Desktop/Py-environment/streamlit try/model/label_encoder.pkl")


# 2.5. Load the job descriptions
job_descriptions_df = pd.read_excel("/Users/m202109833/Desktop/Py-environment/capstone-code/Job_descriptions.xlsx")  # <-- Adjust the path if needed
job_descriptions_dict = dict(zip(job_descriptions_df["Job Title"], job_descriptions_df["Description"]))


# 2. Define skills and questions
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
}  # (your existing 27 questions dictionary here)

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

 # --- STREAMLIT APP ---

st.title("Career Path and Skill Recommendation Assessment")

st.header("📝 1. Complete the Assessment")

# Initialize session state
if "assessment_done" not in st.session_state:
    st.session_state.assessment_done = False
if "education_blocks" not in st.session_state:
    st.session_state.education_blocks = []

responses = {}
with st.form(key='assessment_form'):
    for q, text in questions.items():
        responses[q] = st.slider(text, 1, 5, 3)
    submitted = st.form_submit_button("Submit Assessment")

if submitted:
    st.session_state.responses = responses
    st.session_state.assessment_done = True

# Only move to education AFTER assessment is done
if st.session_state.assessment_done:

    # 1. Calculate skills
    skill_averages = {}
    for skill, qs in skill_groups.items():
        avg = np.mean([st.session_state.responses[q] for q in qs])
        skill_averages[skill] = round(avg, 2)

    st.success("✅ Assessment Submitted!")

    # 2. Show skills
    st.subheader("📊 Your Skill Scores (11 Skills)")
    for skill, avg in skill_averages.items():
        st.write(f"**{skill}**: {avg}")

    # 3. Prepare model input
    model_skills_input = [skill_averages[s] for s in model_skill_order]

    st.header("🎓 2. Add Your Education")

    degree_options = list(mlb_degree.classes_)
    field_options = list(mlb_field.classes_)

    # Add Education Entry Button
    if st.button("➕ Add Education"):
        st.session_state.education_blocks.append({"degree": "", "field": ""})

    # Display Education Inputs
    for i, edu in enumerate(st.session_state.education_blocks):
        st.markdown(f"##### 🎓 Education {i+1}")
        degree = st.selectbox(f"Select Degree {i+1}", degree_options, key=f"degree_{i}")
        if degree != "High School Diploma":
            field = st.selectbox(f"Select Field of Study {i+1}", field_options, key=f"field_{i}")
        else:
            field = None
        st.session_state.education_blocks[i] = {"degree": degree, "field": field}

    # Predict Career
    if st.button("✅ Get Career Recommendations"):
        if not st.session_state.education_blocks:
            st.error("❗ Please add at least one education entry.")
            st.stop()

        try:
            selected_degrees = [entry["degree"] for entry in st.session_state.education_blocks]
            selected_fields = [entry["field"] for entry in st.session_state.education_blocks if entry["field"] is not None]

            degree_encoded = mlb_degree.transform([selected_degrees])
            field_encoded = mlb_field.transform([selected_fields]) if selected_fields else np.zeros((1, len(mlb_field.classes_)))

            model_input = np.hstack((np.array(model_skills_input).reshape(1, -1), degree_encoded, field_encoded))

            # 4. Predict
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(model_input)[0]
                top_indices = np.argsort(probs)[-5:][::-1]
                job_titles = le.inverse_transform(top_indices)
                scores = probs[top_indices]

                st.subheader("🎯 Top 5 Job Recommendations:")
                print("\n🎯 Top 5 Job Recommendations:")
                for idx, (title, score) in enumerate(zip(job_titles, scores), 1):
                    description = job_descriptions_dict.get(title, "No description available.")
                    st.write(f"\n{i}. {title} — Confidence: {score:.2%}")
                    st.write(f"   📖 Description: {description}")
            else:
                prediction = model.predict(model_input)
                job = le.inverse_transform(prediction)[0]
                st.subheader(f"🎯 Recommended Job Title: **{job}**")

            # 5. Skill Courses
            st.subheader("🔵 Courses Based on Your Skills")
            for skill in model_skill_order:
                if skill_averages[skill] <= 3:
                    st.write(f"- {skill}: [Course Link]({skill_courses[skill]})")

            # 6. Question-based Courses
            st.subheader("🟣 Personalized Course Suggestions")
            for q, score in st.session_state.responses.items():
                if score <= 3 and q in question_courses:
                    st.write(f"- {questions[q]}: [Course Link]({question_courses[q]})")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
