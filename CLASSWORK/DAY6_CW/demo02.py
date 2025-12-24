from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def calculator(exp):
    """
    This is calculator function solves any arithmetic expression containing all constant value.
    It supports basic arithmetic operators +,-,*,/, and paranthesis.
    

    :param exp: str input arithmetic expression
    : returns expression result as str 

    """
    try:
        result = eval(exp)
        return str(result)
    except:
        return "Error: Cannot solve expression"
    
llm = init_chat_model(
    model = "google_gemma-3-4b-it",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "no_need"
)

agent = create_agent(
                model=llm,
                tools=[calculator
                       ],
                system_prompt="You are a helpful assistant. Answer in short."
            )

while True:
    user_input = input("You: ")
    if user_input == "Exit":
        break

    result = agent.invoke({
        "messages":[
            {"role": "user", "content": user_input}
        ]
    })

    llm_output = result["messages"][-1]
    print("AI: ", llm_output.content)
    print("\n\n", result["messages"])
