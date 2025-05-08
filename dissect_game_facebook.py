import streamlit as st
import random
import csv

# Updated sections including a separate Literature Review
sections = {
    "Abstract": {
        "text": "This meta-analysis looked at 18 studies with 8,798 participants to find out if using Facebook makes people feel more or less lonely. The study found a small but significant positive correlation: more Facebook use was linked with more loneliness. The analysis also explored whether loneliness causes people to use Facebook more, or if using Facebook leads to loneliness.",
        "question": "What was the main purpose of the abstract?",
        "options": ["To present detailed statistics", "To summarize the study's purpose and results", "To explain the methods"],
        "answer": "To summarize the study's purpose and results",
        "explanation": "The abstract provides a concise overview of the entire study including its aims, methods, and key findings."
    },
    "Introduction": {
        "text": "Loneliness is a growing concern in modern society. The authors introduce the idea that online social networking sites like Facebook may play a role in either reducing or contributing to loneliness. They aim to explore this question through a meta-analysis.",
        "question": "What is the main role of the Introduction section?",
        "options": ["To explain statistical results", "To describe previous studies in detail", "To introduce the research question and purpose"],
        "answer": "To introduce the research question and purpose",
        "explanation": "The introduction briefly sets up the research question, provides rationale, and outlines the study’s intent."
    },
    "Literature Review": {
        "text": "Previous research has produced mixed findings about Facebook and loneliness. Some studies suggest Facebook helps people connect socially, while others show it may replace face-to-face interaction, increasing loneliness. Researchers have examined both time spent on Facebook and psychological motives for its use.",
        "question": "Which best describes the purpose of the Literature Review section?",
        "options": ["To present the data analysis", "To explain the hypothesis", "To summarize past studies and theoretical models"],
        "answer": "To summarize past studies and theoretical models",
        "explanation": "The literature review synthesizes prior research findings and identifies gaps that the current study aims to fill."
    },
    "Methods": {
        "text": "The researchers searched databases for studies using keywords like 'Facebook' and 'loneliness.' They only included studies with quantitative data that could be used to calculate effect sizes. Different ways of measuring Facebook use and loneliness were categorized.",
        "question": "Which best describes a key part of the Methods section?",
        "options": ["Describing survey results", "Explaining how data was collected and selected", "Summarizing prior research"],
        "answer": "Explaining how data was collected and selected",
        "explanation": "The methods describe how the researchers gathered and processed the data used in the study."
    },
    "Results": {
        "text": "The overall correlation between Facebook use and loneliness was small but positive (r = .166). People who used Facebook more tended to report more loneliness. This effect varied depending on how Facebook use and loneliness were measured.",
        "question": "What does the Results section do in a research article?",
        "options": ["Offers opinions", "Presents data and findings", "Explains theoretical implications"],
        "answer": "Presents data and findings",
        "explanation": "The Results section objectively presents the study’s findings using statistics and data summaries."
    },
    "Discussion": {
        "text": "The authors concluded that lonely people are more likely to use Facebook as a way to feel connected. This supports the 'social compensation' model. They emphasized that more research is needed to examine long-term effects and differences across age groups.",
        "question": "What is the main role of the Discussion section?",
        "options": ["To present raw data", "To connect results to larger theories", "To restate the method"],
        "answer": "To connect results to larger theories",
        "explanation": "The discussion interprets results, connects them to the broader field, and suggests implications for future research."
    }
}

# Set up Streamlit state
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.round = 0
    st.session_state.history = []
if "section_name" not in st.session_state:
    st.session_state.section_name, st.session_state.section_data = random.choice(list(sections.items()))

st.set_page_config(page_title="Facebook & Loneliness Game", layout="centered")
st.title("📘 Facebook & Loneliness: Research Dissection Game")
st.markdown("Explore and learn from a real journal article. Match each excerpt to its section, and test your knowledge.")

st.subheader(f"🔍 Round {st.session_state.round + 1}: Read This Excerpt")
st.info(st.session_state.section_data["text"])

user_guess = st.selectbox("Which section is this from?", list(sections.keys()))
submit_guess = st.button("Submit Answer")

def next_round():
    st.session_state.round += 1
    st.session_state.section_name, st.session_state.section_data = random.choice(list(sections.items()))
    st.experimental_rerun()

if submit_guess:
    correct = user_guess == st.session_state.section_name
    if correct:
        st.success(f"✅ Correct! This is the **{st.session_state.section_name}** section.")
        st.session_state.score += 1
    else:
        st.error(f"❌ Nope — this is actually from the **{st.session_state.section_name}** section.")
        st.warning("Hint: Think about the main purpose of the excerpt.")
    with st.expander("🧠 Explanation"):
        st.write(st.session_state.section_data["explanation"])

    st.subheader("🧠 Bonus Question")
    st.write(st.session_state.section_data["question"])
    answer = st.radio("Choose your answer:", st.session_state.section_data["options"], key=f"bonus_{st.session_state.round}")
    submit_bonus = st.button("Submit Bonus", key=f"submit_bonus_{st.session_state.round}")
    if submit_bonus:
        correct_bonus = answer == st.session_state.section_data["answer"]
        if correct_bonus:
            st.success("🎉 Correct! You earned an extra point.")
            st.session_state.score += 1
        else:
            st.error(f"🤔 Not quite. The correct answer is: **{st.session_state.section_data['answer']}**")
        with st.expander("📚 Bonus Explanation"):
            st.write(st.session_state.section_data["explanation"])

    st.session_state.history.append({
        "round": st.session_state.round + 1,
        "guess": user_guess,
        "correct_section": st.session_state.section_name,
        "bonus_answer": answer,
        "correct_bonus": st.session_state.section_data["answer"],
        "score": st.session_state.score
    })

    st.button("Next Round ▶️", on_click=next_round)

# Download CSV
if st.session_state.history:
    st.subheader("📥 Download Results")
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=st.session_state.history[0].keys())
        writer.writeheader()
        writer.writerows(st.session_state.history)
    with open("results.csv", "rb") as f:
        st.download_button("Download CSV", f, "facebook_game_results.csv", mime="text/csv")

st.sidebar.markdown("### 🎯 Your Progress")
st.sidebar.write(f"**Rounds Played:** {st.session_state.round}")
st.sidebar.write(f"**Total Score:** {st.session_state.score}")
