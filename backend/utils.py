#Import shared app state
import backend.state as state


#Create RAG chunks from transcript chunks
def create_rag_chunks_from_processed_chunks(
    processed_chunks,
    max_chars=2000,
    overlap_chars=300
):

    #Store final RAG chunks
    rag_texts = []

    #Store chunk metadata
    rag_metadatas = []

    #Current chunk text
    current_text = ""

    #Current chunk start time
    current_start_time = None

    #Current chunk duration
    current_duration = 0

    #Default language
    current_language = "en"

    #Loop through transcript chunks
    for chunk in processed_chunks:

        chunk_text = chunk["text"]

        #Set initial chunk metadata
        if current_start_time is None:
            current_start_time = chunk["start_time_ms"]
            current_language = chunk["language"]

        #Check max chunk size
        if len(current_text) + len(chunk_text) > max_chars:

            #Save chunk text
            rag_texts.append(current_text.strip())

            #Save metadata
            rag_metadatas.append({
                "start_time_ms": current_start_time,
                "duration_ms": current_duration,
                "language": current_language
            })

            #Create overlap between chunks
            current_text = (
                current_text[-overlap_chars:]
                + " "
                + chunk_text
            )

            #Reset metadata
            current_start_time = chunk["start_time_ms"]
            current_duration = chunk["duration_ms"]

        else:

            #Append transcript text
            current_text += " " + chunk_text

            #Add duration
            current_duration += chunk["duration_ms"]

    #Save final chunk
    if current_text.strip():

        rag_texts.append(current_text.strip())

        rag_metadatas.append({
            "start_time_ms": current_start_time,
            "duration_ms": current_duration,
            "language": current_language
        })

    #Return chunked texts and metadata
    return rag_texts, rag_metadatas


#Convert milliseconds to YouTube timestamp link
def create_youtube_timestamp_link(start_time_ms, video_id=None):

    #Use provided video id or current active video id
    selected_video_id = video_id or state.current_video_id

    #Convert milliseconds to seconds
    seconds = int(start_time_ms / 1000)

    #Convert to readable timestamp
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    #Format timestamp
    readable_time = f"{minutes:02d}:{remaining_seconds:02d}"

    #Create YouTube timestamp URL
    url = (
        f"https://www.youtube.com/watch?"
        f"v={selected_video_id}&t={seconds}s"
    )

    #Return timestamp data
    return {
        "time": readable_time,
        "url": url
    }