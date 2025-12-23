import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("CSV SQL Assistant")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("CSV Schema")
    st.write(df.dtypes)

    user_question = st.text_input("Ask a question about the data")

    if user_question:

        prompt = f"""
        Convert the following question into an SQL query.
        Table name: df
        Columns and types:
        {df.dtypes}

        Question: {user_question}
        Return only SQL.
        """

        sql_query = llm.invoke(prompt).content.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        st.subheader("Generated SQL")
        st.code(sql_query)

        try:
            result = sqldf(sql_query, {"df": df})
            st.subheader("Query Result")
            st.dataframe(result)

            explain_prompt = f"""
            Explain the following result in simple English:

            SQL Query:
            {sql_query}

            Result:
            {result.head()}
            """

            explanation = llm.invoke(explain_prompt).content
            st.subheader("Explanation")
            st.write(explanation)

        except Exception as e:
            st.error(f"SQL Error: {e}")
