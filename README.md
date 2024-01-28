# Use LLMs inside your terminal 

## Install

```
pip install custom-chat-gpt
```

## Usage

```
chat-gpt --help
chat-gpt chat               # chat with the default model
chat-gpt chat --markdown    # chat with the default model and markdown output
chat-gpt youtube            # chat with a youtube video transcript
```


## Dev commands

```
poetry init
poetry add openai rich typer
poetry shell
poetry install
poetry run chat-gpt
poetry build
poetry publish
```