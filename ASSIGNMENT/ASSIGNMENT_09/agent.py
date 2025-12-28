from intern import web_scrape
from batch import batch_fee_scrape
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def read_file(filepath):
    """Read and return the content of a text file.

    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except :
        return f"Error reading file:"


llm = init_chat_model(
    model="google_gemma-3-4b-it",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)


agent = create_agent(
    model=llm,
    tools=[
           read_file,
           web_scrape,
           batch_fee_scrape
           ],
    system_prompt = (
    """
    You are a tool-using assistant.

    Rules:
    1. Always decide the correct tool based on the user question.
    2. If the question is about internships, technologies, prerequisites, learning, or location:
    → call the web_scrape tool ONCE and use its data to answer.
    3. If the question is about batch schedule, batch duration, dates, time, or fees:
    → call the batch_fee_scrape tool ONCE and use its data to answer.
    4. Do NOT ask the user for any URL.
    5. Do NOT re-scrape data for follow-up questions.
    6. Answer only from the tool output.
    7. If data is not found, clearly say "Information not available".

    Keep answers short, clear, and factual.


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
