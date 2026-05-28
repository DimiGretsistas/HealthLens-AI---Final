#Import regex
import re

#Import prompt template
from langchain_core.prompts import ChatPromptTemplate

#Import output parser
from langchain_core.output_parsers import StrOutputParser

#Import shared LLM
from backend.config import llm

#Import memory functions
from backend.memory import save_to_memory
from backend.memory import get_chat_history

#Import shared app state
import backend.state as state

#Import tools
from backend.tools import video_qa_tool
from backend.tools import summary_tool
from backend.tools import ingredient_extraction_tool
from backend.tools import macro_calculator_tool
from backend.tools import health_safety_tool
from backend.tools import meal_suggestion_tool
from backend.tools import shopping_list_tool


#Create router prompt
router_prompt = ChatPromptTemplate.from_template("""
You are an AI routing system.

Your job is to choose the BEST tool for the user request.
If the selected tool generates a user-facing answer, the final answer should be in the same language as the user's question.
                                                 
Available tools:
- video_qa_tool
- summary_tool
- ingredient_extraction_tool
- macro_calculator_tool
- health_safety_tool
- meal_suggestion_tool
- shopping_list_tool

IMPORTANT:
- Questions about unhealthy foods, toxins, harmful ingredients, bad oils, unsafe cookware, chemicals, supplements, creatine, vitamins, or safety MUST use health_safety_tool.
- Do NOT use video_qa_tool for these topics.
- Questions asking for a shopping list, grocery list, or groceries MUST use shopping_list_tool.
- Do NOT use video_qa_tool for shopping list requests.

Routing rules:
- Questions about longevity foods or foods that help longevity -> video_qa_tool
- Questions asking what was mentioned earlier, previous answer, previous ingredient, or healthy fat source mentioned before -> video_qa_tool
- Ingredients, foods, vegetables, fruits, grains, seeds, or recipe ingredients -> ingredient_extraction_tool
- Unhealthy foods, bad oils, harmful ingredients, unsafe cooking, cookware, chemicals, toxins, or what to avoid -> health_safety_tool
- Calories, macros, protein, carbs, fat, or macro ratio -> macro_calculator_tool
- Supplements, creatine, vitamins, minerals, or protein powder -> health_safety_tool
- Meal ideas, recipes, meal prep, or what to cook -> meal_suggestion_tool
- Shopping list or groceries -> shopping_list_tool
- Summary or overview -> summary_tool
- General question about the video -> video_qa_tool

Rules:
- Return ONLY the tool name.
- Do not explain anything.
- Do not return extra text.

Previous conversation:
{chat_history}

Current user request:
{user_input}
""")


#Create router chain
router_chain = router_prompt | llm | StrOutputParser()

#Create Multi-Tool Health Agent
def health_agent(user_input):

    #Load previous conversation
    chat_history_text = get_chat_history()

    #Debug current video
    print("CURRENT VIDEO:", state.current_video_id)

    #Classify user request
    tool_choice = router_chain.invoke({
        "user_input": user_input,
        "chat_history": chat_history_text
    }).strip()

    #Debug selected tool
    print("Selected tool:", tool_choice)

    #Video Q&A tool
    if tool_choice == "video_qa_tool":
        result = video_qa_tool(user_input)

    #Summary tool
    elif tool_choice == "summary_tool":
        result = summary_tool()

    #Ingredient extraction tool
    elif tool_choice == "ingredient_extraction_tool":
        result = ingredient_extraction_tool()

    #Macro calculator tool
    elif tool_choice == "macro_calculator_tool":

        calorie_match = re.search(r"\d+", user_input)

        total_calories = (
            int(calorie_match.group())
            if calorie_match
            else 2200
        )

        result = macro_calculator_tool(total_calories)

    #Health safety tool
    elif tool_choice == "health_safety_tool":
        result = health_safety_tool(user_input)

    #Meal suggestion tool
    elif tool_choice == "meal_suggestion_tool":
        result = meal_suggestion_tool()

    #Shopping list tool
    elif tool_choice == "shopping_list_tool":
        result = shopping_list_tool()

    #Fallback tool
    else:
        tool_choice = "video_qa_tool"
        result = video_qa_tool(user_input)

    #Save interaction into memory
    save_to_memory(user_input, result)

    #Return final response
    return {
        "selected_tool": tool_choice,
        "response": result
    }