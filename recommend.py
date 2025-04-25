import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- System Prompt (Improved Version) ---
system_prompt = """
You are a world-class international education counselor helping Indian students choose master's programs abroad.

You are given a student profile, and your job is to recommend exactly 5 real, verifiable university + program combinations.

Every recommendation MUST be thoughtful and counselor-level — realistic, specific, and research-backed.

### YOUR RULES:

1. DO NOT suggest Ivy League / elite schools unless the profile *clearly qualifies*. Avoid generic top-tiers like Stanford, MIT, unless well-justified.

2. Each of your 5 program recommendations must include:
   - **University Name + Program Name**
   - **Why it's a Good Fit:** Connect to GPA, undergrad stream, work ex, career goal, extracurriculars, budget, etc.
   - **Course Structure:** Duration, key subjects, optional tracks, capstone/internship/research components.
   - **Tuition + Living Costs:** Use accurate 2023/2024 numbers, mention currency. Flag if above or below budget.
   - **City + Country**
   - **Post-Graduation Options:** Visa duration, job market strength, industries hiring grads, typical job roles.
   - **ROI Insight:** Typical graduate salary (if verifiable), payback time, or salary vs tuition comparison.
   - **Alumni Outcomes:** Name real companies, roles, or platforms where past graduates have worked. If not available, say “No verified data.”

3. Maintain a professional tone — like a seasoned counselor speaking to a serious student. No fluff. No hallucination. Be honest if unsure.

4. All information should be factually verifiable and useful for decision-making. No summarizing, no generic benefits.

FORMAT STRICTLY LIKE THIS:

1. **University Name - Program Name**
   - *Why a Good Fit:* ...
   - *Course Structure:* ...
   - *Tuition + Living Costs:* ...
   - *Country + City:* ...
   - *Post-Graduation Options:* ...
   - *ROI Insight:* ...
   - *Alumni Outcomes:* ...

You are not a chatbot — you are a senior counselor at a premium global education consultancy. Be precise, data-driven, and transparent.
"""

# --- Streamlit UI ---
st.set_page_config(page_title="University Recommender", layout="wide")
st.title("🎓 GradGuide – AI-Powered University Recommender")

with st.form("student_form"):
    st.subheader("📋 Enter Student Profile")

    name = st.text_input("Name")
    city = st.text_input("Current City")
    dob = st.text_input("Date of Birth (YYYY-MM-DD)")
    xii_year = st.text_input("XII Completion Year")
    xii_percent = st.text_input("XII Percentage")
    ug_status = st.selectbox("Undergrad Status", ["Completed", "Ongoing"])
    stream = st.text_input("UG Stream")
    grad_year = st.text_input("UG Completion Year")
    cgpa = st.text_input("CGPA")
    backlogs = st.selectbox("Any Backlogs?", ["No", "Yes"])
    gaps = st.text_input("Gap Years (if any)")
    work_exp = st.text_input("Work Experience (in years)")
    goals = st.text_area("Career Goals")
    finance = st.selectbox("Is Budget a Concern?", ["Yes", "No"])
    post_stay = st.selectbox("Stay in Country Post Graduation?", ["Yes", "No"])
    relevant_exp = st.selectbox("Relevant Work Exp in Field?", ["Yes", "No"])
    family_abroad = st.selectbox("Family Abroad?", ["Yes", "No"])
    switch_course = st.selectbox("Open to Switching Courses?", ["Yes", "No"])
    extracurriculars = st.selectbox("Strong in Research/ECAs?", ["Yes", "No"])
    culture = st.text_input("Familiarity with Foreign Culture")
    budget = st.text_input("Annual Budget (USD)")
    country = st.text_input("Interested Country")

    submitted = st.form_submit_button("🎯 Generate Recommendations")

if submitted:
    # Build user prompt
    user_prompt = "Student Profile:\n"
    fields = {
        "Name": name, "Current city": city, "DOB": dob, "XII completion year": xii_year,
        "XII percentage": xii_percent, "Undergrad status": ug_status, "Stream": stream,
        "Undergrad completion year": grad_year, "CGPA": cgpa, "Backlogs": backlogs,
        "Gap years": gaps, "Work experience": work_exp, "Career goals": goals,
        "Financial concern": finance, "Post grad stay": post_stay,
        "Relevant experience": relevant_exp, "Family abroad": family_abroad,
        "Switch courses": switch_course, "Extracurriculars or research": extracurriculars,
        "Cultural familiarity": culture, "Budget": budget, "Interested country": country
    }

    for k, v in fields.items():
        user_prompt += f"{k}: {v}\n"
    user_prompt += "\nBased on this profile, suggest 5 realistic university programs.\n"

    # GPT Call
    st.info("Generating recommendations... please wait.")
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        result = response.choices[0].message.content

        st.success("✅ Recommendations generated!")
        st.markdown("### 🎓 Recommended Universities")
        st.markdown(result)

        st.download_button(
            label="📄 Download as TXT",
            data=result,
            file_name=f"{name}_recommendations.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
