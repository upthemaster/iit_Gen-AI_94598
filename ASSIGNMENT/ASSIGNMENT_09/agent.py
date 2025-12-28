from intern import web_scrape
from batch import batch_fee_scrape
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

import pandas as pd
from pandasql import sqldf
from langchain.tools import tool

@tool
def csv_tool(filepath: str, sql_query: str):
    """
    CSV Question Answering Tool

    Inputs:
        filepath (str): Path of the CSV file
        sql_query (str): SQL query generated from user question

    Output:
        Final answer after executing SQL on CSV data
    """

    try:
        # Load CSV
        df = pd.read_csv(filepath)

        # Execute SQL using pandasql
        result = sqldf(sql_query, {"data": df})

        # Return answer (not query)
        return result.to_string(index=False)

    except FileNotFoundError:
        return "CSV file not found."

    except Exception as e:
        return f"Error while processing CSV: {str(e)}"



llm = init_chat_model(
    model="google_gemma-3-4b-it",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)


agent = create_agent(
    model=llm,
    tools=[
           csv_tool,
           web_scrape,
           batch_fee_scrape
           ],
    system_prompt = (
        """
        You are an intelligent tool-using assistant.

        Instructions:
        1. Analyze the user question and choose the correct tool automatically.
        2. For CSV-related questions:
            - Convert the question into a valid SQL query using table name `data`
            - Call csv_tool with the CSV file path and SQL query
            - Return only the final answer, not the SQL
        3. For internship-related questions (technology, aim, prerequisites, learning, location):
            - Call web_scrape once and answer strictly from its output
        4. For batch-related questions (schedule, duration, dates, time, fees):
            - Call batch_fee_scrape once and answer strictly from its output
        5. Do not ask the user for URLs or re-scrape data for follow-up questions.
        6. Respond in simple, short, and factual English only.

        """
    )
)

conversation = [] 

while True:
    user_prompt = input("Ask: ")
    if user_prompt.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    })

    ai_msg = result["messages"][-1].content
    print("AI msg:", ai_msg)

    conversation.append({
        "user": user_prompt,
        "assistant": ai_msg
    })