#Import LangChain chat model
from langchain_openai import ChatOpenAI

#Import LangChain message type
from langchain_core.messages import HumanMessage

#Import library RAG function
from backend.library_pipeline import ask_library_with_sources

#Create LangChain judge model
judge_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

#Create evaluation questions for preloaded video library
questions = [
    "What does the library say about McDonald's food?",
    "What does the library say about Taco Bell?",
    "What health risks are mentioned about fast food?",
    "What does the library say about seed oils?",
    "What does the library say about processed meat?",
    "What does the library say about Chicken McNuggets?",
    "What does the library say about French fries?",
    "What does the library say about anti-aging meals?",
    "What foods are recommended for longevity?",
    "What does the library say about protein intake?",
    "What does the library say about vegetables and health?",
    "What does the library say about sauna benefits?",
    "How can sauna use support health according to the library?",
    "What does the library say about sleep quality?",
    "What habits destroy sleep quality?",
    "What does the library say about caffeine and sleep?",
    "What does the library say about being tired all the time?",
    "What lifestyle habits are connected to low energy?",
    "What does the library say about light exposure before sleep?",
    "What does the library say about improving recovery?"
]

#Loop through questions
for question in questions:

    #Get answer from preloaded video library
    result = ask_library_with_sources(question)

    #Create judge prompt
    judge_prompt = f"""
You are an evaluator for a RAG-based YouTube video library Q&A system.

The system answers questions using a preloaded library of YouTube video transcripts.

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