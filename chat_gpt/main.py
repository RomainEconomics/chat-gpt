
from rich.prompt import Prompt
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
import time
import os
import sys
import openai
import typer

app = typer.Typer()


def main():

    console = Console()
    
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    if openai.api_key is None:
        console.print('[red]Please set the OPENAI_API_KEY environment variable.')
        exit(1)  

    messages = [
     {"role": "system", "content" : "You’re a helpful programming assistant"}
    ]


    console.print("Starting a chat ...")

    while True:
        console.print()
        content = Prompt.ask("[red][b]User [b/]")
        console.print()
        messages.append({"role": "user", "content": content})

        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages,
          temperature=0,
          stream=True 
        )

        console.print("[blue][b]Assistant :[/b]")
        chat_response = "" 
        with Live(console=console, refresh_per_second=2) as live_chat:
            for chunk in completion:
                if "content" in chunk.choices[0].delta:
                    chat_response += chunk.choices[0].delta.content
                else:
                    pass
                live_chat.update(Markdown(chat_response))

        messages.append({"role": "assistant", "content": chat_response})
        console.print()



@app.command()
def start():
    """
    Start conversation with our assistant
    """
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)