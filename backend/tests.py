from backend.video_processor import process_video
from backend.agent import health_agent


#Process test video
print(process_video("https://www.youtube.com/watch?v=3kAiPSEnrHI"))


#Test questions
test_questions = [
    "What is the main topic of the video?",
    "What habits destroy sleep quality?",
    "Why is eating late harmful for sleep?",
    "How does caffeine affect sleep?",
    "Summarize the video."
]


for question in test_questions:

    result = health_agent(question)

    print("\n====================")
    print("QUESTION:")
    print(question)

    print("\nTOOL:")
    print(result["selected_tool"])

    print("\nANSWER:")
    print(result["response"]["answer"])

    print("\nSOURCES:")
    for source in result["response"]["sources"]:
        print(f"- {source['time']} → {source['url']}")