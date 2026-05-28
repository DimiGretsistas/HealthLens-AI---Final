#Conversation memory
chat_history = []


#Save interaction to memory
def save_to_memory(question, answer):
    if isinstance(answer, dict):
        if "answer" in answer:
            answer = answer["answer"]
        elif "response" in answer and "answer" in answer["response"]:
            answer = answer["response"]["answer"]
        else:
            answer = str(answer)

    chat_history.append({
        "role": "user",
        "content": question
    })

    chat_history.append({
        "role": "assistant",
        "content": answer
    })

#Convert memory into readable text
def get_chat_history():
    recent_messages = chat_history[-20:]
    history_text = ""

    for message in recent_messages:
        if message["role"] == "user":
            history_text += f"User: {message['content']}\n"
        elif message["role"] == "assistant":
            history_text += f"Assistant: {message['content']}\n"
    return history_text