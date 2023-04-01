import os
import requests
import json

from dotenv import load_dotenv, find_dotenv


class FoodApi:
    """
    FoodApi that returns random or specific repices
    """

    api_key = None
    payload = {}
    headers = {}

    def __init__(self):
        load_dotenv(find_dotenv())
        self.api_key = os.getenv('SPOONACULAR_API_KEY')

    def food_api_random_request(self):
        """
        Arguments:
        None

        Returns:
        - name of the recipe as string
        - dictionary containing the name of a used ingredient with the needed measures
        - array of steps for the recipe
        """

        url = 'https://api.spoonacular.com/recipes/random?number=1&limitLicense=true&apiKey=' + self.api_key

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        response_json = json.loads(response.text)

        recipe = response_json['recipes'][0]
        analyzed_instructions = recipe['analyzedInstructions'][0]['steps']
        extended_ingredients = recipe['extendedIngredients']

        recipe_name = recipe['title']
        ingredient_dic = self.extract_ingredients_to_dictionary(extended_ingredients)
        step_descriptions = self.extract_steps_to_array(analyzed_instructions)

        return recipe_name, ingredient_dic, step_descriptions

    def extract_steps_to_array(self, analyzed_instructions):
        step_descriptions = []
        for steps in analyzed_instructions:
            step_descriptions.append(steps['step'])

        return step_descriptions

    def extract_ingredients_to_dictionary(self, extended_ingredients):
        ingredient_dic = {}
        for ingredient in extended_ingredients:
            ingredient_name = ingredient['name']
            ingredient_amount = ingredient['measures']['metric']['amount']
            ingredient_unit = ingredient['measures']['metric']['unitLong']
            ingredient_dic[ingredient_name] = self.convert_ingredient_measures_to_string(ingredient_amount,
                                                                                         ingredient_unit)

        return ingredient_dic

    def convert_ingredient_measures_to_string(self, ingredient_amount, ingredient_unit):
        ingredient_amount = self.convert_float_to_int_if_valid(ingredient_amount)
        ingredient_string = str(ingredient_amount)

        if ingredient_unit:
            ingredient_string += ' ' + ingredient_unit

        return ingredient_string

    def convert_float_to_int_if_valid(self, float_value):
        if float_value.is_integer():
            return int(float_value)
        return float_value
