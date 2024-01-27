
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser 
from rich.console import Console
from rich.prompt import Prompt


def create_db_from_youtube_video_url(url: str, language: str, console: Console) -> FAISS:
    embeddings = OpenAIEmbeddings()

    console.print("[cyan]Start by checking if transcripts availabled ...")

    loader = YoutubeLoader.from_youtube_url(url, language=language)
    console.print("[cyan]Import transcripts recordings ...")

    transcript = loader.load()

    console.print("[cyan]Transcripts received  ...")

    console.print("[cyan]Start splitting transcripts ...")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    console.print("[cyan]Documents created !")
    console.print()
    return FAISS.from_documents(docs, embeddings)


def get_response_from_query(db: FAISS, query: str, k: int, console: Console):

    console = Console()

    # docs = db.similarity_search(query, k=k)
    # docs_page_content = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(temperature=0.1)

    template="""
        You are a helpful assistant that that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {
            "docs": itemgetter("question") | db.as_retriever(),
            "question": itemgetter("question"),
        } 
        | prompt
        | llm
        | StrOutputParser()
    )

    console.print("[blue][b]Assistant :[/b][/blue]")
    
    for chunk in chain.stream({"question": query}):
        console.print(chunk, end="", style="green")
    

def chat_with_yt_video(url: str, language: str):

    console = Console()

    #video_url = "https://www.youtube.com/watch?v=NYSWn1ipbgg" "https://www.youtube.com/watch?v=L_Guz73e6fw"
    db = create_db_from_youtube_video_url(url, language, console)

    console.print("[green]You can now ask questions about the video's transcript.\n")

    while True:
        content = Prompt.ask("[red][b]User[b/]")
        console.print()

        get_response_from_query(db, content, k=5, console=console)

        console.print()
        console.print()
