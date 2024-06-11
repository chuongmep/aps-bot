import click
import os
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI
from .config import Config


@click.command()
def chat():
    """This command starts a chat session with the bot."""
    click.echo("Starting chat with the bot. Type 'exit' to end the chat.")
    client = OpenAI()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            click.echo("Ending chat session.")
            break
        chat_complete = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        bot_response = chat_complete.choices[0].message.content
        click.echo(f"Bot: {bot_response}")


@click.command()
@click.option('--folder_path', prompt='Folder Path', default=lambda: Config.load_folder_path(), help='The folder path.')
def chat_data(folder_path):
    """This command starts a chat with knowledge based on data in the specified folder."""
    click.echo("Starting chat with the bot. Type 'exit' to end the chat.")
    if not os.path.exists(folder_path):
        click.echo("Invalid folder path.")
        return
    # Read and process CSV files in the specified folder
    Config.save_folder_path(folder_path)
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
    GPT_MODEL = "gpt-3.5-turbo"
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content
