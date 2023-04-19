import os
import requests
import json
import random
from dotenv import load_dotenv, find_dotenv


class FoodApi:
    """
    FoodApi that returns random or specific recipe
    """

    api_key = None
    payload = {}
    headers = {}

    def __init__(self):
        load_dotenv(find_dotenv())
        self.api_key = os.getenv('SPOONACULAR_API_KEY')

    def food_api_find_by_ingredients_request(self, ingredient_list, ranking=1):
        """
        Arguments:
        - list containing all ingredients
        - Whether to maximize used ingredients (1) or minimize missing ingredients (2) first. (Default: 2)

        Returns:
        - name of the recipe as string
        - dictionary containing the name of a used ingredient with the needed measures
        - array of steps for the recipe (it is possible that no instructions are available)
        """

        ingredients_as_csv = self.convert_ingredient_list_to_csv(ingredient_list)

        url = 'https://api.spoonacular.com/recipes/findByIngredients?number=25&limitLicense=true&ranking=' + \
              str(ranking) + '&ignorePantry=true&apiKey=' + self.api_key + '&ingredients=' + ingredients_as_csv

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        response_json = json.loads(response.text)
        recipe_id = response_json[random.randint(0, len(response_json)-1)]['id']

        return self.extract_recipe_information(recipe_id)

    def food_api_random_request(self):
        """
        Arguments:
        None

        Returns:
        - name of the recipe as string
        - dictionary containing the name of a used ingredient with the needed measures
        - array of steps for the recipe (it is possible that no instructions are available)
        """

        url = 'https://api.spoonacular.com/recipes/random?number=25&limitLicense=true&apiKey=' + self.api_key

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        response_json = json.loads(response.text)
        recipe_id = response_json['recipes'][random.randint(0, len(response_json['recipes'])-1)]['id']

        return self.extract_recipe_information(recipe_id)

    def extract_recipe_information(self, recipe_id):

        url = 'https://api.spoonacular.com/recipes/' + str(recipe_id) + '/information?apiKey=' + self.api_key

        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        recipe = json.loads(response.text)

        analyzed_instructions = []
        if recipe['analyzedInstructions']:
            analyzed_instructions = recipe['analyzedInstructions'][0]['steps']
        extended_ingredients = recipe['extendedIngredients']

        recipe_name = recipe['title']
        ingredient_dic = self.extract_ingredients_to_dictionary(extended_ingredients)
        step_descriptions = self.extract_steps_to_array(analyzed_instructions)

        return recipe_name, ingredient_dic, step_descriptions

    def convert_ingredient_list_to_csv(self, ingredient_list):
        return ",".join(ingredient_list)

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
