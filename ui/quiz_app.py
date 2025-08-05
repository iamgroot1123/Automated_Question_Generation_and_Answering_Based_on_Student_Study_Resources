import streamlit as st
import json

# Load questions
with open("../data/generated_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

st.title("🧠 Quiz Time - Auto Generated Questions")
score = 0
submitted = st.button("Submit Quiz")

# Store user answers
user_answers = {}

for q in questions:
    st.markdown(f"---\n### Q{q['id']}")

    # MCQ Section
    st.markdown(f"**MCQ:** {q['mcq']['question']}")
    selected_option = st.radio(
        f"Options for Q{q['id']}",
        q['mcq']['options'],
        key=f"mcq_{q['id']}"
    )
    user_answers[f"mcq_{q['id']}"] = selected_option

    # Short Answer Section
    st.markdown(f"**Short Answer:** {q['short_answer']['question']}")
    short_response = st.text_input("Your Answer:", key=f"short_{q['id']}")
    user_answers[f"short_{q['id']}"] = short_response

# Check answers if submitted
if submitted:
    st.markdown("---")
    st.subheader("✅ Results")

    for q in questions:
        qid = q['id']
        # MCQ
        correct_mcq = q['mcq']['answer']
        if user_answers[f"mcq_{qid}"] == correct_mcq:
            score += 1
            st.success(f"Q{qid} MCQ: Correct!")
        else:
            st.error(f"Q{qid} MCQ: Incorrect. Answer: {correct_mcq}")

        # Short Answer
        correct_short = q['short_answer']['answer'].strip().lower()
        user_short = user_answers[f"short_{qid}"].strip().lower()
        if user_short == correct_short:
            score += 1
            st.success(f"Q{qid} Short Answer: Correct!")
        else:
            st.error(f"Q{qid} Short Answer: Incorrect. Answer: {correct_short}")

    st.markdown(f"---\n### 🎯 Total Score: `{score}` / `{len(questions) * 2}`")
