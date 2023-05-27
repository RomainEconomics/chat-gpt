from langchain.callbacks import CallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage
from langchain.schema import HumanMessage
from langchain.schema import SystemMessage
from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt

from chat_gpt.utils.callbacks import rich_streaming_display
from chat_gpt.utils.callbacks import StreamingTerminalCallbackHandler


def chat(model_name: str):
    console = Console()

    messages: list[BaseMessage] = [
        SystemMessage(
            content="You’re a helpful programming assistant. Answers the questions as a professional programmer."
        ),
    ]

    console.print("Starting a chat ...")
    console.print()

    while True:
        content = Prompt.ask("[red][b]User [b/]")
        console.print()
        messages.append(HumanMessage(content=content))

        stream_manager = CallbackManager(
            [
                StreamingTerminalCallbackHandler(
                    output_callback=lambda x: rich_streaming_display(x, live_chat)
                )
            ]
        )
        chat = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            streaming=True,
            callback_manager=stream_manager,
            verbose=True,
        )

        console.print("[blue][b]Assistant :[/b][/blue]")
        with Live(console=console, refresh_per_second=2) as live_chat:
            ai_response = chat(messages)

        messages.append(ai_response)
        console.print()
