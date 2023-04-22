
from typing import Any
from rich.prompt import Prompt
from rich.console import Console
from rich.live import Live
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import CallbackManager
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    BaseMessage
)
from chat_gpt.utils.callbacks import StreamingTerminalCallbackHandler, rich_streaming_display



def chat():

    console = Console()

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
