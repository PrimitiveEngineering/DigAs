""" test_main
    * all basic-tests for Google-Maps-API are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       22.03.2023
    version:    0.0.1
    license:    MIT
"""
import unittest
from cooking.foodApi import FoodApi

FA = FoodApi()


class TestFoodApi(unittest.TestCase):
    # def test_food_api_find_by_ingredients_request(self):
    #     FA.food_api_find_by_ingredients_request(["banana", "egg"])
    #
    # def test_food_api_random_request(self):
    #     # self.assertEqual(True, False)  # add assertion here

    # def test_extract_recipe_information(self):
    #     correct_string = ('Tangy & Savory Mexican Soup', {'avocado': '1', 'carrots': '2', 'cilantro': '8 servings', 'garlic cloves': '6', 'ground beef': '907.185 grams', 'lime juice': '118.294 milliliters', 'oregano': '8 servings', 'bell peppers': '2', 'chili flakes': '0.5 teaspoons', 'onion': '1 large', 'sea salt & pepper': '8 servings', 'cream': '8 servings', 'tomato paste': '236.588 milliliters', 'tortilla chips': '8 servings', 'combination of water': '1.893 liters', 'zucchini': '3', 'cortido': '8 servings'}, ['Lightly brown beef or chicken, make sure there is still some pink. If you brown it too much it will taste "dry" in the soup.Bring stock to a boil with tomato paste/sauce. Stir in meat, garlic, chili flakes, zucchini, carrots, onions &amp; bell peppers. Simmer for about 15-30 minutes or till veggies are tender, but still slightly crunchy.', 'Add in lime juice and season to taste with oregano, rosemary, thyme, sea salt &amp; pepper.', 'Serve with garnishes.'])
    #
    #     self.assertEqual(correct_string,FA.extract_recipe_information(1))

    def test_convert_ingredient_list_to_csv(self):
        correct_string = "banana,egg"
        test_array = ["banana", "egg"]
        self.assertEqual(correct_string, FA.convert_ingredient_list_to_csv(test_array))

    def test_extract_steps_to_array(self):
        correct_instructions = [
            'In a small saucepan over medium heat, add the blackberries, Meyer lemon zest, sugar, and water.Stir to combine and cook until the water starts to thicken and the berries lose their shape, stirring occasionally. This should take about 10 minute.',
            'Remove from the heat and set aside.In a medium bowl, whisk together the ricotta cheese, Meyer lemon zest, juice, sugar and egg yolks.Gradually stir in the flour until just combined.Using a stand or hand mixer, whisk the egg whites with a pinch of salt until stiff peaks are formed.Take a large spoonful of the eggs whites and stir it into the batter. With the remaining eggs whites, fold in half, slowly turning the bowl while you fold. It is fine if there are some white streaks left in the batter before you add the second half. Fold in the remaining eggs white and set the batter aside while you heat up a griddle or non-stick pan on medium heat.',
            'Add some butter to the pre-heated pan, and swirl to coat.',
            'Add about a 1/4 cup of batter and cook until bubbles start to form on the top and the edges begin to brown slightly.Flip the pancakes and cook for an additional minute.',
            'Remove and keep warm, while you repeat with the remaining batter.',
            'Serve the pancakes with the blackberry compote and if you like a little pure maple syrup.']
        test_instructions = [{'number': 1,
                              'step': 'In a small saucepan over medium heat, add the blackberries, Meyer lemon zest, sugar, and water.Stir to combine and cook until the water starts to thicken and the berries lose their shape, stirring occasionally. This should take about 10 minute.',
                              'ingredients': [{'id': 9042, 'name': 'blackberries', 'localizedName': 'blackberries',
                                               'image': 'blackberries.jpg'},
                                              {'id': 1009150, 'name': 'meyer lemon', 'localizedName': 'meyer lemon',
                                               'image': 'lemon.png'},
                                              {'id': 1009054, 'name': 'berries', 'localizedName': 'berries',
                                               'image': 'berries-mixed.jpg'},
                                              {'id': 19335, 'name': 'sugar', 'localizedName': 'sugar',
                                               'image': 'sugar-in-bowl.png'},
                                              {'id': 14412, 'name': 'water', 'localizedName': 'water',
                                               'image': 'water.png'}], 'equipment': [
                {'id': 404669, 'name': 'sauce pan', 'localizedName': 'sauce pan', 'image': 'sauce-pan.jpg'}],
                              'length': {'number': 10, 'unit': 'minutes'}}, {'number': 2,
                                                                             'step': 'Remove from the heat and set aside.In a medium bowl, whisk together the ricotta cheese, Meyer lemon zest, juice, sugar and egg yolks.Gradually stir in the flour until just combined.Using a stand or hand mixer, whisk the egg whites with a pinch of salt until stiff peaks are formed.Take a large spoonful of the eggs whites and stir it into the batter. With the remaining eggs whites, fold in half, slowly turning the bowl while you fold. It is fine if there are some white streaks left in the batter before you add the second half. Fold in the remaining eggs white and set the batter aside while you heat up a griddle or non-stick pan on medium heat.',
                                                                             'ingredients': [
                                                                                 {'id': 1036, 'name': 'ricotta cheese',
                                                                                  'localizedName': 'ricotta cheese',
                                                                                  'image': 'ricotta.png'},
                                                                                 {'id': 1009150, 'name': 'meyer lemon',
                                                                                  'localizedName': 'meyer lemon',
                                                                                  'image': 'lemon.png'},
                                                                                 {'id': 1124, 'name': 'egg whites',
                                                                                  'localizedName': 'egg whites',
                                                                                  'image': 'egg-white.jpg'},
                                                                                 {'id': 1125, 'name': 'egg yolk',
                                                                                  'localizedName': 'egg yolk',
                                                                                  'image': 'egg-yolk.jpg'},
                                                                                 {'id': 20081,
                                                                                  'name': 'all purpose flour',
                                                                                  'localizedName': 'all purpose flour',
                                                                                  'image': 'flour.png'},
                                                                                 {'id': 1019016, 'name': 'juice',
                                                                                  'localizedName': 'juice',
                                                                                  'image': 'apple-juice.jpg'},
                                                                                 {'id': 19335, 'name': 'sugar',
                                                                                  'localizedName': 'sugar',
                                                                                  'image': 'sugar-in-bowl.png'},
                                                                                 {'id': 1123, 'name': 'egg',
                                                                                  'localizedName': 'egg',
                                                                                  'image': 'egg.png'},
                                                                                 {'id': 2047, 'name': 'salt',
                                                                                  'localizedName': 'salt',
                                                                                  'image': 'salt.jpg'}], 'equipment': [
                {'id': 404628, 'name': 'hand mixer', 'localizedName': 'hand mixer', 'image': 'hand-mixer.png'},
                {'id': 404645, 'name': 'frying pan', 'localizedName': 'frying pan', 'image': 'pan.png'},
                {'id': 404661, 'name': 'whisk', 'localizedName': 'whisk', 'image': 'whisk.png'},
                {'id': 404783, 'name': 'bowl', 'localizedName': 'bowl', 'image': 'bowl.jpg'}]},
                             {'number': 3, 'step': 'Add some butter to the pre-heated pan, and swirl to coat.',
                              'ingredients': [{'id': 1001, 'name': 'butter', 'localizedName': 'butter',
                                               'image': 'butter-sliced.jpg'}], 'equipment': [
                                 {'id': 404645, 'name': 'frying pan', 'localizedName': 'frying pan',
                                  'image': 'pan.png'}]}, {'number': 4,
                                                          'step': 'Add about a 1/4 cup of batter and cook until bubbles start to form on the top and the edges begin to brown slightly.Flip the pancakes and cook for an additional minute.',
                                                          'ingredients': [], 'equipment': []},
                             {'number': 5, 'step': 'Remove and keep warm, while you repeat with the remaining batter.',
                              'ingredients': [], 'equipment': []}, {'number': 6,
                                                                    'step': 'Serve the pancakes with the blackberry compote and if you like a little pure maple syrup.',
                                                                    'ingredients': [{'id': 19911, 'name': 'maple syrup',
                                                                                     'localizedName': 'maple syrup',
                                                                                     'image': 'maple-syrup.png'},
                                                                                    {'id': 9042, 'name': 'blackberries',
                                                                                     'localizedName': 'blackberries',
                                                                                     'image': 'blackberries.jpg'},
                                                                                    {'id': 0, 'name': 'compote',
                                                                                     'localizedName': 'compote',
                                                                                     'image': ''}], 'equipment': []}]

        self.assertEqual(correct_instructions, FA.extract_steps_to_array(test_instructions))

    def test_extract_ingredients_to_dictionary(self):
        correct_dict = {'banana': '1 small', 'peanut butter': '1 Tbsp',
                        'vanilla almond milk': '177.441 milliliters'}
        test_ingredients = [
            {'id': 9040, 'aisle': 'Produce', 'image': 'bananas.jpg', 'consistency': 'SOLID', 'name': 'banana',
             'nameClean': 'banana', 'original': '1 small frozen ripe banana, peeled',
             'originalName': 'frozen ripe banana, peeled', 'amount': 1.0, 'unit': 'small',
             'meta': ['frozen', 'ripe', 'peeled'],
             'measures': {'us': {'amount': 1.0, 'unitShort': 'small', 'unitLong': 'small'},
                          'metric': {'amount': 1.0, 'unitShort': 'small', 'unitLong': 'small'}}},
            {'id': 16098, 'aisle': 'Nut butters, Jams, and Honey', 'image': 'peanut-butter.png', 'consistency': 'SOLID',
             'name': 'peanut butter', 'nameClean': 'peanut butter', 'original': '1 tbsp Peanut Butter',
             'originalName': 'Peanut Butter', 'amount': 1.0, 'unit': 'tbsp', 'meta': [],
             'measures': {'us': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'},
                          'metric': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'}}},
            {'id': 93607, 'aisle': 'Milk, Eggs, Other Dairy', 'image': 'almond-milk.png', 'consistency': 'LIQUID',
             'name': 'vanilla almond milk', 'nameClean': 'almond milk',
             'original': '3/4 cup unsweetened vanilla almond milk', 'originalName': 'unsweetened vanilla almond milk',
             'amount': 0.75, 'unit': 'cup', 'meta': ['unsweetened'],
             'measures': {'us': {'amount': 0.75, 'unitShort': 'cups', 'unitLong': 'cups'},
                          'metric': {'amount': 177.441, 'unitShort': 'ml', 'unitLong': 'milliliters'}}}
        ]

        self.assertEqual(correct_dict, FA.extract_ingredients_to_dictionary(test_ingredients))

    def test_convert_ingredient_measures_to_string(self):
        correct_string = "42 ToMaszinen"
        self.assertEqual(correct_string, FA.convert_ingredient_measures_to_string(42.0, "ToMaszinen"))

    def test_convert_float_to_int_if_valid_true(self):
        correct_number = 42
        float_number = 42.00
        self.assertEqual(correct_number, FA.convert_float_to_int_if_valid(float_number))

    def test_convert_float_to_int_if_valid_false(self):
        correct_number = 42.69
        float_number = 42.69
        self.assertEqual(correct_number, FA.convert_float_to_int_if_valid(float_number))
