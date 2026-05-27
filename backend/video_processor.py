#Import URL parsing helpers
from urllib.parse import urlparse, parse_qs

#Import Chroma vector database
from langchain_chroma import Chroma

#Import Supadata client and embeddings
from backend.config import supadata
from backend.config import embeddings

#Import shared app state module
import backend.state as state

#Import memory state
import backend.memory as memory

#Import chunking utility
from backend.utils import create_rag_chunks_from_processed_chunks


#Extract YouTube video id safely
def extract_video_id(youtube_url):

    parsed_url = urlparse(youtube_url)

    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")

    if "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)

        if "v" in query_params:
            return query_params["v"][0]

        if "/shorts/" in parsed_url.path:
            return parsed_url.path.split("/shorts/")[1].split("/")[0]

    raise ValueError("Invalid YouTube URL")


#Process any YouTube video
def process_video(youtube_url):

    #Reset memory for new video
    memory.chat_history = []

    #Extract video id safely
    video_id = extract_video_id(youtube_url)

    #Create empty transcript container
    processed_chunks = []

    #Load transcript with Supadata
    transcript = supadata.transcript(youtube_url)

    print("Supadata transcript loaded")

    #Convert Supadata transcript chunks
    for chunk in transcript.content:
        processed_chunks.append({
            "text": chunk.text,
            "start_time_ms": chunk.offset,
            "duration_ms": chunk.duration,
            "language": chunk.lang
        })

    if len(processed_chunks) == 0:
        raise ValueError("No transcript chunks found for this video")

    #Create full transcript text
    full_transcript = " ".join(
        chunk["text"] for chunk in processed_chunks
    )

    #Create RAG chunks and metadata
    split_texts, metadatas = create_rag_chunks_from_processed_chunks(
        processed_chunks
    )

    if len(split_texts) == 0:
        raise ValueError("No RAG chunks created from transcript")

    #Create Chroma vectorstore
    vectorstore = Chroma.from_texts(
        texts=split_texts,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name=f"video_{video_id}"
    )

    #Save video session
    state.video_sessions[video_id] = {
        "vectorstore": vectorstore,
        "processed_chunks": processed_chunks,
        "full_transcript": full_transcript,
        "split_texts": split_texts
    }

    #Set active video
    state.current_video_id = video_id

    #Return status
    return f"Video processed successfully. Total chunks: {len(split_texts)}"