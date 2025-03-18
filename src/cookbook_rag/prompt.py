from pydantic import BaseModel

class RecipeRequest(BaseModel):
    ingredients: list[str]
    recipes: list[str]
    strict: bool


from ragbits.core.prompt.prompt import Prompt

class RecipePrompt(Prompt[RecipeRequest]):
    system_prompt = """
        You are a professional cooker.
    """

    user_prompt = """
        CONTEXT: 
        {% for recipe in recipes %}
        [# Recipe {{loop.index}}]
        {{recipe}}
        {% endfor %}
        
        INSTRUCTIONS:
        Choose a recipe to prepare a meal. The list of ingredients you have include:
        {% for ingredient in ingredients %}
            - {{ingredient}}
        {% endfor %}
        You should only use recipes from the provided context
        
        {% if strict %}
        You must only pick a recipe if the list of input ingredients is a subset of the recipe ingredients.
        If you can't find a recipe that meets this criteria, you should respond with 
        "I can't find a recipe matching the ingredients".
        {% else %}
        You should try to pick a recipe that has the most ingredients in common with the list of input ingredients.
        {% endif %}
    """


class RecipePromptPolish(Prompt[RecipeRequest]):
    system_prompt = """
        You are a professional cooker.
    """

    user_prompt = """
        CONTEXT: 
        {% for recipe in recipes %}
        [# Recipe {{loop.index}}]
        {{recipe}}
        {% endfor %}
        
        INSTRUCTIONS:
        Choose a recipe to prepare a meal. The list of ingredients you have include:
        {% for ingredient in ingredients %}
            - {{ingredient}}
        {% endfor %}
        You should only use recipes from the provided context
        
        {% if strict %}
        You must only pick a recipe if the list of input ingredients is a subset of the recipe ingredients.
        If you can't find a recipe that meets this criteria, you should respond with 
        "I can't find a recipe matching the ingredients".
        {% else %}
        You should try to pick a recipe that has the most ingredients in common with the list of input ingredients.
        {% endif %}
        Translate the final recipe into Polish.
    """