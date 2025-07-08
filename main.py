import chainlit as cl
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, Agent, Runner
from agents.run import RunConfig
import os

#ASYNC CODE

@cl.on_message
async def main(msg:cl.Message):

    API_KEY=os.getenv("GEMINI_API_KEY")
    base_url=os.getenv("base_url")

    client = AsyncOpenAI(
        api_key=API_KEY,
        base_url=base_url
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )

    config = RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True
    )

    autism_agent = Agent(
        name="Agent for autistic behavior",
        instructions="You check the user's input and try to analyze if it matches the symptoms of autism. Help the user nicely and also reminds them that you're just a bot not a real life therapist. use resources and provide links.",
        handoff_description="Specialist agent for checking autism in user behavior.",
    )

    adhd_agent = Agent(
        name="Agent for adhd behavior",
        instructions="You check the user's input and try to analyze with professioncy that if it matched with the symptoms of adhd. Help the user nicely and also reminds them that you're just a bot not a real life therapist so advice them to consult a real one. Use resources and provide links.",
        handoff_description="Specialist agent for checking adhd in user's behavior."
    )

    triage_agent = Agent(
        name="Triage agent",
        instructions="You determine which agent to use based on the user's input and behavior.",
        model=model,
        handoffs=[autism_agent, adhd_agent]
    )
    print(f"The user query: {msg.content}")
    await cl.Message(content="Querying.....").send()

    try:
        result = await Runner.run(
            starting_agent=triage_agent,
            input=msg.content,
            run_config=config
        )
        await cl.Message(content=f"\n{result.final_output}").send()
    except Exception as e:
        await cl.Message(content=f"An error occurred during agent execution:\n{e}").send()

#SYNC CODE
    
# API_KEY=os.getenv("GEMINI_API_KEY")
# base_url=os.getenv("base_url")

# client = AsyncOpenAI(
#     api_key=API_KEY,
#     base_url=base_url
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=client
# )

# config = RunConfig(
#     model=model,
#     model_provider=client,
#     tracing_disabled=True
# )

# autism_agent = Agent(
#     name="Agent for autistic behavior",
#     instructions="You check the user's input and try to analyze if it matches the symptoms of autism. Help the user nicely and also reminds them that you're just a bot not a real life therapist. use resources and provide links.",
#     handoff_description="Specialist agent for checking autism in user behavior.",
# )

# adhd_agent = Agent(
#     name="Agent for adhd behavior",
#     instructions="You check the user's input and try to analyze with professioncy that if it matched with the symptoms of adhd. Help the user nicely and also reminds them that you're just a bot not a real life therapist so advice them to consult a real one. Use resources and provide links.",
#     handoff_description="Specialist agent for checking adhd in user's behavior."
# )

# triage_agent = Agent(
#     name="Triage agent",
#     instructions="You determine which agent to use based on the user's input and behavior.",
#     model=model,
#     handoffs=[autism_agent, adhd_agent]
# )

# user_input= input("User:\n")

# result = Runner.run_sync(
#     triage_agent,
#     user_input,
#     run_config=config,
# )
# print(f"Answer: \n{result.final_output}")