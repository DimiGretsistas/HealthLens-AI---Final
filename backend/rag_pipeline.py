#Import LangChain prompt template
from langchain_core.prompts import ChatPromptTemplate

#Import output parser
from langchain_core.output_parsers import StrOutputParser

#Import shared LLM
from backend.config import llm

#Import memory function
from backend.memory import get_chat_history

#Import shared app state module
import backend.state as state

#Import utility function
from backend.utils import create_youtube_timestamp_link


#Prompt template for transcript question answering
rag_prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant answering questions about a YouTube video.

Use ONLY the provided transcript context.

If the answer is not contained in the transcript,
say that the video does not contain enough information.

Chat History:
{chat_history}

Transcript Context:
{context}

Question:
{question}

Answer:
""")


#LCEL chain
#Prompt -> LLM -> Output Parser
rag_chain = rag_prompt | llm | StrOutputParser()


#Retrieve similar transcript chunks
def ask_video_with_sources(question):

    #Check if a video was processed first
    if state.current_video_id is None:
        return {
            "answer": "Please process a YouTube video first.",
            "sources": []
        }

    #Get current video vectorstore
    current_vectorstore = (
        state.video_sessions[state.current_video_id]["vectorstore"]
    )

    #Retrieve similar chunks
    retrieved_docs = current_vectorstore.similarity_search_with_score(
        question,
        k=10
    )

    #Similarity threshold
    SIMILARITY_THRESHOLD = 2.5

    #Store filtered documents
    filtered_docs = []

    #Store unique chunks
    seen_texts = set()

    #Filter retrieved chunks
    for doc, score in retrieved_docs:

        #Skip weak matches
        if score >= SIMILARITY_THRESHOLD:
            continue

        #Skip duplicate chunks
        if doc.page_content in seen_texts:
            continue

        #Save unique chunk
        seen_texts.add(doc.page_content)

        #Save filtered document
        filtered_docs.append(doc)

    #Combine transcript chunks into one context
    context = "\n\n".join([
        doc.page_content for doc in filtered_docs
    ])

    #Run LangChain RAG chain
    answer = rag_chain.invoke({
        "chat_history": get_chat_history(),
        "context": context,
        "question": question
    })

    #Create source links
    sources = []

    for doc in filtered_docs:

        source = create_youtube_timestamp_link(
            doc.metadata["start_time_ms"]
        )

        #Avoid duplicate sources
        if source not in sources:
            sources.append(source)

    #Remove sources if answer says there is not enough information
    if "video does not contain enough information" in answer.lower():
        sources = []

    #Return final answer and sources
    return {
        "answer": answer,
        "sources": sources[:3]
    }