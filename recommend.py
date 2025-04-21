import openai
import os
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = """
You are an expert international higher education counselor with deep knowledge of master's programs around the world. Your job is to match students to the most realistic and well-suited graduate programs based on their actual academic background, goals, budget, and preferences.

Using the student profile provided, recommend **exactly 5 real, verifiable university + program combinations** that align with their goals and constraints.

Here are your rules:

1. **Do not recommend unrealistic or generic top-tier programs** (e.g., Stanford, MIT, Oxford) unless the student’s academic profile clearly qualifies.
2. Each recommendation MUST include:
   - **University Name + Program Name**
   - **Why it's a good fit** (tie directly to GPA, stream, work experience, goals, budget, etc.)
   - **Course structure** (duration, specialization areas, internships, capstone, etc.)
   - **Tuition + estimated living costs** (in USD or local currency as appropriate)
   - **City + Country**
   - **Post-graduate work opportunities** (stay-back visas, OPT/PGWP, typical employers or industries)
3. **Do not hallucinate** program names, structures, or costs. Use real data from 2023–2024 if available.
4. Make the tone sound like a seasoned, confident advisor—not like a Google search result or ChatGPT default.
5. Every part of your response should be thoughtful, specific, and useful enough that a human counselor could send it directly to a student without edits.

Format strictly like this for each recommendation:

1. **University Name - Program Name**
   - *Why a Good Fit:* ...
   - *Course Structure:* ...
   - *Tuition + Living Costs:* ...
   - *Country + City:* ...
   - *Post-Graduation Options:* ...

If you are unsure or can't verify something, say so. Prioritize transparency over guesswork.
"""

# --- Input function ---
def get_student_input():
    print("Enter student details:")
    data = {}
    data['Name'] = input("Name: ")
    data['Current city'] = input("Current city: ")
    data['DOB'] = input("Date of Birth (YYYY-MM-DD): ")
    data['XII completion year'] = input("Year of XIIth grade completion: ")
    data['XII percentage'] = input("XII percentage: ")
    data['Undergrad status'] = input("Status of undergrad (completed/ongoing): ")
    data['Stream'] = input("Stream pursuing/pursued: ")
    data['Undergrad completion year'] = input("Year of undergrad completion (or expected): ")
    data['CGPA'] = input("CGPA or final GPA: ")
    data['Backlogs'] = input("Any backlogs or KTs? (yes/no): ")
    data['Gap years'] = input("Gap years, if any: ")
    data['Work experience'] = input("Number of years of work experience: ")
    data['Career goals'] = input("Specific career goals: ")
    data['Financial concern'] = input("Are finances a concern? (yes/no): ")
    data['Post grad stay'] = input("Do you plan to stay in the country post graduation? (yes/no): ")
    data['Relevant experience'] = input("Do you have relevant work experience in your chosen field? (yes/no): ")
    data['Family abroad'] = input("Do you have family abroad? (yes/no): ")
    data['Switch courses'] = input("Would you consider switching courses? (yes/no): ")
    data['Extracurriculars or research'] = input("Do you prefer universities with strong extracurricular or research opportunities? (yes/no): ")
    data['Cultural familiarity'] = input("How familiar are you with the country's culture and academic environment? ")
    data['Budget'] = input("Budget (in USD/year): ")
    data['Interested country'] = input("Country you're interested in: ")
    return data

def build_prompt(student_data):
    user_prompt = "Student Profile:\n"
    for key, value in student_data.items():
        user_prompt += f"{key}: {value}\n"
    user_prompt += "\nBased on this profile, suggest 5 realistic university programs.\n"
    return user_prompt

def main():
    student_data = get_student_input()
    user_prompt = build_prompt(student_data)

    print("\nGenerating recommendations... please wait.\n")

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )

    result = response.choices[0].message.content
    usage = response.usage

    print("=== University Recommendations ===\n")
    print(result)

    print("\n=== Token Usage Summary ===")
    print(f"Prompt tokens: {usage.prompt_tokens}")
    print(f"Completion tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")

    # --- Estimate cost (GPT-4-8K pricing as of 2024) ---
    input_cost_per_1k = 0.03   # $0.03 per 1K prompt tokens
    output_cost_per_1k = 0.06  # $0.06 per 1K completion tokens

    cost = (usage.prompt_tokens / 1000 * input_cost_per_1k) + (usage.completion_tokens / 1000 * output_cost_per_1k)
    print(f"Estimated cost: ${cost:.4f} USD")

# --- Entry point ---
if __name__ == "__main__":
    main()
