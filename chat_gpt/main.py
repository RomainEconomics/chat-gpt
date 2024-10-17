import os
import sys
import yaml

import openai
import typer
from rich.console import Console
from youtube_transcript_api import TranscriptsDisabled

from chat_gpt.commands.chat import chat
from chat_gpt.commands.youtube import chat_with_yt_video
from chat_gpt.config import CONFIG_PATH, load_config, Config

app = typer.Typer()

console = Console()

openai.api_key = os.environ.get("OPENAI_API_KEY")

if openai.api_key is None:
    console.print("[red]Please set the OPENAI_API_KEY environment variable.")
    exit(1)


@app.command("chat")
def start(
    model_name: str | None = None,
    markdown: bool = False,
    file_path: str | None = None,
):
    """
    Start conversation with our assistant
    """
    config: Config = load_config()

    try:
        chat(model_name or config.MODEL_NAME, markdown=markdown, file_path=file_path)
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


@app.command()
def config(model_name: str):
    """
    Change model configuration
    """

    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    print("Current model name:", config["model_name"])

    # Update the model_name field
    config["model_name"] = model_name

    print("New model name:", config["model_name"])

    # Write the updated configuration back to the file
    with open(CONFIG_PATH, "w") as file:
        yaml.safe_dump(config, file, default_flow_style=False)
