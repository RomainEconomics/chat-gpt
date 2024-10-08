import os
import sys
from typing import Optional

import openai
import typer
from rich.console import Console
from youtube_transcript_api import TranscriptsDisabled

from chat_gpt.commands.chat import chat
from chat_gpt.commands.youtube import chat_with_yt_video

app = typer.Typer()

console = Console()

openai.api_key = os.environ.get("OPENAI_API_KEY")

if openai.api_key is None:
    console.print("[red]Please set the OPENAI_API_KEY environment variable.")
    exit(1)


@app.command("chat")
def start(
    model_name: str = "gpt-4o", markdown: bool = False, file_path: Optional[str] = None
):
    """
    Start conversation with our assistant
    """
    try:
        chat(model_name, markdown=markdown, file_path=file_path)
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)


@app.command()
def youtube(url: str, language: str = "en"):
    """
    Start conversation with our assistant using a youtube video transcript
    """

    try:
        chat_with_yt_video(url, language)
    except TranscriptsDisabled as e:
        console.print(
            "\n[red]Transcripts are disabled for this video or the video you're trying to extract doesn't exist."
        )
        console.print(e)
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
