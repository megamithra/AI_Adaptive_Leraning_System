import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from clustering import run_clustering
from prediction import train_prediction_model
from rl_engine import AdaptiveQuiz

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Adaptive Learning", layout="wide")

st.title("AI-Based Adaptive Learning System")
st.markdown("---")

# -----------------------------
# LOAD DATA + MODELS
# -----------------------------
@st.cache_data
def load_data():
    return run_clustering()

@st.cache_resource
def load_model():
    return train_prediction_model()

data, cluster_model = load_data()
prediction_model, error = load_model()

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = AdaptiveQuiz()

if "question" not in st.session_state:
    st.session_state.question = st.session_state.quiz.get_question()

if "answered" not in st.session_state:
    st.session_state.answered = False

quiz = st.session_state.quiz

# -----------------------------
# SIDEBAR
# -----------------------------
menu = st.sidebar.selectbox(
    "Select Module",
    ["Dashboard", "Student Prediction", "Cluster Analysis", "Adaptive Quiz"]
)

# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "Dashboard":

    st.header("Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Students", len(data))
    c2.metric("Avg Score", round(data["quiz_score"].mean(), 2))
    c3.metric("Model Error", round(error, 2))

    st.dataframe(data)

    st.subheader("Score Distribution")

    fig, ax = plt.subplots()
    sns.histplot(data["quiz_score"], bins=10, kde=True, ax=ax)
    st.pyplot(fig)

# -----------------------------
# PREDICTION
# -----------------------------
elif menu == "Student Prediction":

    st.header("Predict Score")

    study_hours = st.slider("Study Hours", 1, 10, 5)
    quiz_score = st.slider("Quiz Score", 0, 100, 50)
    accuracy = st.slider("Accuracy", 0, 100, 60)
    attendance = st.slider("Attendance", 0, 100, 70)

    if st.button("Predict"):

        pred = prediction_model.predict([[study_hours, quiz_score, accuracy, attendance]])

        st.success(f"Predicted Score: {round(pred[0], 2)}")

# -----------------------------
# CLUSTER
# -----------------------------
elif menu == "Cluster Analysis":

    st.header("Clusters")

    st.dataframe(data[["study_hours", "quiz_score", "cluster"]])

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=data,
        x="study_hours",
        y="quiz_score",
        hue="cluster",
        palette="deep",
        ax=ax
    )

    st.pyplot(fig)

# -----------------------------
# ADAPTIVE QUIZ (FIXED)
# -----------------------------
elif menu == "Adaptive Quiz":

    st.header("Adaptive Quiz")

    st.subheader(f"Difficulty: {quiz.difficulty}")

    q = st.session_state.question

    st.write("### Question")
    st.write(q["question"])

    answer = st.text_input("Your Answer")

    if st.button("Submit"):

        correct = answer.strip().lower() == q["answer"].lower()

        if correct:
            st.success("Correct")
        else:
            st.error(f"Wrong. Answer: {q['answer']}")

        quiz.update(correct)
        st.session_state.answered = True

        st.write("Score:", quiz.score)

    if st.session_state.answered:

        if st.button("Next Question"):

            st.session_state.question = quiz.get_question()
            st.session_state.answered = False
            st.rerun()