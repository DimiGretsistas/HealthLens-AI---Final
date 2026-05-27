#Import LangChain prompt template
from langchain_core.prompts import ChatPromptTemplate

#Import output parser
from langchain_core.output_parsers import StrOutputParser

#Import Chroma vector database
from langchain_chroma import Chroma

#Import shared LLM and embeddings
from backend.config import llm
from backend.config import embeddings

#Import utility function
from backend.utils import create_youtube_timestamp_link


#Load preloaded Chroma collection only when needed
def get_library_vectorstore():

    return Chroma(
        collection_name="preloaded_video_library",
        embedding_function=embeddings,
        persist_directory="chroma_db"
    )


#Prompt for preloaded video library Q&A
library_prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant answering questions using a preloaded YouTube video library.

Use ONLY the provided transcript context.

If the answer is not contained in the transcript context,
say that the preloaded video library does not contain enough information.

Transcript Context:
{context}

Question:
{question}

Answer:
""")


#LCEL chain
library_chain = library_prompt | llm | StrOutputParser()


#Ask question across preloaded video library
def ask_library_with_sources(question):

    #Load Chroma collection only when library mode is used
    library_vectorstore = get_library_vectorstore()

    #Retrieve similar chunks from preloaded library
    retrieved_docs = library_vectorstore.similarity_search_with_score(
        question,
        k=8
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

    #Return fallback if no relevant chunks were found
    if not filtered_docs:

        return {
            "answer": "The preloaded video library does not contain enough information.",
            "sources": []
        }

    #Combine transcript chunks into context
    context = "\n\n".join([
        f"Video: {doc.metadata.get('video_title')}\n{doc.page_content}"
        for doc in filtered_docs
    ])

    #Run library chain
    answer = library_chain.invoke({
        "context": context,
        "question": question
    })

    #Create source links
    sources = []

    for doc in filtered_docs:

        video_id = doc.metadata.get("video_id")
        start_time_ms = doc.metadata.get("start_time_ms")
        video_title = doc.metadata.get("video_title")

        source = create_youtube_timestamp_link(
            start_time_ms,
            video_id
        )

        source["title"] = video_title

        #Avoid duplicate sources
        if source not in sources:
            sources.append(source)

    #Remove sources if answer says there is not enough information
    if "preloaded video library does not contain enough information" in answer.lower():
        sources = []

    #Return answer and sources
    return {
        "answer": answer,
        "sources": sources[:3]
    }