from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

llm = init_chat_model(
    model="google_gemma-3-4b-it",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key = "not_needed"
)

conversation = []

agent = create_agent(
    model=llm,
    tools = [],
    system_prompt="You are a helpful assisstant, Answer in short."
    
    )

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    conversation.append({"role": "user", "content":user_input})
    result = agent.invoke({"messages": conversation})
    ai_msg = result["messages"][-1]
    print("AI: ", ai_msg.content)

    conversation = result["messages"]