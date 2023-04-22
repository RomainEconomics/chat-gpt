
from typing import Any, Callable
from rich.prompt import Prompt
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
import os
import sys
import openai
import typer
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    BaseMessage
)

app = typer.Typer()


class StreamingTerminalCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self, output_callback: Callable[[str], None] = None, **kwargs):
        super().__init__(**kwargs)
        self.output = ""
        self.output_callback = output_callback

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.output += token
        if self.output_callback is not None:
            self.output_callback(self.output)


def rich_streaming_display(token: str, live_chat) -> None:
    live_chat.update(Markdown(token))

def chat():

    console = Console()
    
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    if openai.api_key is None:
        console.print('[red]Please set the OPENAI_API_KEY environment variable.')
        exit(1)  

    messages: list[BaseMessage] = [
        SystemMessage(content="You’re a helpful programming assistant. Answers the questions as a professional programmer."),
    ]

    console.print("Starting a chat ...")

    while True:
        console.print()
        content = Prompt.ask("[red][b]User [b/]")
        console.print()
        messages.append(HumanMessage(content=content))

        stream_manager = CallbackManager(
            [StreamingTerminalCallbackHandler(output_callback= lambda x: rich_streaming_display(x, live_chat))]
        )
        chat = ChatOpenAI(temperature=0, streaming=True, callback_manager=stream_manager, verbose=True)

        console.print("[blue][b]Assistant :[/b][/blue]")
        with Live(console=console, refresh_per_second=2) as live_chat:
            ai_response = chat(messages)
        
        messages.append(ai_response)
        console.print()


@app.command()
def start():
    """
    Start conversation with our assistant
    """
    try:
        chat()
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)