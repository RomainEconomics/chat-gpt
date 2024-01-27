from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.live import Live


def chat(model_name: str, markdown: bool):

    console = Console()

    messages: list[BaseMessage] = [
        SystemMessage(
            content="You’re a helpful programming assistant. Answers the questions as a professional programmer."
        ),
    ]

    console.print("Starting a chat ...")
    console.print()

    while True:
        user_content = Prompt.ask("[red][b]User [b/]")
        console.print()
        messages.append(HumanMessage(content=user_content))
        prompt = ChatPromptTemplate.from_messages(messages)

        model = ChatOpenAI(model=model_name, temperature=0.1)
        output_parser = StrOutputParser()

        chain = prompt | model | output_parser

        ai_content = ""

        if markdown:
            console.print("[blue][b]Assistant :[/b][/blue]")
            with Live('', refresh_per_second=10, console=console) as live:
                for chunk in chain.stream({}):
                    ai_content += chunk
                    live.update(Markdown(ai_content))
        else:
            console.print("[blue][b]Assistant :[/b][/blue]", end=" ")

            for chunk in chain.stream({}):
                ai_content += chunk
                console.print(chunk, end="", style="green")
        
        messages.append(AIMessage(content=ai_content)) 
        console.print()
        console.print()
