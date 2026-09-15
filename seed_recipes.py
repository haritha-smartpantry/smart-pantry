from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["smart_pantry"]

recipe_collection = db["recipes"]

# Remove old recipes
recipe_collection.delete_many({})

recipes = [

    # CAPSICUM
    {
        "recipe_name": "Capsicum Masala",
        "ingredients": ["Capsicum", "Onion", "Tomato"],
        "instructions": "Sauté onion and tomato. Add capsicum and spices. Cook until soft."
    },
    {
        "recipe_name": "Capsicum Rice",
        "ingredients": ["Capsicum", "Rice", "Onion"],
        "instructions": "Sauté onion and capsicum. Add cooked rice and spices. Mix well."
    },
    {
        "recipe_name": "Capsicum Stir Fry",
        "ingredients": ["Capsicum", "Onion"],
        "instructions": "Cut capsicum and onion. Stir-fry with spices until slightly soft."
    },

    # TOMATO
    {
        "recipe_name": "Tomato Rice",
        "ingredients": ["Tomato", "Rice", "Onion"],
        "instructions": "Sauté onion and tomato with spices. Add cooked rice and mix well."
    },
    {
        "recipe_name": "Tomato Soup",
        "ingredients": ["Tomato", "Onion"],
        "instructions": "Cook tomato and onion. Blend until smooth and boil with spices."
    },
    {
        "recipe_name": "Tomato Curry",
        "ingredients": ["Tomato", "Onion", "Potato"],
        "instructions": "Cook onion and tomato with spices. Add potato and cook until soft."
    },

    # POTATO
    {
        "recipe_name": "Aloo Rice",
        "ingredients": ["Potato", "Rice", "Onion"],
        "instructions": "Sauté potato and onion with spices. Add cooked rice and mix well."
    },
    {
        "recipe_name": "Aloo Fry",
        "ingredients": ["Potato", "Onion"],
        "instructions": "Cut potatoes and fry with onion and spices until golden."
    },
    {
        "recipe_name": "Potato Curry",
        "ingredients": ["Potato", "Tomato", "Onion"],
        "instructions": "Cook onion and tomato with spices. Add potato and cook until tender."
    },

    # CARROT
    {
        "recipe_name": "Carrot Rice",
        "ingredients": ["Carrot", "Rice", "Onion"],
        "instructions": "Sauté carrot and onion. Add cooked rice and spices and mix well."
    },
    {
        "recipe_name": "Carrot Stir Fry",
        "ingredients": ["Carrot", "Onion"],
        "instructions": "Stir-fry chopped carrot and onion with simple spices."
    },
    {
        "recipe_name": "Vegetable Rice",
        "ingredients": ["Carrot", "Potato", "Capsicum", "Rice"],
        "instructions": "Cook vegetables with spices. Add cooked rice and mix well."
    },

    # SPINACH
    {
        "recipe_name": "Palak Rice",
        "ingredients": ["Spinach", "Rice", "Onion"],
        "instructions": "Cook spinach and onion with spices. Add cooked rice and mix well."
    },
    {
        "recipe_name": "Palak Dal",
        "ingredients": ["Spinach", "Dal", "Onion"],
        "instructions": "Cook dal and spinach together with onion and spices."
    },
    {
        "recipe_name": "Spinach Curry",
        "ingredients": ["Spinach", "Tomato", "Onion"],
        "instructions": "Cook spinach with tomato, onion and spices until well combined."
    },

    # ONION
    {
        "recipe_name": "Onion Rice",
        "ingredients": ["Onion", "Rice"],
        "instructions": "Sauté sliced onion with spices. Add cooked rice and mix well."
    },
    {
        "recipe_name": "Onion Paratha",
        "ingredients": ["Onion", "Flour"],
        "instructions": "Mix chopped onion and spices with flour dough. Roll and cook on a pan."
    },

    # MILK
    {
        "recipe_name": "Milkshake",
        "ingredients": ["Milk", "Banana"],
        "instructions": "Blend milk and banana until smooth."
    },
    {
        "recipe_name": "Rice Kheer",
        "ingredients": ["Milk", "Rice", "Sugar"],
        "instructions": "Cook rice in milk. Add sugar and cook until thick."
    },
    {
        "recipe_name": "Milk Pudding",
        "ingredients": ["Milk", "Sugar"],
        "instructions": "Heat milk with sugar and cook until it thickens."
    },

    # BROCCOLI
    {
        "recipe_name": "Broccoli Stir Fry",
        "ingredients": ["Broccoli", "Onion", "Capsicum"],
        "instructions": "Stir-fry broccoli, onion and capsicum with spices."
    },

    # CAULIFLOWER
    {
        "recipe_name": "Gobi Masala",
        "ingredients": ["Cauliflower", "Tomato", "Onion"],
        "instructions": "Cook onion and tomato with spices. Add cauliflower and cook until tender."
    },

    # BEANS
    {
        "recipe_name": "Beans Stir Fry",
        "ingredients": ["Beans", "Onion", "Carrot"],
        "instructions": "Stir-fry beans, onion and carrot with spices."
    },

    # RICE
    {
        "recipe_name": "Vegetable Fried Rice",
        "ingredients": ["Rice", "Carrot", "Onion"],
        "instructions": "Cook rice. Stir-fry onion and carrot. Add cooked rice and mix well."
    },
    {
        "recipe_name": "Vegetable Pulao",
        "ingredients": ["Rice", "Carrot", "Potato", "Onion"],
        "instructions": "Sauté vegetables and spices. Add rice and water. Cook until the rice is soft."
    }

]

recipe_collection.insert_many(recipes)

print("Recipe database updated successfully!")
print("Total recipes:", recipe_collection.count_documents({}))