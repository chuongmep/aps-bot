import click
import os
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI
from .config import Config
import openai

@click.command()
@click.option('--model_name', prompt='Model', default=lambda: Config.load_ai_model(), help='The model to use.')
def chat(model_name):
    """This command starts a chat session with the bot."""
    Config.save_ai_model(model_name)
    click.echo("Starting chat with the bot. Type 'exit' to end the chat.")
    client = OpenAI()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            click.echo("Ending chat session.")
            break
        messages_pompt = []
        messages_pompt += [{"role":"user", "content": user_input}]
        response = openai.chat.completions.create(
            messages = messages_pompt,
            model=model_name,
            temperature=0,
            max_tokens=500,
        )
        bot_response = response.choices[0].message.content
        click.echo(f"Bot: {bot_response}")

@click.command()
@click.option('--folder_path', prompt='Folder Path', default=lambda: Config.load_folder_path(), help='The folder path.')
@click.option('--model_name', prompt='Model', default=lambda: Config.load_ai_model(), help='The model to use.')
def chat_data(folder_path, model_name):
    """This command starts a chat with knowledge based on data in the specified folder."""
    click.echo("Starting chat with the bot. Type 'exit' to end the chat.")
    if not os.path.exists(folder_path):
        click.echo("Invalid folder path.")
        return
    # Read and process CSV files in the specified folder
    Config.save_folder_path(folder_path)
    Config.save_ai_model(model_name)
    dfs = read_and_process_csv(folder_path)
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            click.echo("Ending chat session.")
            break
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0), dfs, verbose=True)
        bot_response = agent.invoke(user_input)
        click.echo(f"Bot: {bot_response}")


def read_and_process_csv(folder_path):
    # List all CSV files in the specified folder
    dataframes = [pd.read_csv(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if
                  file.endswith('.csv')]
    return dataframes


def interact_with_chatgpt(knowledge_base, query):
    # Format the input for the chat model
    knowledge_summary = '\n'.join([f"{key}: {value}" for key, value in knowledge_base.items()])
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",
         "content": f"Here is some knowledge:\n\n{knowledge_summary}\n\nBased on this information, {query}"}
    ]
    client = OpenAI()
    GPT_MODEL = Config.load_ai_model()
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content
