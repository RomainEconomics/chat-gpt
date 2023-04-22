
import os
from typing import Any, Callable
from rich.markdown import Markdown
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler




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