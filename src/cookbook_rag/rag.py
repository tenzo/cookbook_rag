import asyncio

from ragbits.core.llms.litellm import LiteLLM

from cookbook_rag.ingest import document_search
from cookbook_rag.prompt import RecipeRequest, RecipePromptPolish

llm = LiteLLM("gpt-4")


async def find_recipe_for_ingredients(ingredients: list[str], strict: bool = False) -> str:
    """Main RAG query function. Given a list of ingredients, find a recipes that use them.
    Construct the extended prompt using the context retrieved. Return the generated recipe.
    """
    ingredients_str = ", ".join(ingredients)
    elements = await document_search.search(ingredients_str)
    recipes = [element.text_representation for element in elements if element.text_representation]
    print(f"Found {len(recipes)} recipes")
    prompt = RecipePromptPolish(
        RecipeRequest(
            recipes=recipes,
            ingredients=ingredients,
            strict=strict,
        )
    )
    print(f"Rendered prompt:\nSystem:{prompt.rendered_system_prompt}\nUser:{prompt.rendered_user_prompt}")
    print("###Generating recipe...###\n\n\n##############")
    return await llm.generate(prompt)

if __name__ == '__main__':
    ingredients = ["flour", "sugar", "eggs", "milk"]
    print(asyncio.run(find_recipe_for_ingredients(ingredients, strict=True)))
    # ingredients = ["pepper", "cucumber", "olive oil"]
    # print(asyncio.run(find_recipe_for_ingredients(ingredients, strict=False)))
