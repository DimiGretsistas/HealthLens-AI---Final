#Import RAG question answering function
from backend.rag_pipeline import ask_video_with_sources


#Tool 1: Transcript Question Answering Tool
def video_qa_tool(question):

    #Use current RAG system
    return ask_video_with_sources(question)


#Tool 2: Summary tool
def summary_tool():
    
    #Summarize video using RAG system
    return ask_video_with_sources(
        "Summarize the main ideas of this video."
    )


#Tool 3: Ingredient extraction tool
def ingredient_extraction_tool():

    #Extract foods and ingredients from video
    return ask_video_with_sources(
        "List all foods, ingredients, oils, supplements, and unhealthy foods mentioned in the video."
    )


#Tool 4: Macro calculator tool
def macro_calculator_tool(total_calories):

    #Calculate macro calories
    protein_calories = total_calories * 0.25
    carbs_calories = total_calories * 0.35
    fat_calories = total_calories * 0.40

    #Convert macro calories to grams
    protein_grams = protein_calories / 4
    carbs_grams = carbs_calories / 4
    fat_grams = fat_calories / 9

    #Return macro breakdown
    return {
        "total_calories": total_calories,
        "protein_grams": round(protein_grams, 1),
        "carbs_grams": round(carbs_grams, 1),
        "fat_grams": round(fat_grams, 1)
    }


#Tool 5: Health safety tool
def health_safety_tool(user_input):

    #Ask safety-related question to the video
    result = ask_video_with_sources(user_input)

    #Add safety note
    result["answer"] += "\n\nNote: This is based on the video transcript and is not medical advice."

    return result


#Tool 6: Meal suggestion tool
def meal_suggestion_tool():

    #Generate meal suggestions inspired by transcript foods
    return ask_video_with_sources(
        """
        Suggest 3 healthy meal ideas inspired by the foods,
        ingredients, and nutrition principles mentioned in the video.

        Clearly mention that these meals are inspired by the video
        and are not medical advice.
        """
    )


#Tool 7: Shopping list tool
def shopping_list_tool():

    #Create shopping list from transcript ingredients
    return ask_video_with_sources(
        """
        Create a clear shopping list using only the foods,
        ingredients, oils, and healthy items mentioned in the video.

        Group the list into categories:
        - vegetables
        - legumes and grains
        - fruits
        - nuts and seeds
        - oils
        - herbs and extras

        Do not include items that are not mentioned in the video.
        """
    )