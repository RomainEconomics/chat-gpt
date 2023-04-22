import sys
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    BaseMessage
)
from rich.prompt import Prompt

from typing import Any
from rich.live import Live
from langchain.callbacks import CallbackManager
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    BaseMessage
)
from chat_gpt.utils.callbacks import StreamingTerminalCallbackHandler, rich_streaming_display



def create_db_from_youtube_video_url(url: str, language: str, console: Console) -> FAISS:
    embeddings = OpenAIEmbeddings()

    console.print("[cyan]Start by checking if transcripts availabled ...")

    loader = YoutubeLoader.from_youtube_url(url, language=language)
    console.print("[cyan]Import transcripts recordings ...")

    transcript = loader.load()

    console.print("[cyan]Transcripts received  ...")

    console.print("[cyan]Start splitting transcripts ...")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    console.print("[cyan]Documents created !")
    console.print()
    return FAISS.from_documents(docs, embeddings)


def get_response_from_query(db, query, k, console):

    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    stream_manager = CallbackManager(
            [StreamingTerminalCallbackHandler(output_callback= lambda x: rich_streaming_display(x, live_chat))]
        )
    llm = ChatOpenAI(temperature=0, streaming=True, callback_manager=stream_manager, verbose=True)

    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful assistant that that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    console.print("[blue][b]Assistant :[/b][/blue]")
    with Live(console=console, refresh_per_second=2) as live_chat:
        response = chain.run(question=query, docs=docs_page_content)
    
    response = response.replace("\n", "")
    return response, docs


def chat_with_yt_video(url: str, language: str):

    console = Console()

    #video_url = "https://www.youtube.com/watch?v=NYSWn1ipbgg" "https://www.youtube.com/watch?v=L_Guz73e6fw"
    db = create_db_from_youtube_video_url(url, language, console)

    console.print("[green]You can now ask questions about the video's transcript.\n")

    while True:
        content = Prompt.ask("[red][b]User [b/]: ")
        console.print()

        response, docs = get_response_from_query(db, content, k=5, console=console)
        console.print()
