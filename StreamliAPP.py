import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

# Your local package
try:
    from mcqgenerator.utils import read_file, get_table_data
    from langchain.callbacks import get_openai_callback
    from mcqgenerator.MCQGenerator import generate_evaluate_chain
    from mcqgenerator.loggers import logging
except Exception as e:
    st.title("MCQs Creator Application with LangChain 🦜⛓")
    st.error("Failed to import project modules. See details below.")
    st.exception(e)
    st.stop()

# Load .env (you imported it but didn’t call it)
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.warning("OPENAI_API_KEY not found in environment. Set it in a .env file or the environment.")

# Load the JSON schema safely
RESPONSE_JSON = {}
json_path_candidates = ["Response.json", "response.json", "./response.json", "./Response.json"]
json_loaded = False
for p in json_path_candidates:
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                RESPONSE_JSON = json.load(f)
                json_loaded = True
                break
        except Exception as e:
            st.warning(f"Found {p} but failed to parse JSON: {e}")

if not json_loaded:
    st.warning("Response.json not found or invalid. Using a minimal fallback schema.")
    RESPONSE_JSON = {"quiz": [], "review": ""}

st.title("MCQs Creator Application with LangChain 🦜⛓")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50, value=5)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Create MCQs")

if button:
    if uploaded_file is None or not mcq_count or not subject or not tone:
        st.error("Please provide all the inputs above.")
        st.stop()

    with st.spinner("Generating MCQs..."):
        try:
            text = read_file(uploaded_file)
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON),
                    }
                )
        except Exception as e:
            # Correct traceback attribute is __traceback__, not _traceback_
            st.error("An error occurred while generating MCQs:")
            st.code("".join(traceback.format_exception(type(e), e, e.__traceback__)))
            st.stop()

        # Show token/cost info in the UI (prints go to console otherwise)
        st.info(
            f"Total Tokens: {cb.total_tokens} | "
            f"Prompt: {cb.prompt_tokens} | "
            f"Completion: {cb.completion_tokens} | "
            f"Estimated Cost: ${cb.total_cost:.6f}"
        )

        if isinstance(response, dict):
            quiz = response.get("quiz")
            if quiz:
                table_data = get_table_data(quiz)
                if table_data is not None:
                    df = pd.DataFrame(table_data)
                    df.index = df.index + 1
                    st.table(df)
                    st.text_area(label="Review", value=response.get("review", ""), height=200)
                else:
                    st.error("Error in the table data.")
            else:
                st.warning("No quiz data returned.")
        else:
            st.write(response)
