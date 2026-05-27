#Import LangChain chat model
from langchain_openai import ChatOpenAI

#Import LangChain message type
from langchain_core.messages import HumanMessage

#Import project functions
from backend.video_processor import process_video
from backend.rag_pipeline import ask_video_with_sources


#Create LangChain judge model
judge_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


#Process test video
process_video("https://www.youtube.com/watch?v=3kAiPSEnrHI")


#Create evaluation questions
questions = [
    "What is the main topic of the video?",
    "Which habit was mentioned first?",
    "What does the video say about caffeine?",
    "What does the video say about bedroom temperature?",
    "What does the video say about noise and sleep?",
    "What does the video say about eating too late?",
    "What does the video recommend for winding down before bed?",
    "What does the video say about light exposure before sleep?",
    "What are the top 3 sleep mistakes mentioned?",
    "What does the video say about drinking alcohol before sleep?"
]


#Loop through questions
for question in questions:

    #Get answer from RAG system
    result = ask_video_with_sources(question)

    #Create judge prompt
    judge_prompt = f"""
You are an evaluator for a RAG-based YouTube video Q&A system.

Evaluate the answer using ONLY the provided sources.

Evaluation criteria:

1. Faithfulness:
Is the answer supported by the provided sources?

2. Relevance:
Does the answer directly answer the question?

3. Clarity:
Is the answer clear and easy to understand?

4. Hallucination Safety:
Does the answer add unsupported claims that are not grounded in the sources?
Score 5/5 if there are no hallucinations.
Score 1/5 if the answer contains major unsupported claims.

Question:
{question}

Answer:
{result["answer"]}

Sources:
{result["sources"]}

Return your evaluation in this exact format:

Faithfulness: X/5
Relevance: X/5
Clarity: X/5
Hallucination Safety: X/5
Feedback: short feedback
"""

    #Run LangChain judge evaluation
    evaluation = judge_llm.invoke([
        HumanMessage(content=judge_prompt)
    ])

    #Print result
    print("\n====================")
    print("QUESTION:")
    print(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    print(result["sources"])

    print("\nEVALUATION:")
    print(evaluation.content)