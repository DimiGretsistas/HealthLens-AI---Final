#Import Chroma vector database
from langchain_chroma import Chroma

#Import shared Supadata client and embeddings
from backend.config import supadata
from backend.config import embeddings

#Import chunking utility
from backend.utils import create_rag_chunks_from_processed_chunks


#Preloaded video library
PRELOADED_VIDEOS = [
    {
        "title": "Taco Bell Video",
        "url": "https://www.youtube.com/watch?v=o9f6EZaCRng"
    },
    {
        "title": "Sauna Video",
        "url": "https://www.youtube.com/watch?v=kiUM92VDI1Y&t=167s"
    },
    {
        "title": "Anti-Aging Meals",
        "url": "https://www.youtube.com/watch?v=0bUieoJ6FI4"
    },
    {
        "title": "McDonald's Video",
        "url": "https://www.youtube.com/watch?v=agF-JwliFw0&t=5s"
    },
    {
        "title": "Why You're Always Tired",
        "url": "https://www.youtube.com/watch?v=3kAiPSEnrHI&t=7s"
    }
]


#Extract YouTube video id
def extract_video_id(youtube_url):
    if "v=" in youtube_url:
        return youtube_url.split("v=")[1].split("&")[0]

    return youtube_url.split("/")[-1].split("?")[0]


#Preload videos into ChromaDB
def preload_videos():
    all_texts = []
    all_metadatas = []

    for video in PRELOADED_VIDEOS:
        print(f"Loading transcript: {video['title']}")
        video_id = extract_video_id(video["url"])
        transcript = supadata.transcript(video["url"])
        processed_chunks = []

        for chunk in transcript.content:
            processed_chunks.append({
                "text": chunk.text,
                "start_time_ms": chunk.offset,
                "duration_ms": chunk.duration,
                "language": chunk.lang
            })

        split_texts, metadatas = create_rag_chunks_from_processed_chunks(
            processed_chunks
        )

        for metadata in metadatas:
            metadata["video_id"] = video_id
            metadata["video_title"] = video["title"]
            metadata["youtube_url"] = video["url"]
            metadata["source_type"] = "preloaded_library"

        all_texts.extend(split_texts)
        all_metadatas.extend(metadatas)

    vectorstore = Chroma.from_texts(
        texts=all_texts,
        embedding=embeddings,
        metadatas=all_metadatas,
        collection_name="preloaded_video_library",
        persist_directory="chroma_db"
    )

    print("Preloaded video library created successfully.")
    print(f"Total chunks stored: {len(all_texts)}")

    return vectorstore


if __name__ == "__main__":
    preload_videos()